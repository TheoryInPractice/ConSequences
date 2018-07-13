#!/usr/bin/env python
"""
This file provides a converter for mapping PACE datasets into something
QuickBB can use. See here for more:
http://www.hlt.utdallas.edu/~vgogate/quickbb.html
"""

import argparse
import os

def generate_cnf_dataset(filename):
    """
    Converts a .gr dataset in PACE format to a .cnf file in CNF format.
    """

    line = []
    with open(filename, "r") as infile:
        lines = infile.readlines()

    with open(filename.replace(".line", ".cnf"), "w") as outfile:
        for line in lines:
            if line[0] == "c":
                pass
            elif line[0] == "p":
                outfile.write(line.replace("tw", "cnf"))
            else:
                outfile.write("{} 0\n".format(line.strip()))

def construct_argparser():
    """
    Controls the retrieval of command line arguments using the argparse module.
    """

    parser = argparse.ArgumentParser(description="Adjacency Matrix to PACE args")
    parser.add_argument("filename", type=str, help="Filename of input graph in PACE format")
    return parser

if __name__=="__main__":
    """
    Main CLI for converting an ajacency matrix to a PACE graph.
    """

    args = construct_argparser().parse_args()
    filename = os.path.abspath(args.filename)

    generate_cnf_dataset(filename)
