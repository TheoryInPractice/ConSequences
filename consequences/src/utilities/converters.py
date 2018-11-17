from datastructures import ContractionSequence, LegLinks,\
                           PerfectEliminationOrdering,\
                           TreeDecomposition
from readers import read_td_to_tree_decomposition, read_line_map, \
                    read_contraction_sequence, read_pace_to_networkx_graph
from writers import write_conseq, write_td
import copy
from itertools import product, combinations

import networkx as nx

"""
converters.py

A collection of functions for transforming data.
"""


def td_to_conseq(line_map_filename, td_filename, conseq_filename):
    line_map = read_line_map(line_map_filename)

    td = read_td_to_tree_decomposition(td_filename)
    print("td bags:", td.bags)
    print("td tree edges:", td.tree.edges())
    eo = td_to_eo(td)
    print("eo:", eo.ordering)
    conseq = eo_to_conseq(eo, line_map)
    print("conseq:", conseq.ordering)
    new_node_conseq = conseq_to_new_node_conseq(conseq)
    print("new_node_conseq:", new_node_conseq.ordering)
    write_conseq(new_node_conseq, conseq_filename)


def conseq_to_td(graph_filename, line_graph_filename,
                 line_map_filename, conseq_filename, td_filename):
    graph = read_pace_to_networkx_graph(graph_filename)
    line_graph = read_pace_to_networkx_graph(line_graph_filename)
    line_map = read_line_map(line_map_filename)

    new_node_conseq = read_contraction_sequence(conseq_filename)
    print("qTorch conseq:", new_node_conseq.ordering)
    conseq = new_node_conseq_to_conseq(new_node_conseq, graph)
    print("conseq:", conseq.ordering)
    eo = conseq_to_eo(conseq, line_map)
    print("eo:", eo.ordering)
    td = eo_to_td(eo, line_graph)
    write_td(td, td_filename)


def networkx_graph_to_line_graph(graph):
    """
    Takes in a NetworkX graph and computes its line graph.
    Input:
        graph (NetworkX Graph): The graph
    Returns:
        line_graph (NetworkX Graph): The line graph
        map (dict): A lookup table mapping new vertex name to old vertex name
    """
    pass


def networkx_graph_to_leglinks(graph):
    """
    Converts a NetworkX graph to a list of leg links for MATLAB.
    Input:
        graph (NetworkX Graph): The graph
    Returns:
        legs (LegLinks): A lookup table that maps each vertex to a list
        of its incident edges.
    """
    # Make a lookup table where edge_label_lookup[node1][node2] returns the
    # label of the edge (node1, node2)
    # Start edge labels at 1
    edge_label_lookup = {}
    for edge_label, (node1, node2) in enumerate(sorted(graph.edges()), 1):
        if node1 in edge_label_lookup:
            edge_label_lookup[node1][node2] = edge_label
        else:
            edge_label_lookup[node1] = {node2: edge_label}

        if node2 in edge_label_lookup:
            edge_label_lookup[node2][node1] = edge_label
        else:
            edge_label_lookup[node2] = {node1: edge_label}

    # Compute the leg links
    legs = LegLinks()
    for node in sorted(graph.nodes()):
        legs.incident_edges[node] = sorted(list(map(lambda neighbor:
            edge_label_lookup[node][neighbor], graph.neighbors(node))))

    return legs


def _increment_eo(td, eo):
    """
    Given a TreeDecomposition and a (partial) PerfectEliminationOrdering, add
    one more vertex to the eo or recognize that we're
    already done.
    Input:
        td (TreeDecomposition): A tree decomposition.
        eo (PerfectEliminationOrdering): The perfect elimination ordering
        currently being constructed.
    Output:
        The final eo returned by a recursive call.
    """

    # Base case: If one node left, add its vertices to the eo
    if td.tree.order() == 1:
        only_vertex = list(td.tree.nodes())[0]
        eo.ordering += sorted(td.bags[only_vertex])
        return eo

    # Otherwise we can identify a leaf and its parent
    leaf = list(filter(lambda node: td.tree.degree[node] == 1,
                td.tree.nodes()))[0]
    parent = min(list(td.tree.neighbors(leaf)))

    # See if there are any vertices in leaf's bag that are not in
    # parent's bag
    vertex_diff = td.bags[leaf] - td.bags[parent]

    # If there's a vertex in the leaf and not in the parent,
    # then remove it from the graph and add it to the eo.
    if vertex_diff:
        next_vertex = min(vertex_diff)
        eo.ordering.append(next_vertex)
        for key in td.bags:
            td.bags[key].discard(next_vertex)

    # Else remove the leaf from the graph
    else:
        td.tree.remove_node(leaf)
        td.bags.pop(leaf)

    # Recurse until we hit the base case
    return _increment_eo(td, eo)


def td_to_eo(td):
    """
    Generates a perfect elimination ordering from a tree decomposition. The
    algorithm is taken from Markov and Shi Proof of Prop 4.2
    (https://arxiv.org/pdf/quant-ph/0511069.pdf).
    Input:
        td (TreeDecomposition): A tree decomposition for a graph.
    Output:
        eo (PerfectEliminationOrdering): A perfect elimination ordering
        corresponding to the tree decomposition (Note: There may be multiple
        valid eo for a given td).
    """

    # Copy the tree decomposition, my_td will be modified recursively
    my_td = copy.deepcopy(td)

    # Recursively construct the eo
    eo = _increment_eo(my_td, PerfectEliminationOrdering())
    return eo


def eo_to_td(eo, line_graph):
    """
    Constructs a tree decomposition from a perfect elimination ordering.
    """

    td = TreeDecomposition()

    # Copy the graph so we can modify it incrementally
    gr = nx.Graph(line_graph)

    # Compute the maximal cliques (will be the bags)
    for bag_number, vertex in enumerate(eo.ordering, 1):
        # The clique is formed by a vertex and its neighbors
        clique = [vertex,]
        # We want the neighbors in the order they appear in the eo
        for neighbor in eo.ordering[bag_number-1:]:
            if gr.has_edge(vertex, neighbor):
                clique.append(neighbor)
        td.bags[bag_number] = clique

        # Adds edges for neighbors later in the ordering
        gr.add_edges_from(combinations(gr.neighbors(vertex), 2))

        # Remove the eliminated vertes
        gr.remove_node(vertex)

    print(td.bags)
    # Compute the tree edges
    for bag_number, bag in td.bags.items():
        if len(bag) > 1:
            parents = [key for key in td.bags if td.bags[key][0] == bag[1]]
            print("Adding edge ({}, {})".format(bag_number, parents[0]))
            td.tree.add_edge(bag_number, parents[0])

    return td


def eo_to_conseq(eo, line_map):
    """
    Generates a contraction sequence for the original graph, given a perfect
    elimination ordering for the line graph and a map between line graph
    vertices and original graph edges.
    Input:
        eo (PerfectEliminationOrdering): A perfect elimination ordering for a
        line graph.
        map (dictionary): A map between line graph vertices and original graph
        edges.
    Output:
        conseq (ContractionSequence): An ordering on the edges from the
        original graph.
    """
    conseq = ContractionSequence()
    for vertex in eo.ordering:
        conseq.ordering.append(line_map[vertex])
    return conseq


def conseq_to_eo(conseq, line_map):
    """
    Generates a contraction sequence for the original graph, given a perfect
    elimination ordering for the line graph and a map between line graph
    vertices and original graph edges.
    Input:
        eo (PerfectEliminationOrdering): A perfect elimination ordering for a
        line graph.
        map (dictionary): A map between line graph vertices and original graph
        edges.
    Output:
        conseq (ContractionSequence): An ordering on the edges from the
        original graph.
    """
    eo = PerfectEliminationOrdering()
    # Invert the line map
    inverted_line_map = {}
    for key in line_map:
        inverted_line_map[line_map[key]] = key
    # Map conseq to eo
    for edge in conseq.ordering:
        eo.ordering.append(inverted_line_map[edge])
    return eo


def conseq_to_new_node_conseq(conseq):
    new_node_conseq = ContractionSequence()
    # components will have a label and a list of vertices
    components = {}
    # component_lookup will return which component a vertex belongs to
    component_lookup = {}

    vertices = set()
    for edge in conseq.ordering:
        vertices.update(edge)

    for vertex in vertices:
        components[vertex] = [vertex]
        component_lookup[vertex] = vertex

    new_component_label = max(vertices)
    for edge in conseq.ordering:
        # Look up the latest component labels
        component1 = component_lookup[edge[0]]
        component2 = component_lookup[edge[1]]

        # Continue if this is a self-loop
        if component1 == component2:
            continue

        # Translate the original edge into an edge with these labels
        new_component_label += 1
        new_node_conseq.ordering.append(tuple(sorted([component1,
                                                      component2])))

        # Construct the new component
        new_component = components[component1] + components[component2]

        # Add this new component and remove the two old components
        components[new_component_label] = new_component
        components.pop(component1, None)
        components.pop(component2, None)

        # Update the lookup table
        for vertex in new_component:
            component_lookup[vertex] = new_component_label

    return new_node_conseq


def new_node_conseq_to_conseq(new_node_conseq, graph):
    conseq = ContractionSequence()
    # components will have a label and a list of vertices
    components = {}
    # component_lookup will return which component a vertex belongs to
    component_lookup = {}

    vertices = set(graph.nodes())
    edges_remaining = set()
    for edge in graph.edges():
        edges_remaining.add(tuple(sorted(edge)))

    for vertex in vertices:
        components[vertex] = [vertex]
        component_lookup[vertex] = vertex

    new_component_label = max(vertices)
    for edge in new_node_conseq.ordering:
        # Look up the latest component labels
        component1, component2 = edge

        # Translate the original edge into an edge with these labels
        new_component_label += 1

        for original_edge in product(components[component1],
                                     components[component2]):
            original_edge = tuple(sorted(original_edge))
            if original_edge in edges_remaining:
                conseq.ordering.append(original_edge)
                edges_remaining.remove(original_edge)

        # Construct the new component
        new_component = components[component1] + components[component2]

        # Add this new component and remove the two old components
        components[new_component_label] = new_component
        components.pop(component1, None)
        components.pop(component2, None)

        # Update the lookup table
        for vertex in new_component:
            component_lookup[vertex] = new_component_label

    assert(len(edges_remaining) == 0)
    return conseq
