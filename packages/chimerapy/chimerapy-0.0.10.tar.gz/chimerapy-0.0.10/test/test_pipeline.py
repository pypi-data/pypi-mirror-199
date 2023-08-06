import logging

import pytest
from pytest_lazyfixture import lazy_fixture
import numpy as np

import chimerapy as cp

logger = cp._logger.getLogger("chimerapy")

# How to test with matplotlib
# https://stackoverflow.com/questions/63541241/networkx-drawing-in-layered-manner


@pytest.fixture
def simple_graph():

    a = cp.Node(name="a")
    b = cp.Node(name="b")

    graph = cp.Graph()
    graph.add_nodes_from([a, b])
    graph.add_edge(a, b)

    return graph


@pytest.fixture
def slightly_more_complex_graph():

    a = cp.Node(name="a")
    b = cp.Node(name="b")
    c = cp.Node(name="c")
    d = cp.Node(name="d")

    graph = cp.Graph()
    graph.add_nodes_from([a, b, c, d])
    graph.add_edges_from([[a, b], [a, c], [b, c], [c, d]])
    return graph


@pytest.fixture
def complex_graph():

    a = cp.Node(name="a")
    b = cp.Node(name="b")
    c = cp.Node(name="c")
    d = cp.Node(name="d")
    e = cp.Node(name="e")
    f = cp.Node(name="f")

    graph = cp.Graph()
    graph.add_nodes_from([a, b, c, d, e, f])
    graph.add_edges_from([[a, b], [c, d], [c, e], [b, e], [d, f], [e, f]])
    return graph


@pytest.mark.parametrize(
    "graph",
    [
        (lazy_fixture("simple_graph")),
        (lazy_fixture("slightly_more_complex_graph")),
        (lazy_fixture("complex_graph")),
    ],
)
def test_graph_instance(graph):
    assert isinstance(graph, cp.Graph)


@pytest.mark.skip(reason="need to automate matplotlib test")
@pytest.mark.parametrize(
    "graph",
    [
        (lazy_fixture("simple_graph")),
        (lazy_fixture("slightly_more_complex_graph")),
        (lazy_fixture("complex_graph")),
    ],
)
def test_graph_simple_visualization(graph):

    # Visualize the graph
    graph.plot()
