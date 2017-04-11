from collections import defaultdict


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """
        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None
    
    def substitute(self, node_old, node_new):
        """ Find the node_old in a graph and replace """
        # if node_old is a key
        if node_old in self._graph:
            for node in self._graph[node_old]:
                # key .add(set)
                self._graph[node_new].add(node)
                if not self._directed:
                    self._graph[node].add(node_new)

        keys = self._graph.keys()

        for key in keys:
            # if node_old is an element of a key specified in this loop
            if node_old in self._graph[key]:
                self._graph[key].add(node_new)
                if not self._directed:
                    self._graph[node_new].add(key)
        self.remove(node_old)
        return None

connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),
                   ('C', 'D'), ('E', 'F'), ('F', 'C')]

import pprint

g = Graph(connections)
pprint.pprint(g._graph)

# test: add node ==> SUCCESS
print 'g._graph[B].add(K)'
g._graph['B'].add('K')
pprint.pprint(g._graph)

# test: remove node ==> SUCCESS
print ''
print 'g.remove(K)'
g.remove('K')
pprint.pprint(g._graph)

# test: substitute node with new node ==> SUCCESS
print ''
print 'g.substitute(A,I)'
g.substitute('A','I')
pprint.pprint(g._graph)

# test: substitute node with new node ==> SUCCESS
print ''
print 'g.substitute(B,K)'
g.substitute('B','K')
pprint.pprint(g._graph)
