# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 15:34:26 2016

@author: HKIM85
"""

import tim
import Table1_1 as tbl


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
