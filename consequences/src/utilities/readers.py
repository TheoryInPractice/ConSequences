"""
readers.py

A collection of functions for reading data.
"""

import networkx as nx
from datastructures import ContractionSequence, TreeDecomposition,\
                           PerfectEliminationOrdering


def read_pace_to_networkx_graph(pace_filename):
    """
    Takes in a graph in PACE format and returns the graph as a NetworkX Graph
    object.
    Input:
        gr_file (str): Filename for the PACE graph
    Returns:
        graph (NetworkX Graph): A Graph object inflated from gr_file
    """
    graph = nx.MultiGraph()
    with open(pace_filename, 'r') as infile:
        # Read in everything from the PACE file
        for line in infile.readlines():
            # Skip lines denoted as comments
            if line[0] == 'c':
                continue
            # Else store info from the header line
            elif line[0] == 'p':
                nodes, edges = map(int, line.split()[2:])
                # PACE format has vertices 1, ..., n
                graph.graph['nodes'] = nodes
                graph.graph['edges'] = edges
                graph.add_nodes_from(range(1, nodes + 1))
            # Else the line is an edge
            else:
                node1, node2 = map(int, line.split())
                graph.add_edge(node1, node2)

    # Sanity check: The graph should have the number of nodes and edges
    # specified in the PACE file.
    assert(graph.graph['nodes'] == graph.order())
    assert(graph.graph['edges'] == graph.size())

    return graph


def read_line_map(map_filename):
    """
    Reads in a .map file into a dictionary.
    Input:
        map_filename (str): .map file filename
    Output:
        line_map (dictionary): A dictionary mapping vertices in the line graph
        to edges in the original graph.
    """
    line_map = {}
    with open(map_filename, 'r') as infile:
        for line in infile.readlines():
            node_line, node_u, node_v = map(
                int, line.strip().replace(':', '').split())
            line_map[node_line] = (node_u, node_v)
    return line_map


def read_td_to_tree_decomposition(td_filename):
    """
    Reads in a .td file in PACE format into a TreeDecomposition object.
    Input:
        td_filename (str): .td file filename
    Output:
        td (TreeDecomposition): A populated TreeDecomposition object
    """

    td = TreeDecomposition()

    with open(td_filename, 'r') as infile:
        # Ignore comments
        line = infile.readline()
        while line[0] == 'c':
            line = infile.readline()

        # The next line will look like "s td 28 25 95"
        # Currently unused
        num_nodes, max_bag, num_vertices = map(int, line.split()[2:])

        line = infile.readline()
        while line[0] == 'b':
            # A bag line will look like:
            # "b 1 1 11 16 41 42 43 44 45"
            node = int(line.split()[1])
            vertices = set(map(int, line.split()[2:]))
            td.bags[node] = vertices
            line = infile.readline()

        # Add a node for each bag
        td.tree.add_nodes_from(td.bags)

        # Add the first edge
        td.tree.add_edge(*map(int, line.split()))

        # The remainder of the file is edges
        for line in infile.readlines():
            td.tree.add_edge(*map(int, line.split()))

    return td


def read_contraction_sequence(conseq_filename):
    """
    Reads in a contraction sequence (usually .conseq) file into a
    ContractionSequence object.
    Input:
        conseq_filename (str): Filename for contraction sequence
    Output:
        conseq (ContractionSequence): The populated contraction sequence
    """

    conseq = ContractionSequence()
    with open(conseq_filename, 'r') as infile:
        for line in infile.readlines():
            conseq.ordering.append(tuple(map(int, line.strip().split())))
    return conseq


def read_perfect_elimination_ordering(peo_filename):
    peo = PerfectEliminationOrdering()
    with open(peo_filename, 'r') as infile:
        for line in infile.readlines():
            peo.ordering.append(int(line))
    return peo
