import glob
import itertools
import networkx as nx
import os

from readers import read_pace_to_networkx_graph


def check_isomorphism(directory, exact, print_headers_only):
    """
    In the provided directory, read in all .gr graphs and for those with the
    same order and size, check if they're isomorphic and print a report.
    Input:
        directory (str): Name of directory holding .gr files
        exact (boolean): Exact isomorphism check or not
    Output:
        print summary of isomorphism checks
    """

    # Choose the specified level of isomorphism check
    if exact:
        isomorphism_function = nx.is_isomorphic
    else:
        isomorphism_function = nx.faster_could_be_isomorphic

    # Read all graphs into memory
    graphs = {}
    for file in glob.glob("{}/*.gr".format(directory)):
        graphs[file] = read_pace_to_networkx_graph(file)

    groups = {}
    # Group these graphs by (|V|, |E|)
    for graph_name in graphs:
        graph = graphs[graph_name]
        key = (graph.order(), graph.size())
        groups[key] = groups.get(key, []) + [graph_name]

    # Check if all graphs in a 'group' are isomorphic. If not, create an
    # isomorphism 'eqv_class'
    for key in sorted(groups):
        graph_names = groups[key]
        # eqv_classes will have a representative and a list of isomorphic graphs
        eqv_classes = {}

        # Initialize the first graph as its own isomorphism 'eqv_class'
        eqv_classes[0] = [0]

        # For each graph, check if it's isomorphic to a graph from each subgraph
        for i in range(1, len(graph_names)):
            found_eqv_class = False
            for j in eqv_classes:
                if isomorphism_function(graphs[graph_names[i]],
                                        graphs[graph_names[j]]):
                    eqv_classes[j].append(i)
                    found_eqv_class = True
                    break
                if found_eqv_class is False:
                    eqv_classes[i] = [i]
                    break

        for counter, eqv_class_root in enumerate(eqv_classes):
            eqv_class_graph_names = sorted([graph_names[x] for x in
                                           eqv_classes[eqv_class_root]])
            representative = eqv_class_graph_names[0]

            print("Group: (|V|={}, |E|={}, eqv_class={}) \t number: {} \t all_isomorphic: {} \t representative: {}".format(*key, counter, len(eqv_class_graph_names), True, representative))

            if not print_headers_only:
                for name in eqv_class_graph_names:
                    print("{}".format(name))
