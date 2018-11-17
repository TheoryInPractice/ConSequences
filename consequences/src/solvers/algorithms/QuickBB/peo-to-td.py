#!/usr/bin/env python

import os
import argparse


def generate_td(eo_filename, cnf_filename, td_filename):
    fout = open(td_filename, "w")

    # get last line of .eo file
    last_line = ""
    with open(eo_filename, "r") as infile:
        lines = infile.readlines()
        for line in lines:
            if 'Treewidth' not in line:
                last_line = line.strip()

    # print (last_line)
    # get neighborhood dictionary
    with open(cnf_filename, "r") as infile:
        lines = infile.readlines()
        for line in lines:
            if "p cnf " in line:
                vertices = line.split()[2]

        # Hacky fix: QuickBB doesn't always provide a complete eo, so we need
        # to pad it with the missing vertices
        eo_values = list(map(int, last_line.split()))
        for vertex in range(1, int(vertices) + 1):
            if vertex not in eo_values:
                eo_values.append(vertex)

        neighborhood_list = [[] for i in range(int(vertices) + 1)]
        # print (len(neighborhood_list))

        for line in lines:
            if "p cnf " not in line:
                line = line.split()
                neighborhood_list[int(line[0])].append(int(line[1]))
                neighborhood_list[int(line[1])].append(int(line[0]))

        # for index in enumerate(neighborhood_list):
        #     # print ("{}: ".format(index))

    # get bags
    bag_list = [[]]
    #eo_values = last_line.split()
    for target in eo_values:
        bag_contents = []
        bag_contents.append(int(target))
        # for target_neighbor in neighborhood_list[int(value)]:
        # for each target in the eo, check if each value later in the eo is a
        # neighbor of the target.  if so, add to bag
        later = False
        for value in eo_values:
            if int(value) == int(target):
                later = True
            if later:
                # check if value is in target's neighbor list
                if int(value) in neighborhood_list[int(target)]:
                    bag_contents.append(int(value))

        # print ("Start Bag ***************************")
        # print (bag_contents)
        import itertools
        pairs = itertools.combinations(bag_contents, 2)
        for pair in pairs:
            # print(pair)
            # for every pair, add pair[0] to neighborhood_list[1]
            # if pair[0] not in neighborhood_list[1]
            # print ("Looking at N({})".format(pair[1]))
            # print ("Before:", neighborhood_list[pair[1]])
            # print ("Is {} in N({})?".format(pair[0], pair[1]))
            if pair[0] not in neighborhood_list[pair[1]]:
                neighborhood_list[pair[1]].append(pair[0])
            if pair[1] not in neighborhood_list[pair[0]]:
                neighborhood_list[pair[0]].append(pair[1])

            # print ("After:", neighborhood_list[pair[1]])

        bag_list.append(bag_contents)
    # print(bag_list)

    # print (neighborhood_list)
    # create edge list
    edge_list = []
    for index, bag in enumerate(bag_list):
        # print (bag_list[index])
        if len(bag) > 1:
            # print (bag[1])
            for index2, search_bag in enumerate(bag_list):
                # print("** Looking for {} in {}".format(bag[1], search_bag))
                if len(search_bag) > 0:
                    if search_bag[0] == bag[1]:
                        edge_list.append("{} {}".format(index, index2))
                        break
    # get tw
    tw = 0
    for bag in bag_list:
        if(len(bag) > tw):
            tw = len(bag)

    fout.write("s td {} {} {}\n".format(len(bag_list) - 1, tw,
               len(bag_list) - 1))
    for index, bag in enumerate(bag_list):
        if index != 0:
            fout.write("b {} ".format(index))
            for thing in bag:
                fout.write("{} ".format(str(thing)))
            fout.write("\n")
    for edge in edge_list:
        fout.write(edge)
        fout.write("\n")

def construct_argparser():
    """
    Controls the retrieval of command line arguments using the argparse module.
    """

    parser = argparse.ArgumentParser(description="Elimination ordering to tree decomposition")
    parser.add_argument("eo_filename", type=str, help="Filename of input graph eo format (.eo)")
    parser.add_argument("cnf_filename", type=str, help="Filename of the cnf graph (.cnf)")
    return parser


if __name__ == "__main__":
    """
    Main CLI for converting an ajacency matrix to a PACE graph.
    """

    args = construct_argparser().parse_args()
    eo_filename = os.path.abspath(args.eo_filename)
    cnf_filename = os.path.abspath(args.cnf_filename)
    td_filename = eo_filename.replace(".eo", ".td")

    generate_td(eo_filename, cnf_filename, td_filename)
