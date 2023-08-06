# Built-in Imports
import os
import time
import logging
import collections
import pathlib

# Third-party Imports
import dill
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal Imports
import chimerapy as cp

logger = cp._logger.getLogger("chimerapy")
# cp.debug(["chimerapy-networking"])
cp.debug()

from .data_nodes import VideoNode, AudioNode, ImageNode, TabularNode
from ..conftest import linux_run_only, linux_expected_only
from ..mock import DockeredWorker
from ..utils import cleanup_and_recreate_dir
import shutil

pytestmark = [pytest.mark.slow, pytest.mark.timeout(600)]

# References:
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

NAME_CLASS_MAP = {
    "vn": VideoNode,
    "img_n": ImageNode,
    "tn": TabularNode,
    "an": AudioNode,
}
NUM_OF_WORKERS = 3


@pytest.fixture
def single_worker_manager(manager, worker):

    # Define graph
    graph = cp.Graph()
    node_ids = []
    for node_name, node_class in NAME_CLASS_MAP.items():
        node = node_class(name=node_name)
        node_ids.append(node.id)
        graph.add_node(node)

    # Connect to the manager
    worker.connect(host=manager.host, port=manager.port)

    # Then register graph to Manager
    assert manager.commit_graph(
        graph,
        {worker.id: node_ids},
    )

    return manager


@pytest.fixture
def multiple_worker_manager(manager, worker):

    # Construct graph
    graph = cp.Graph()

    workers = []
    worker_node_map = collections.defaultdict(list)
    for i in range(NUM_OF_WORKERS):
        worker = cp.Worker(name=f"W{i}", port=0)
        worker.connect(host=manager.host, port=manager.port)
        workers.append(worker)

        # For each worker, add all possible nodes
        for node_name, node_class in NAME_CLASS_MAP.items():
            node = node_class(name=node_name)
            worker_node_map[worker.id].append(node.id)
            graph.add_node(node)

    # Then register graph to Manager
    assert manager.commit_graph(graph, worker_node_map)

    yield manager

    for worker in workers:
        worker.shutdown()


@pytest.fixture
def dockered_single_worker_manager(manager, docker_client):

    worker = DockeredWorker(docker_client, name="docker")

    # Define graph
    graph = cp.Graph()
    node_ids = []
    for node_name, node_class in NAME_CLASS_MAP.items():
        node = node_class(name=node_name)
        node_ids.append(node.id)
        graph.add_node(node)

    # Connect to the manager
    worker.connect(host=manager.host, port=manager.port)

    # Then register graph to Manager
    assert manager.commit_graph(
        graph,
        {worker.id: node_ids},
    )

    return manager


@pytest.fixture
def dockered_multiple_worker_manager(manager, docker_client):

    # Construct graph
    graph = cp.Graph()

    workers = []
    worker_node_map = collections.defaultdict(list)
    for i in range(NUM_OF_WORKERS):
        worker = DockeredWorker(docker_client, name=f"W{i}")
        worker.connect(host=manager.host, port=manager.port)
        workers.append(worker)

        # For each worker, add all possible nodes
        for node_name, node_class in NAME_CLASS_MAP.items():
            node = node_class(name=node_name)
            worker_node_map[worker.id].append(node.id)
            graph.add_node(node)

    # Then register graph to Manager
    assert manager.commit_graph(graph, worker_node_map)

    yield manager

    for worker in workers:
        worker.shutdown()


def test_worker_data_archiving(worker):

    # Just for debugging
    # worker.delete_temp = False

    nodes = []
    for node_name, node_class in NAME_CLASS_MAP.items():
        nodes.append(node_class(name=node_name))

    # Simple single node without connection
    for node in nodes:
        msg = {
            "id": node.id,
            "name": node.name,
            "pickled": dill.dumps(node),
            "in_bound": [],
            "in_bound_by_name": [],
            "out_bound": [],
            "follow": None,
        }
        worker.create_node(msg)

    logger.debug("Waiting!")
    time.sleep(2)

    logger.debug("Start nodes!")
    worker.start_nodes()

    logger.debug("Let nodes run for some time")
    time.sleep(1)

    for node_name in NAME_CLASS_MAP:
        assert (worker.tempfolder / node_name).exists()


# @pytest.mark.repeat(5)
@pytest.mark.parametrize(
    "config_manager, expected_number_of_folders",
    [
        (lazy_fixture("single_worker_manager"), 1),
        (lazy_fixture("multiple_worker_manager"), NUM_OF_WORKERS),
        pytest.param(
            lazy_fixture("dockered_single_worker_manager"),
            1,
            marks=linux_run_only,
        ),
        pytest.param(
            lazy_fixture("dockered_multiple_worker_manager"),
            NUM_OF_WORKERS,
            marks=linux_run_only,
        ),
    ],
)
def test_manager_worker_data_transfer(config_manager, expected_number_of_folders):

    # Take a single step and see if the system crashes and burns
    config_manager.start()
    time.sleep(2)
    config_manager.stop()

    # Transfer the files to the Manager's logs
    assert config_manager.collect()

    # Assert the behavior
    assert (
        len([x for x in config_manager.logdir.iterdir() if x.is_dir()])
        == expected_number_of_folders
    )
    assert (config_manager.logdir / "meta.json").exists()
    for worker_id in config_manager.workers:
        for node_id in config_manager.workers[worker_id].nodes:
            assert config_manager.workers[worker_id].nodes[node_id].finished

    # Cleanup in case reruns
    cleanup_and_recreate_dir(config_manager.logdir)
