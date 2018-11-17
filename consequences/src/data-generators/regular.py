import networkx as nx


def generate_regular(vertices, regularity, seed, output_dir):
    """
    Uses networkx to generate a graph with the given number of vertices,
    regularyity and seed to the specified output directory.

    Keyword arguments:
    vertices -- number of vertices in the graph
    regularity -- regularity of the graph
    seed -- random seed with which to generate the graph
    output_dir -- output directory of the graph files
    """

    base_filename = "r{}-v{}-s{}.gr".format(regularity, vertices, seed)
    full_output_path = "{}/{}".format(output_dir, base_filename)

    try:
        G = nx.random_regular_graph(regularity, vertices, seed)
        if not nx.is_connected(G):
            raise ValueError("graph not connected")

        fout = open(full_output_path, "w")
        with open(full_output_path, 'w') as fout:
            fout.write("c Regular graph of {} degree and {} nodes."
                       "Seed = {}\n".format(regularity, vertices, seed))
            fout.write("p tw {} {}\n"
                       "".format(vertices, G.number_of_edges()))

            for line in nx.generate_edgelist(G, data=False):
                line = line.split()
                u = int(str(line[0])) + 1
                v = int(str(line[1])) + 1
                fout.write("{} {}\n".format(u, v))
    except Exception:
        pass
