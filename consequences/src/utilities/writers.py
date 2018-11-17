"""
writers.py

A collection of functions for writing data.
"""


def write_networkx_graph(graph, filename):
    """
    Writes a NetworkX graph to a file in PACE format.
    Input:
        graph (NetworkX Graph): The graph
        filename (str): The output filename
    Output:
        The graph is written to filename
    """
    pass


def write_leglinks(leglinks, filename):
    """
    Writes leglinks to a file.
    Input:
        leglinks (dict of list): A lookup table that maps each vertex to a list
        of its incident edges.
    Output:
        The file where the leglinks are written.
    """
    with open(filename, 'w') as outfile:
        for key in sorted(leglinks.incident_edges.keys()):
            outfile.write(str(leglinks.incident_edges[key])[1:-1] + '\n')


def write_eo(eo, filename):
    """
    Writes eo to a file.
    Input:
        eo (EliminationOrdering): An elimination ordering object.
    Output:
        The file where the eo is written.
    """

    with open(filename, 'w') as outfile:
        for node in eo.ordering:
            outfile.write('{}\n'.format(node))


def write_conseq(conseq, filename):
    """
    Writes a contraction sequence to a file.
    Input:
        conseq (ContractionSequence): A contraction sequence.
    Output:
        The file where the conseq is written.
    """
    with open(filename, 'w') as outfile:
        for edge in conseq.ordering:
            outfile.write('{} {}\n'.format(*edge))


def write_td(td, filename):
    with open(filename, 'w') as outfile:
        # Write header
        num_bags = len(td.bags)
        max_bag_size = max(len(bag) for bag in td.bags.values())
        vertices = set()
        for bag in td.bags.values():
            vertices.update(bag)
        num_vertices = len(vertices)
        outfile.write('s td {} {} {}\n'.format(num_bags,
                                               max_bag_size,
                                               num_vertices))
        # Write bags
        for key in sorted(td.bags.keys()):
            outfile.write('b {} '.format(key) + ' '.join(
                map(str, sorted(td.bags[key]))) + '\n')

        # Write edges
        for edge in sorted(td.tree.edges()):
            outfile.write('{} {}\n'.format(*edge))
