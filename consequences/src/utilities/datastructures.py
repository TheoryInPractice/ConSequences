"""
datastructures.py

A collection of structures for storing data.
"""

import networkx as nx


class TreeDecomposition:
    """
    A named struct for convenience.
    """
    def __init__(self):
        """
        A tree decomposition consisting of a tree of nodes and a lookup table
        mapping decomposition nodes to vertices in the original graph.
        """
        self.tree = nx.Graph()
        self.bags = {}


class EliminationOrdering:
    """
    A named struct for convenience.
    """
    def __init__(self):
        """
        A elimination ordering is an ordered list of vertices.
        """
        self.ordering = []


class ContractionSequence:
    """
    A named struct for convenience.
    """
    def __init__(self):
        """
        A contraction sequence is an ordered list of vertices
        """
        self.ordering = []


class LegLinks:
    """
    A named struct for convenience.
    """
    def __init__(self):
        """
        A colleciton of leg links is a list of labeled edges associated with
        each vertex, represented in a dictionary.
        """
        self.incident_edges = {}

    def __repr__(self):
        """
        Return leglinks in a str importable into MATLAB.
        """
        return '{' + ' '.join(map(lambda key: '{},'.format(
            self.incident_edges[key]), self.incident_edges))[:-1] + '}'
