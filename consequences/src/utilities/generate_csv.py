"""
This file creates a .csv by scraping a directory that contains a collection
of .td files.
"""

import argparse
import glob
import os
from os.path import basename


def append_to_csv(regularity, vertices, treewidth, algorithm, valid):
    """
    Appends information on regularity, vertices, treewidth, algorithm and
    validity to the .csv

    Keyword arguments:
    regularity -- regularity of the .gr graph
    vertices -- number of vertices in the .gr graph
    treewidth -- treewidth from the .td
    algorithm -- algorithm used to get .td
    valid -- true if the tree decomposition was valid for its graph
    """

    if valid:
        csv.write("{},{},{},{}\n".format(regularity, vertices,
                                         treewidth, algorithm))
    else:
        csv.write("{},{},{},{}\n".format(regularity, vertices,
                                         float('nan'), algorithm))


def construct_argparser():
    """
    Controls the retrieval of command line arguments using the argparse module.
    """

    parser = argparse.ArgumentParser(description="Generating a .csv "
                                     "from .td files")
    parser.add_argument("input_dir", type=str, help="input directory "
                        "of .td files")
    parser.add_argument("csv_filename", type=str, help="output file of .csv")
    return parser


def get_data(td_filename, gr_filename):
    """
    Collects the regularity, vertices, treewidth and algorithms from the
    tree decompositions and graph files.

    Keyword arguments:
    td_filename -- filename of tree decomposition
    gr_filename -- filename of .gr file
    """
    valid = True
    with open(td_filename) as f:
        content = f.readlines()

    tw = float('nan')
    for line in content:
        if(line.startswith("c invalid")):

            valid = False

        if line.startswith("s"):
            tw = line.split(" ")[3]
            tw = int(tw) - 1

    with open(gr_filename) as f:
        content = f.readlines()

    for line in content:
        if line.startswith("p"):
            vertices = line.split(" ")[2]

    regularity = basename(gr_filename).split("-")[0]
    tokens = list(regularity)
    del(tokens[0])
    regularity = "".join(tokens)

    td_split_name = basename(td_filename).split("-")
    tokens = list(td_split_name)
    del(tokens[0])
    del(tokens[0])
    del(tokens[0])
    algo_with_extension = "-".join(tokens)
    algorithm = algo_with_extension.split(".")[0]

    append_to_csv(regularity, vertices, tw, algorithm, valid)


if __name__ == "__main__":
    """
    Main CLI for creating a .csv from .td files
    """
    args = construct_argparser().parse_args()

    csv = open(args.csv_filename, "w")
    csv.write("regularity,vertices,treewidth,algorithm\n")

    td_files = glob.glob(args.input_dir + "/*.td")
    gr_files = glob.glob(args.input_dir + "/*.gr")

    print ("Creating csv...")

    for tree_decomposition in td_files:
        # retrieve appropriate .gr filename by removing -[algorithm].td
        filename = os.path.splitext(tree_decomposition)[0]

        td_name = basename(filename).split("-")
        graph_name = "{}-{}-{}".format(td_name[0], td_name[1], td_name[2])
        graph_name = "{}.gr".format(filename.replace(basename(filename),
                                    graph_name))

        # send filenames to get_data()
        get_data(tree_decomposition, graph_name)

    print (".csv created\n")
