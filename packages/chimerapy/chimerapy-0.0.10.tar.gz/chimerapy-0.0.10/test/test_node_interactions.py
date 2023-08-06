from typing import Dict, Any
import time
import logging
import pdb

import numpy as np
import pytest
from pytest_lazyfixture import lazy_fixture

import chimerapy as cp

cp.debug()

logger = cp._logger.getLogger("chimerapy")


class LowFrequencyNode(cp.Node):
    def prep(self):
        self.i = 0

    def step(self):
        data_chunk = cp.DataChunk()
        if self.i == 0:
            time.sleep(0.5)
            self.i += 1
            data_chunk.add("i", self.i)
            return data_chunk
        else:
            time.sleep(3)
            self.i += 1
            data_chunk.add("i", self.i)
            return data_chunk


class HighFrequencyNode(cp.Node):
    def prep(self):
        self.i = 0

    def step(self):
        time.sleep(0.1)
        self.i += 1
        data_chunk = cp.DataChunk()
        data_chunk.add("i", self.i)
        return data_chunk


class SubsequentNode(cp.Node):
    def prep(self):
        self.record = {}

    def step(self, data: Dict[str, cp.DataChunk]):

        for k, v in data.items():
            self.record[k] = v

        data_chunk = cp.DataChunk()
        data_chunk.add("record", self.record)

        return data_chunk


@pytest.fixture
def step_up_graph():
    hf = HighFrequencyNode(name="hf")
    lf = LowFrequencyNode(name="lf")
    sn = SubsequentNode(name="sn")

    graph = cp.Graph()
    graph.add_nodes_from([hf, lf, sn])

    graph.add_edge(src=hf, dst=sn, follow=True)
    graph.add_edge(src=lf, dst=sn)

    return (graph, [hf.id, lf.id, sn.id])


@pytest.fixture
def step_down_graph():
    hf = HighFrequencyNode(name="hf")
    lf = LowFrequencyNode(name="lf")
    sn = SubsequentNode(name="sn")

    graph = cp.Graph()
    graph.add_nodes_from([hf, lf, sn])

    graph.add_edge(src=hf, dst=sn)
    graph.add_edge(src=lf, dst=sn, follow=True)

    return (graph, [hf.id, lf.id, sn.id])


@pytest.mark.parametrize(
    "config_graph_data, follow",
    [
        (
            lazy_fixture("step_up_graph"),
            "up",
        ),
        (
            lazy_fixture("step_down_graph"),
            "down",
        ),
    ],
)
def test_node_frequency_execution(manager, worker, config_graph_data, follow):

    # Decompose graph data
    config_graph, node_ids = config_graph_data

    # Connect to the manager
    worker.connect(host=manager.host, port=manager.port)

    # Then register graph to manager
    manager.commit_graph(
        config_graph,
        {
            worker.id: node_ids,
        },
    )

    # Take a single step and see if the system crashes and burns
    manager.start()
    time.sleep(3)
    manager.stop()

    # Convert name to id
    name_to_id = {
        data["object"].name: n for n, data in manager.graph.G.nodes(data=True)
    }

    # Then request gather and confirm that the data is valid
    latest_data_values = manager.gather()
    logger.info(f"Data Values: {latest_data_values}")
    data_chunk_step_records = latest_data_values[name_to_id["sn"]]
    step_records = data_chunk_step_records.get("record")["value"]

    if follow == "up":
        assert step_records["lf"] == latest_data_values[name_to_id["lf"]]
        assert (
            np.abs(
                (
                    step_records["hf"].get("i")["value"]
                    - latest_data_values[name_to_id["hf"]].get("i")["value"]
                )
            )
            < 5
        )
    elif follow == "down":
        assert step_records["lf"] == latest_data_values[name_to_id["lf"]]
        assert step_records["hf"] != latest_data_values[name_to_id["hf"]]
