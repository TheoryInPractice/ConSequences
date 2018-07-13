"""
A collection of MERA fabric generators.
"""
import networkx as nx
from itertools import chain, product

class MERA:
    def __init__(self, dim, k, levels, num_inputs, io_nodes):
        self.graph = nx.MultiGraph()
        self.dim = dim
        self.k = k
        self.levels = levels
        self.num_inputs = num_inputs
        self.io_nodes = io_nodes

    def generate(self):
        pass

    def _add_next_level(self):
        pass

    def _add_negative_levels(self, verbose=False):
        bottom_nodes = [MERA.compute_complement(node)
                        for node in self.graph.nodes()]
        bottom_edges = [(MERA.compute_complement(edge[0]),
                         MERA.compute_complement(edge[1]))
                        for edge in self.graph.edges()]
        bottom_nodes = [node for node in bottom_nodes if 'top' not in node]
        bottom_edges = [edge for edge in bottom_edges if 'top' not in edge[0]
                        and 'top' not in edge[1]]
        self.graph.add_nodes_from(bottom_nodes)
        self.graph.add_edges_from(bottom_edges)

    def _add_io_nodes(self):
        pass

    @staticmethod
    def compute_complement(node_name):
        """
        Converts isometry or unitary to its negative level complement.
        """
        return "{}_-{}_{}".format(*node_name.split("_"))

    @staticmethod
    def print_mera_fabric(mera, verbose=False):
        nodes = list(mera.graph.nodes())

        # Print the top if it exists
        if mera.io_nodes:
            print('----- Level {} ------'.format(mera.levels+1))
            print(list(filter(lambda x: "top" in x, mera.graph.nodes())))

        # Print each level above 0
        for level in range(mera.levels, 0, -1):
            isometries = list(filter(
                lambda node: 'isometry_{}'.format(level) in node, nodes))
            unitaries = list(filter(
                lambda node: 'unitary_{}'.format(level) in node, nodes))

            print('----- Level {} ------'.format(level))

            if verbose:
                print('Isometries: {} ({})'.format(len(isometries),
                                                   isometries))
                print('Unitaries : {} ({})'.format(len(unitaries), unitaries))
                edges = mera.graph.subgraph(unitaries + isometries).edges()
                print('Edges: {}'.format(edges))
            else:
                print('Isometries: {}'.format(len(isometries)))
                print('Unitaries : {}'.format(len(unitaries)))

        # Print level 0
        operators = list(filter(lambda node: 'operator' in node, nodes))
        print('----- Level 0 ------')
        if verbose:
            print('Operator inputs: {} ({})'.format(len(operators), operators))
        else:
            print('Operator inputs: {}'.format(len(operators)))
        print('----- Level 0 ------')

        # Print each level above 0
        for level in range(-1, -1 * (mera.levels+1), -1):
            unitaries = sorted(list(filter(
                lambda node: 'unitary_{}'.format(level) in node, nodes)))
            isometries = sorted(list(filter(
                lambda node: 'isometry_{}'.format(level) in node, nodes)))

            if verbose:
                print('Unitaries : {} ({})'.format(len(unitaries), unitaries))
                print('Isometries: {} ({})'.format(len(isometries),
                                                   isometries))
                edges = mera.graph.subgraph(unitaries + isometries).edges()
                print('Edges: {}'.format(edges))
            else:
                print('Unitaries : {}'.format(len(unitaries)))
                print('Isometries: {}'.format(len(isometries)))

            print('----- Level {} -----'.format(level))

        # Print the bottom if it exists
        if mera.io_nodes:
            print(list(filter(lambda x: "bottom" in x, mera.graph.nodes())))
            print('----- Level {} -----'.format(0-mera.levels-1))

    @staticmethod
    def write_gr(mera, gr_filename, int_labels=False):
        print("Writing to: {}".format(gr_filename))
        if int_labels:
            mera.graph = nx.convert_node_labels_to_integers(
                mera.graph, first_label=1, ordering="sorted")
        with open(gr_filename, "w") as fout:
            #  dim, k, levels, num_inputs, io_nodes
            header = ("c MERA graph dim={} k={} levels={} num_inputs={}" +
                      " io_nodes={}\n")
            fout.write(header.format(
                mera.dim, mera.k, mera.levels,
                mera.num_inputs, mera.io_nodes))
            fout.write("p tw {} {}\n".format(
                mera.graph.order(), mera.graph.size()))

            # Sort the order of items in edges, then sort the edges
            edges = sorted([sorted(edge) for edge in mera.graph.edges()])
            # Write the sorted edges
            for edge in edges:
                fout.write("{} {}\n".format(*edge))


class MERA_1d_2ary(MERA):
    def __init__(self, levels, num_inputs, io_nodes):
        super().__init__(1, 2, levels, num_inputs, io_nodes)

    def generate(self, verbose=False):
        # TODO: Generalize for io_nodes == False
        if self.io_nodes is True:
            inputs = ['top_{}_0'.format(self.levels + 1)] * self.num_inputs
        else:
            print('io_nodes == False not supported yet')
            raise()

        # Add levels from self.levels to 1
        for level in range(self.levels, 0, -1):
            inputs = self._add_next_level(inputs, level, verbose)

        # Add levels from -self.levels to -1
        self._add_negative_levels(verbose)

        # Add level 0
        self._add_operators(inputs, verbose)

        # Add io_nodes
        self._add_io_nodes(verbose)

    def _add_next_level(self, inputs, level, verbose=False):
        """
        Add to self.graph the next level of isometries and unitaries.
        """
        # Add next level of isometries
        for index in range(len(inputs)):
            name = "isometry_{}_{}".format(level, index)
            self.graph.add_node(name)
            if verbose:
                print("Added iso: {}".format(name))
            parent = inputs[index]
            self.graph.add_edge(name, parent)
            if verbose:
                print("Added edge from {} to {}".format(name, parent))

        # Add next level of unitaries and output
        output = []
        for index in range(len(inputs)):
            name = "unitary_{}_{}".format(level, index)
            # Add the unitary's two legs
            output.append(name)
            output.append(name)
            self.graph.add_node(name)
            if verbose:
                print("Added uni: {}".format(name))
            # Add edges to parents
            for parent_at_number in range(0, 2):
                parent = "isometry_{}_{}".format(
                    level, (index + parent_at_number) % len(inputs))
                self.graph.add_edge(name, parent)
                if verbose:
                    print("Added edge from {} to {}".format(name, parent))

        return output

    def _add_operators(self, inputs, verbose=False):
        # Add operator node positions
        for index in range(len(inputs)):
            # Add the operator node
            name = "operator_0_{}".format(index)
            self.graph.add_node(name)
            if verbose:
                print("Added operator: {}".format(name))

            # Add the operator edges
            parent = inputs[index]
            for neighbor in [parent, MERA.compute_complement(parent)]:
                self.graph.add_edge(name, neighbor)
                if verbose:
                    print("Added edge from {} to {}".format(name, neighbor))

    def _add_io_nodes(self, verbose=False):
        # Return if not applicable
        if not self.io_nodes:
            if verbose:
                print("I/O Nodes not added")
            return

        # Add io nodes
        top = 'top_{}_0'.format(self.levels + 1)
        bottom = 'bottom_-{}_0'.format(self.levels + 1)
        for name in [top, bottom]:
            self.graph.add_node(name)
            if verbose:
                print("Added {}".format(name))
        self.graph.add_edge(top, bottom)
        if verbose:
            print("Added edge ({}, {})".format(top, bottom))

        # Adding edges from top to the top level of isometries
        bottom_isometries = sorted(list(filter(
            lambda node: 'isometry_-{}'.format(self.levels) in node,
            self.graph.nodes())))

        for node in bottom_isometries:
            self.graph.add_edge(bottom, node)

    def test(self):
        MERA.print_mera_fabric(mera)


class MERA_2d_4ary(MERA):
    def __init__(self, levels, num_inputs, io_nodes):
        super().__init__(2, 4, levels, num_inputs, io_nodes)

    def generate(self, verbose=False):
        # TODO: Generalize for io_nodes == False
        if self.io_nodes is True:
            inputs = []
            for row in range(self.num_inputs):
                inputs.append(
                    ['top_{}_0-0'.format(self.levels + 1)] * self.num_inputs)
        else:
            print('io_nodes == False not supported yet')
            raise()

        # Add levels from self.levels to 1
        for level in range(self.levels, 0, -1):
            inputs = self._add_next_level(inputs, level, verbose)

        # Add levels from -self.levels to -1
        self._add_negative_levels(verbose)

        # Add level 0
        self._add_operators(inputs, verbose)

        # Add io_nodes
        self._add_io_nodes(verbose)

    def _add_next_level(self, inputs, level, verbose=False):
        """
        Add to self.graph the next level of isometries and unitaries.
        """

        # Define the number of rows and cols in our "rows x cols" grid of inputs
        # Assumes a rectangle
        rows = len(inputs)
        cols = len(inputs[0])

        # Add next level of isometries
        for i_index, j_index in product(range(rows), range(cols)):
            name = "isometry_{}_{}-{}".format(level, i_index, j_index)
            self.graph.add_node(name)
            if verbose:
                print("Added iso: {}".format(name))
            parent = inputs[i_index][j_index]
            self.graph.add_edge(name, parent)
            if verbose:
                print("Added edge from {} to {}".format(name, parent))

        # Add next level of unitaries
        for i_index, j_index in product(range(rows), range(cols)):
            name = "unitary_{}_{}-{}".format(level, i_index, j_index)
            self.graph.add_node(name)
            if verbose:
                print("Added uni: {}".format(name))
            # Add edges to parents
            for parent_shift in product(range(0, 2), range(0, 2)):
                parent = "isometry_{}_{}-{}".format(level,
                    (i_index + parent_shift[0]) % rows,
                    (j_index + parent_shift[1]) % cols)
                self.graph.add_edge(name, parent)
                if verbose:
                    print("Added edge from {} to {}".format(name, parent))

        # compute and return output
        output = []
        i_indices = [0]
        i_indices += list(chain(*[[i] + [i] for i in range(1, rows)]))
        i_indices += [0]

        j_indices = [0]
        j_indices += list(chain(*[[i] + [i] for i in range(1, cols)]))
        j_indices += [0]

        for i_index in i_indices:
            output.append(['unitary_{}_{}-{}'.format(level, i_index, j_index)
                           for j_index in j_indices])
        return output

    def _add_operators(self, inputs, verbose=False):
        # Define the number of rows and cols in our "rows x cols" grid of inputs
        # Assumes a rectangle
        rows = len(inputs)
        cols = len(inputs[0])

        # Add operator node positions
        for i_index, j_index in product(range(rows), range(cols)):
            # Add the operator node
            name = "operator_0_{}-{}".format(i_index, j_index)
            self.graph.add_node(name)
            if verbose:
                print("Added operator: {}".format(name))

            # Add the operator edges
            parent = inputs[i_index][j_index]
            for neighbor in [parent, MERA.compute_complement(parent)]:
                self.graph.add_edge(name, neighbor)
                if verbose:
                    print("Added edge from {} to {}".format(name, neighbor))

    def _add_io_nodes(self, verbose=False):
        # Return if not applicable
        if not self.io_nodes:
            if verbose:
                print("I/O Nodes not added")
            return

        # Add io nodes
        top = 'top_{}_0-0'.format(self.levels + 1)
        bottom = 'bottom_-{}_0-0'.format(self.levels + 1)
        for name in [top, bottom]:
            self.graph.add_node(name)
            if verbose:
                print("Added {}".format(name))
        self.graph.add_edge(top, bottom)
        if verbose:
            print("Added edge ({}, {})".format(top, bottom))

        # Adding edges from top to the top level of isometries
        bottom_isometries = sorted(list(filter(
            lambda node: 'isometry_-{}'.format(self.levels) in node,
            self.graph.nodes())))

        for node in bottom_isometries:
            self.graph.add_edge(bottom, node)

    def test(self):
        inputs = [['input_42_0-0', 'input_42_0-1'],
                  ['input_42_1-0', 'input_42_1-1']]
        verbose = True
        for level in range(2, 0, -1):
            inputs = self._add_next_level(inputs, level, verbose)
            print("Next inputs:", inputs)


if __name__ == '__main__':
    mera = MERA_2d_4ary(levels=4, num_inputs=2, io_nodes=True)
    mera.generate(verbose=True)
    mera.write_gr(mera, 'mera_2d_test.gr', int_labels=False)
