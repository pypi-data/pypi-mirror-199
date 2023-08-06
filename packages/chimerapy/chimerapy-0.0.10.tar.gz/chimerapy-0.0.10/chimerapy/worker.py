from typing import Union, Dict, Any, Coroutine, Optional
import os
import time
import tempfile
import pathlib
import shutil
import sys
import pickle
import uuid
import collections

# Third-party Imports
import dill
import aiohttp
from aiohttp import web
import requests

from chimerapy import config
from .states import WorkerState, NodeState
from .utils import get_ip_address, waiting_for, async_waiting_for
from .networking import Server, Client, DataChunk
from .networking.enums import (
    NODE_MESSAGE,
    WORKER_MESSAGE,
)
from . import _logger


class Worker:
    def __init__(
        self,
        name: str,
        port: int = 10000,
        delete_temp: bool = True,
        id: Optional[str] = None,
    ):
        """Create a local Worker.

        To execute ``Nodes`` within the main computer that is also housing
        the ``Manager``, it will require a ``Worker`` as well. Therefore,
        it is common to create a ``Worker`` and a ``Manager`` within the
        same computer.

        To create a worker in another machine, you will have to use the
        following command (in the other machine's terminal):

        >>> cp-worker --ip <manager's IP> --port <manager's port> --name <name>

        Args:
            name (str): The name for the ``Worker`` that will be used \
                as reference.
            port (int): The port of the Worker's HTTP server. Select 0 \
                for a random port, mostly when running multiple Worker \
                instances in the same computer.
            delete_temp (bool): After session is over, should the Worker
                delete any of the temporary files.

        """
        # Saving parameters
        if isinstance(id, str):
            id = id
        else:
            id = str(uuid.uuid4())

        # Creating state
        self.state = WorkerState(id=id, name=name, port=port)
        self.nodes_extra = collections.defaultdict(dict)

        # Instance variables
        self.has_shutdown: bool = False
        self.manager_ack: bool = False
        self.connected_to_manager: bool = False
        self.manager_host = "0.0.0.0"
        self.manager_url = ""

        # Create temporary data folder
        self.delete_temp = delete_temp
        self.tempfolder = pathlib.Path(tempfile.mkdtemp())

        parent_logger = _logger.getLogger("chimerapy-worker")
        self.logger = _logger.fork(parent_logger, name, id)

        # Create server
        self.server = Server(
            port=self.state.port,
            id=self.state.id,
            routes=[
                web.post("/nodes/create", self.async_create_node),
                web.get("/nodes/server_data", self.report_node_server_data),
                web.post("/nodes/server_data", self.process_node_server_data),
                web.get("/nodes/gather", self.report_node_gather),
                web.post("/nodes/save", self.report_node_saving),
                web.post("/nodes/collect", self.send_archive),
                web.post("/nodes/step", self.async_step),
                web.post("/packages/load", self.load_sent_packages),
                web.post("/nodes/start", self.async_start_nodes),
                web.post("/nodes/stop", self.async_stop_nodes),
                web.post("/shutdown", self.async_shutdown),
            ],
            ws_handlers={
                NODE_MESSAGE.STATUS: self.node_status_update,
                NODE_MESSAGE.REPORT_GATHER: self.node_report_gather,
            },
            parent_logger=self.logger,
        )

        # Start the server and get the new port address (random if port=0)
        self.server.serve()
        self.state.ip, self.state.port = self.server.host, self.server.port

        self.logger.info(
            f"Worker {self.state.id} running HTTP server at {self.state.ip}:{self.state.port}"
        )

        # Create a log listener to read Node's information
        self.logreceiver = self._start_log_receiver()
        self.logger.debug(f"Log receiver started at port {self.logreceiver.port}")

    def __repr__(self):
        return f"<Worker name={self.state.name} id={self.state.id}>"

    def __str__(self):
        return self.__repr__()

    ####################################################################
    ## Properties
    ####################################################################

    @property
    def id(self) -> str:
        return self.state.id

    @property
    def name(self) -> str:
        return self.state.name

    @property
    def nodes(self) -> Dict[str, NodeState]:
        return self.state.nodes

    @property
    def ip(self) -> str:
        return self.state.ip

    @property
    def port(self) -> int:
        return self.state.port

    ####################################################################
    ## Manager -> Worker
    ####################################################################

    async def load_sent_packages(self, request: web.Request):
        msg = await request.json()

        # For each package, extract it from the client's tempfolder
        # and load it to the sys.path
        for sent_package in msg["packages"]:

            # Wait until the sent package are started
            success = await async_waiting_for(
                condition=lambda: f"{sent_package}.zip"
                in self.server.file_transfer_records["Manager"],
                timeout=config.get("worker.timeout.package-delivery"),
            )

            if success:
                self.logger.debug(
                    f"{self}: Waiting for package {sent_package}: SUCCESS"
                )
            else:
                self.logger.error(f"{self}: Waiting for package {sent_package}: FAILED")
                return web.HTTPError()

            # Get the path
            package_zip_path = self.server.file_transfer_records["Manager"][
                f"{sent_package}.zip"
            ]["dst_filepath"]

            # Wait until the sent package is complete
            success = await async_waiting_for(
                condition=lambda: self.server.file_transfer_records["Manager"][
                    f"{sent_package}.zip"
                ]["complete"]
                == True,
                timeout=config.get("worker.timeout.package-delivery"),
            )

            if success:
                self.logger.debug(f"{self}: Package {sent_package} loading: SUCCESS")
            else:
                self.logger.debug(f"{self}: Package {sent_package} loading: FAILED")

            assert (
                package_zip_path.exists()
            ), f"{self}: {package_zip_path} doesn't exists!?"
            sys.path.insert(0, str(package_zip_path))

        # Send message back to the Manager letting them know that
        self.logger.info(f"{self}: Completed loading packages sent by Manager")
        return web.HTTPOk()

    async def async_create_node(
        self,
        request: Optional[web.Request] = None,
        node_config: Optional[Dict[str, Any]] = None,
    ):

        if isinstance(request, web.Request):
            msg_bytes = await request.read()
            msg = pickle.loads(msg_bytes)
        elif isinstance(node_config, dict):
            msg = node_config
        else:
            raise RuntimeError("Invalid node creation, need request or msg")

        # Saving name to track it for now
        node_id = msg["id"]
        self.logger.debug(f"{self}: received request for Node {id} creation: {msg}")

        # Saving the node data
        self.state.nodes[node_id] = NodeState(id=node_id)
        self.nodes_extra[node_id]["response"] = False
        self.nodes_extra[node_id]["gather"] = DataChunk()
        self.nodes_extra[node_id].update({k: v for k, v in msg.items() if k != "id"})
        self.logger.debug(f"{self}: created state for <Node {node_id}>")

        # Keep trying to start a process until success
        success = False
        for i in range(config.get("worker.allowed-failures")):

            # Decode the node object
            self.nodes_extra[node_id]["node_object"] = dill.loads(
                self.nodes_extra[node_id]["pickled"]
            )
            self.logger.debug(f"{self}: unpickled <Node {node_id}>")

            # Record the node name
            self.state.nodes[node_id].name = self.nodes_extra[node_id][
                "node_object"
            ].name

            # Provide configuration information to the node once in the client
            self.nodes_extra[node_id]["node_object"].config(
                self.state.ip,
                self.state.port,
                self.tempfolder,
                self.nodes_extra[node_id]["in_bound"],
                self.nodes_extra[node_id]["in_bound_by_name"],
                self.nodes_extra[node_id]["out_bound"],
                self.nodes_extra[node_id]["follow"],
                logging_level=self.logger.level,
                worker_logging_port=self.logreceiver.port,
            )

            # Before starting, over write the pid
            self.nodes_extra[node_id]["node_object"]._parent_pid = os.getpid()

            # Start the node
            self.nodes_extra[node_id]["node_object"].start()
            self.logger.debug(f"{self}: started <Node {node_id}>")

            # Wait until response from node
            success = await async_waiting_for(
                condition=lambda: self.state.nodes[node_id].init == True,
                timeout=config.get("worker.timeout.node-creation"),
            )

            if success:
                self.logger.debug(f"{self}: {node_id} responding, SUCCESS")
            else:
                # Handle failure
                self.logger.debug(f"{self}: {node_id} responding, FAILED, retry")
                self.nodes_extra[node_id]["node_object"].shutdown()
                self.nodes_extra[node_id]["node_object"].terminate()
                continue

            # Now we wait until the node has fully initialized and ready-up
            success = await async_waiting_for(
                condition=lambda: self.state.nodes[node_id].ready == True,
                timeout=config.get("worker.timeout.info-request"),
            )

            if success:
                self.logger.debug(f"{self}: {node_id} fully ready, SUCCESS")
                break
            else:
                # Handle failure
                self.logger.debug(f"{self}: {node_id} fully ready, FAILED, retry")
                self.nodes_extra[node_id]["node_object"].shutdown()
                self.nodes_extra[node_id]["node_object"].terminate()

        if not success:
            self.logger.error(f"{self}: Node {node_id} failed to create")
        else:
            # Mark success
            self.logger.debug(f"{self}: completed node creation: {node_id}")

        # Update the manager with the most up-to-date status of the nodes
        response = {
            "success": success,
            "node_state": self.state.nodes[node_id].to_dict(),
        }

        if isinstance(request, web.Request):
            return web.json_response(response)
        else:
            return success

    async def report_node_server_data(self, request: web.Request):

        node_server_data = self.create_node_server_data()
        return web.json_response(
            {"success": True, "node_server_data": node_server_data}
        )

    async def process_node_server_data(self, request: web.Request):
        msg = await request.json()

        self.logger.debug(f"{self}: processing node server data")

        await self.server.async_broadcast(
            signal=WORKER_MESSAGE.BROADCAST_NODE_SERVER_DATA,
            data=msg,
        )

        # Now wait until all nodes have responded as CONNECTED
        success = []
        for node_id in self.state.nodes:
            for i in range(config.get("worker.allowed-failures")):
                if await async_waiting_for(
                    condition=lambda: self.state.nodes[node_id].connected == True,
                    timeout=config.get("worker.timeout.info-request"),
                ):
                    self.logger.debug(f"{self}: Nodes {node_id} has connected: PASS")
                    success.append(True)
                    break
                else:
                    self.logger.debug(f"{self}: Node {node_id} has connected: FAIL")
                    success.append(False)

        if not all(success):
            self.logger.error(f"{self}: Nodes failed to establish P2P connections")

        # After all nodes have been connected, inform the Manager
        self.logger.debug(f"{self}: Informing Manager of processing completion")

        return web.json_response(
            {"success": True, "worker_state": self.state.to_dict()}
        )

    async def async_step(self, request: web.Request):

        # Worker tell all nodes to take a step
        await self.server.async_broadcast(signal=WORKER_MESSAGE.REQUEST_STEP, data={})

        return web.HTTPOk()

    async def async_start_nodes(self, request: web.Request):

        # Send message to nodes to start
        await self.server.async_broadcast(signal=WORKER_MESSAGE.START_NODES, data={})

        return web.HTTPOk()

    async def async_stop_nodes(self, request: web.Request):

        # Send message to nodes to start
        await self.server.async_broadcast(signal=WORKER_MESSAGE.STOP_NODES, data={})

        return web.HTTPOk()

    async def async_shutdown(self, request: web.Request):
        self.shutdown()

        return web.HTTPOk()

    async def report_node_saving(self, request: web.Request):

        # Request saving from Worker to Nodes
        await self.server.async_broadcast(signal=WORKER_MESSAGE.REQUEST_SAVING, data={})

        # Now wait until all nodes have responded as CONNECTED
        success = []
        for i in range(config.get("worker.allowed-failures")):
            for node_id in self.nodes:

                if await async_waiting_for(
                    condition=lambda: self.state.nodes[node_id].finished == True,
                    timeout=config.get("worker.timeout.info-request"),
                ):
                    self.logger.debug(
                        f"{self}: Node {node_id} responded to saving request: PASS"
                    )
                    success.append(True)
                    break
                else:
                    self.logger.debug(
                        f"{self}: Node {node_id} responded to saving request: FAIL"
                    )
                    success.append(False)

        if not all(success):
            self.logger.error(f"{self}: Nodes failed to report to saving")

        # Send it back to the Manager
        return web.HTTPOk()

    async def report_node_gather(self, request: web.Request):

        self.logger.debug(f"{self}: reporting to Manager gather request")

        for node_id in self.state.nodes:
            self.nodes_extra[node_id]["response"] = False

        # Request gather from Worker to Nodes
        await self.server.async_broadcast(signal=WORKER_MESSAGE.REQUEST_GATHER, data={})

        # Wait until all Nodes have gather
        success = []
        for node_id in self.state.nodes:
            for i in range(config.get("worker.allowed-failures")):

                if await async_waiting_for(
                    condition=lambda: self.nodes_extra[node_id]["response"] == True,
                    timeout=config.get("worker.timeout.info-request"),
                ):
                    self.logger.debug(
                        f"{self}: Node {node_id} responded to gather: PASS"
                    )
                    success.append(True)
                    break
                else:
                    self.logger.debug(
                        f"{self}: Node {node_id} responded to gather: FAIL"
                    )
                    success.append(False)

                if not all(success):
                    self.logger.error(f"{self}: Nodes failed to report to gather")

        # Gather the data from the nodes!
        gather_data = {"id": self.state.id, "node_data": {}}
        for node_id, node_data in self.nodes_extra.items():
            if node_data["gather"] == None:
                data_chunk = DataChunk()
                data_chunk.add("default", None)
                node_data["gather"] = data_chunk
            gather_data["node_data"][node_id] = node_data["gather"]

        return web.Response(body=pickle.dumps(gather_data))

    async def send_archive(self, request: web.Request):
        msg = await request.json()

        # Default value of success
        success = False

        # If located in the same computer, just move the data
        if self.manager_host == get_ip_address():

            self.logger.debug(f"{self}: sending archive locally")

            # First rename and then move
            delay = 1
            miss_counter = 0
            timeout = 10
            while True:
                try:
                    shutil.move(self.tempfolder, pathlib.Path(msg["path"]))
                    break
                except shutil.Error:  # File already exists!
                    break
                except:
                    time.sleep(delay)
                    miss_counter += 1
                    if miss_counter * delay > timeout:
                        raise TimeoutError("Nodes haven't fully finishing saving!")

            old_folder_name = pathlib.Path(msg["path"]) / self.tempfolder.name
            new_folder_name = pathlib.Path(msg["path"]) / f"{self.name}-{self.id}"
            os.rename(old_folder_name, new_folder_name)

        else:

            self.logger.debug(f"{self}: sending archive via network")

            # Else, send the archive data to the manager via network
            try:
                # Create a temporary HTTP client
                client = Client(self.id, host=self.manager_host, port=self.manager_port)
                # client.send_file(sender_name=self.name, filepath=zip_package_dst)
                await client._send_folder_async(self.name, self.tempfolder)
                success = True
            except (TimeoutError, SystemError) as error:
                self.delete_temp = False
                self.logger.exception(
                    f"{self}: Failed to transmit files to Manager - {error}."
                )
                success = False

        # After completion, let the Manager know
        return web.json_response({"id": self.id, "success": success})

    ####################################################################
    ## Worker <-> Node
    ####################################################################

    async def node_report_gather(self, msg: Dict, ws: web.WebSocketResponse):

        # Saving gathering value
        node_state = NodeState.from_dict(msg["data"]["state"])
        node_id = node_state.id
        self.state.nodes[node_id] = node_state

        self.nodes_extra[node_id]["gather"] = msg["data"]["latest_value"]
        self.nodes_extra[node_id]["response"] = True

    async def node_status_update(self, msg: Dict, ws: web.WebSocketResponse):

        self.logger.debug(f"{self}: note_status_update: ", msg)
        node_state = NodeState.from_dict(msg["data"])
        node_id = node_state.id

        # Update our records by grabbing all data from the msg
        self.state.nodes[node_id] = node_state

        # Update Manager on the new nodes status
        if self.connected_to_manager:
            async with aiohttp.ClientSession(self.manager_url) as session:
                async with session.post(
                    "/workers/node_status", data=self.state.to_json()
                ):
                    pass

    ####################################################################
    ## Helper Methods
    ####################################################################

    def create_node_server_data(self):

        # Construct simple data structure for Node to address information
        node_server_data = {"id": self.state.id, "nodes": {}}
        for node_id, node_state in self.state.nodes.items():
            node_server_data["nodes"][node_id] = {
                "host": self.state.ip,
                "port": node_state.port,
            }

        return node_server_data

    def exec_coro(self, coro: Coroutine):
        self.server._thread.exec(coro)

    ####################################################################
    ## Worker Sync Lifecycle API
    ####################################################################

    def connect(self, host: str, port: int, timeout: Union[int, float] = 10.0) -> bool:
        """Connect ``Worker`` to ``Manager``.

        This establish server-client connections between ``Worker`` and
        ``Manager``. To ensure that the connections are close correctly,
        either the ``Manager`` or ``Worker`` should shutdown before
        stopping your program to avoid processes and threads that do
        not shutdown.

        Args:
            host (str): The ``Manager``'s IP address.
            port (int): The ``Manager``'s port number
            timeout (Union[int, float]): Set timeout for the connection.

        Returns:
            bool: Success in connecting to the Manager

        """

        # Sending message to register
        r = requests.post(
            f"http://{host}:{port}/workers/register",
            data=self.state.to_json(),
            timeout=config.get("worker.timeout.info-request"),
        )

        # Check if success
        if r.status_code == requests.codes.ok:

            # Update the configuration of the Worker
            config.update_defaults(r.json())

            # Tracking the state and location of the manager
            self.connected_to_manager = True
            self.manager_host = host
            self.manager_port = port
            self.manager_url = f"http://{host}:{port}"
            self.logger.info(
                f"{self}: connection successful to Manager located at {host}:{port}."
            )
            return True

        return False

    def deregister(self):

        r = requests.post(
            self.manager_url + "/workers/deregister",
            data=self.state.to_json(),
            timeout=config.get("worker.timeout.info-request"),
        )

        self.connected_to_manager = False

        return r.status_code == requests.codes.ok

    def create_node(self, msg: Dict[str, Any]):
        node_id = msg["id"]
        self.server._thread.exec(lambda: self.async_create_node(node_config=msg))

        success = waiting_for(
            condition=lambda: node_id in self.state.nodes
            and self.state.nodes[node_id].ready == True,
            check_period=0.1,
            timeout=config.get("manager.timeout.node-creation"),
        )

        return success

    def step(self):

        # Worker tell all nodes to take a step
        self.server.broadcast(signal=WORKER_MESSAGE.REQUEST_STEP, data={})

    def start_nodes(self):

        # Send message to nodes to start
        self.server.broadcast(signal=WORKER_MESSAGE.START_NODES, data={})

    def stop_nodes(self):

        # Send message to nodes to start
        self.server.broadcast(signal=WORKER_MESSAGE.STOP_NODES, data={})

    def idle(self):

        self.logger.debug(f"{self}: Idle")

        while not self.has_shutdown:
            time.sleep(2)

    def shutdown(self, msg: Dict = {}):
        """Shutdown ``Worker`` safely.

        The ``Worker`` needs to shutdown its server, client and ``Nodes``
        in a safe manner, such as setting flag variables and clearing
        out queues.

        Args:
            msg (Dict): Leave empty, required to work when ``Manager`` sends\
            shutdown message to ``Worker``.

        """
        # Check if shutdown has been called already
        if self.has_shutdown:
            self.logger.debug(f"{self}: requested to shutdown when already shutdown.")
            return
        else:
            self.has_shutdown = True

        self.logger.debug(f"{self}: shutting down!")
        # Sending message to Manager that client is shutting down (only
        # if the manager hasn't already set the client to not running)
        if self.connected_to_manager:
            try:
                self.deregister()
            except requests.ConnectionError:
                self.logger.warning(f"{self}: shutdown didn't reach Manager")

        # Shutdown the Worker 2 Node server
        self.server.shutdown()

        # Shutdown nodes from the client (start all shutdown)
        for node_id in self.nodes_extra:
            self.nodes_extra[node_id]["node_object"].shutdown()

        # Then wait until close, or force
        for node_id in self.nodes_extra:
            self.nodes_extra[node_id]["node_object"].join(
                timeout=config.get("worker.timeout.node-shutdown")
            )

            # If that doesn't work, terminate
            if self.nodes_extra[node_id]["node_object"].exitcode != 0:
                self.logger.warning(f"{self}: Node {node_id} forced shutdown")
                self.nodes_extra[node_id]["node_object"].terminate()

            self.logger.debug(f"{self}: Nodes have joined")

        # Delete temp folder if requested
        if self.tempfolder.exists() and self.delete_temp:
            shutil.rmtree(self.tempfolder)

    def __del__(self):

        # Also good to shutdown anything that isn't
        if not self.has_shutdown:
            self.shutdown()

    @staticmethod
    def _start_log_receiver() -> "ZMQNodeIDListener":
        log_receiver = _logger.get_node_id_zmq_listener()
        log_receiver.start(register_exit_handlers=True)
        return log_receiver
