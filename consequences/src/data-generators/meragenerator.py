import itertools
from mera import MERA, MERA_1d_2ary, MERA_2d_4ary

class MERAGenerator:
    """
    Generates MERAs.
    """

    @staticmethod
    def generate(dim, k, levels, num_inputs, io_nodes, verbose=False):
        # Giant switch for all options
        print(dim, k)
        if dim == 1 and k == 2:
            mera = MERA_1d_2ary(levels, num_inputs, io_nodes)
        elif dim == 2 and k == 4:
            mera = MERA_2d_4ary(levels, num_inputs, io_nodes)
        else:
            print("Coming never!")
            raise()

        mera.generate(verbose)
        return mera

    @staticmethod
    def reduce(mera, operators, verbose=False):
        # Compute a lookup table denoting whether a vertex is in the causal cone
        cone_lookup = MERAGenerator._compute_causal_cone(
            mera, operators, verbose)
        # Reduce a graph based on its causal cone and return
        return MERAGenerator._reduce_mera(mera, cone_lookup, verbose)

    @staticmethod
    def _compute_causal_cone(mera, operators, verbose=False):
        """
            Input:
                mera - MERA fabric
                operators - set of operators placed in graph
            Output:
                Set of vertices in causal cone
        """

        cone_lookup = set()

        current_level = 0
        current_nodes = set(["operator_0_{}".format(x) for x in operators])

        if verbose:
            print("Level {} nodes: {}".format(current_level, current_nodes))

        # Compute causal cone for positive levels
        while current_nodes:
            # Increase the level we're currently examining
            current_level += 1

            # Find the nodes who are (a) neighbors of the current_nodes and (b)
            # contain _[level]_ in their names.

            # Find the next level of unitaries
            cone_lookup.update(current_nodes)
            current_nodes = [list(filter(
                lambda x: "_{}_".format(current_level) in x,
                mera.graph.neighbors(node))) for node in current_nodes]
            current_nodes = set(itertools.chain.from_iterable(current_nodes))
            if verbose:
                print("Level {} unitaries: {}".format(
                    current_level, current_nodes))

            # Find the next level of isometries
            cone_lookup.update(current_nodes)
            current_nodes = [list(filter(
                lambda x: "_{}_".format(current_level) in x,
                mera.graph.neighbors(node))) for node in current_nodes]
            current_nodes = set(itertools.chain.from_iterable(current_nodes))
            if verbose:
                print("Level {} isometries: {}".format(
                    current_level, current_nodes))

        # Add the complement unitaries/isometries from the negative levels
        cone_lookup.update(
            ["{}_-{}_{}".format(*node.split("_")) for node in filter(lambda x:
             "isometry" in x or "unitary" in x, cone_lookup)])

        # Add bottom if it exists
        tops = set(filter(lambda node: 'top' in node, cone_lookup))
        if tops:
            top = tops.pop()
            bottom_location = top.split('_')[-1]
            cone_lookup.add("bottom_-{}_{}".format(mera.levels + 1,
                                                   bottom_location))
        return cone_lookup

    @staticmethod
    def _reduce_mera(mera, cone_lookup, verbose=False):
        """
            Input:
                lookup - set of vertices in causal cone
                graph - MERA fabric
            Output:
                Reduced MERA graph
        """

        nodes_to_remove = []
        for node in mera.graph.nodes():
            # for each node, check if it is in the lookup set
            if node not in cone_lookup:
                # If in set: do nothing
                # If not in set: delete from graph, if parent is in lookup

                # Remove this non-causal-cone node from the graph
                nodes_to_remove.append(node)

                # Compute the level of the current node
                level = int(node.split("_")[1])

                if level < 0:
                    continue

                # Compute the correct level for the parents
                if 'unitary' in node:
                    parent_level = level
                else:
                    parent_level = level + 1

                # Add edge from parents-in-cone to their complement
                parents = list(filter(
                    lambda x: parent_level == int(x.split("_")[1]),
                    mera.graph.neighbors(node)))

                for parent in parents:
                    if parent in cone_lookup:
                        # For any parent that isn't top
                        if 'top' in parent:
                            continue
                        parent_complement = "{}_-{}_{}".format(*parent.split("_"))
                        print("Adding edge ({}, {})".format(parent, parent_complement))
                        mera.graph.add_edge(parent, parent_complement)

                        if verbose:
                            print("Added causal cone edge ({}, {})".format(
                                parent, parent_complement))


        # Return the final tensor network
        mera.graph.remove_nodes_from(nodes_to_remove)
        return mera

if __name__=='__main__':
    levels_list = range(2,7)
    num_inputs_list = range(2,4)
    for levels, num_inputs in itertools.product(levels_list, num_inputs_list):
        # Generate fabric
        mera = MERAGenerator.generate(2, 4, levels, num_inputs, True)

        # Select operators
        operators = set()
        operators.add('0-0')

        mera = MERAGenerator.reduce(mera, operators)

        MERA.write_gr(mera, 'new2d/l{}_n{}.gr'.format(levels, num_inputs))
        MERA.write_gr(mera,
                      'new2d/l{}_n{}_int.gr'.format(levels, num_inputs),
                      int_labels=True)
