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
    # isomorphism 'subgroup'
    for key in sorted(groups):
        graph_names = groups[key]
        # Subgroups will have a representative and a list of isomorphic graphs
        subgroups = {}

        # Initialize the first graph as its own isomorphism 'subgroup'
        subgroups[0] = [0]

        # For each graph, check if it's isomorphic to a graph from each subgraph
        for i in range(1, len(graph_names)):
            found_subgroup = False
            for j in subgroups:
                if isomorphism_function(graphs[graph_names[i]],
                                        graphs[graph_names[j]]):
                    subgroups[j].append(i)
                    found_subgroup = True
                    break
                if found_subgroup is False:
                    subgroups[i] = [i]
                    break

        for counter, subgroup_root in enumerate(subgroups):
            subgroup_graph_names = sorted([graph_names[x] for x in
                                    subgroups[subgroup_root]])
            representative = subgroup_graph_names[0]

            print("Group: (|V|={}, |E|={}, subgroup={}) \t number: {} \t all_isomorphic: {} \t representative: {}".format(*key, counter, len(subgroup_graph_names), True, representative))

            if not print_headers_only:
                for name in subgroup_graph_names:
                    print("{}".format(name))
