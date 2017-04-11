

from collections import defaultdict
import Table1_1 as tbl
import pprint


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
    """
    # cherry pick remove 
    def remove_CP(self, node_key, node_ele):
    """

    def cost_join_nl(self, key_node, node):
        return key_node.card*node.card
            
    # clear NonUDFPred: randomly look at
    """
    Three options
    0) default: random blind processing: don't care the order of processing and consider the assoicated 
    1) ascending/descending order of processing (by selectivity)
        - keep to sort by selectivity to process asscending or dscending order
    2) foresee
        - check the associated TMs' expected cardinalities by checking the neighboring selectivity
    3) hybrid of 1) and 2)

    2) 
    """
    
    #### TO-DO: have to update total cost
    def clearNonUDFPred(self, costFunction):
        # to get keys in the graph
        keys = self._graph.keys()
        # apply each predicate to an associated TM with the lowest card
        for key in keys:
            if key.TMbool == False: # have to check as TM does not have 
                key_pred = key.pred
                if key_pred != 1.0:
                    temp = key
                    temp_low = float("inf")
                    for node in self._graph[key]:
                        if temp_low > node.card:
                            temp_low = node.card
                            temp = node
                    temp.card = temp.card*key_pred
                    temp.cum_cost += (key.cum_cost + costFunction(key, temp))
        # delete all normal tables without UDF (UDF not assumed as of 1/4/2017)
        for key in keys:
            temp_list = []
            # 
            for node in self._graph[key]:
                temp_list.append(node)
            if len(temp_list) == 1:
                pass
            else:
                import itertools
                elements = [list(x) for x in itertools.combinations(temp_list, 2)]
                for nodes in elements:
                    # add new connectinos among TMs
                    self.add(nodes[0],nodes[1])
            # delete all normal tables
            del self._graph[key]

    
            
    #### TO-DO: do sophisticated clearing preds check set
            
            
            
            
            
            
            
            
    def snapshot_AllNodes(self):
        # 1) loop all keys and elements and put everything in a set
        # 2) then print all elements
        """ pprint.pprint(vars(tbl_G)) """

        
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

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


###############################
# creates tables
# test: clearning simple predicates
#### ===>> SUCCESS
###############################
A = tbl.Table('A', card=100000, cum_cost=0, pred=1.0)
B = tbl.Table('B', card=100000, cum_cost=0, pred=.2)
C = tbl.Table('C', card=100000, cum_cost=0, pred=1.0)
AB = tbl.TM(table_name='AB', card=1500000, cum_cost=0, LR_tbls= [A, B])
BC = tbl.TM(table_name='BC', card=2000000, cum_cost=0, LR_tbls= [B, C])

A
print A

conn = [(A, AB), (B ,AB), (B ,BC), (C, BC)]
simple_pred = Graph(conn, directed=True)        
pprint.pprint(simple_pred._graph)

simple_pred.clearNonUDFPred(simple_pred.cost_join_nl)
pprint.pprint(simple_pred._graph)

###############################
# creates tables
# test: clearning simple predicates
#### ===>> SUCCESS
###############################
A = tbl.Table('A', card=100000, cum_cost=0, pred=1.0)
B = tbl.Table('B', card=100000, cum_cost=0, pred=.2)
C = tbl.Table('C', card=100000, cum_cost=0, pred=1.0)
AB = tbl.TM(table_name='AB', card=0, cum_cost=0, LR_tbls= [A, B])
BC = tbl.TM(table_name='BC', card=0, cum_cost=0, LR_tbls= [B, C])

conn = [(A, AB), (B ,AB), (B ,BC), (C, BC)]
simple_pred = Graph(conn, directed=True)        
pprint.pprint(simple_pred._graph)

simple_pred.clearNonUDFPred(simple_pred.cost_join_nl)
pprint.pprint(simple_pred._graph)


        
###############################
# creates tables
# test: clearning predicates
###############################
A = tbl.Table('A', card=100000, cum_cost=0, pred=1.0)
B = tbl.Table('B', card=100000, cum_cost=0, pred=.2)
C = tbl.Table('C', card=100000, cum_cost=0, pred=1.0)
D = tbl.Table('D', card=100000, cum_cost=0, pred=.8)
E = tbl.Table('E', card=100000, cum_cost=0, pred=.6)
AB = tbl.TM(table_name='AB', card=0, cum_cost=0, LR_tbls= [A, B])
BC = tbl.TM(table_name='BC', card=0, cum_cost=0, LR_tbls= [B, C])
BD = tbl.TM(table_name='BD', card=0, cum_cost=0, LR_tbls= [B, D])
DE = tbl.TM(table_name='DE', card=0, cum_cost=0, LR_tbls= [D, E])


# make dict 
conn = [(A, AB), (B ,AB), (B ,BC), (B ,BD), (C, BC), (D, BD), (D, DE), (E, DE)]
c = Graph(conn, directed=True)        
pprint.pprint(c._graph)


c.clearNonUDFPred(c.cost_join_nl)

pprint.pprint(c._graph)


"""
pprint.pprint(c._graph)
defaultdict(<type 'set'>, {A: set([B]), B: set([C, D])})

del c._graph[B]

pprint.pprint(c._graph)

defaultdict(<type 'set'>, {A: set([B])})
"""


for n, cxns in c._graph.iteritems():
    print n, cxns

# to make graph dict
dict(c._graph)
c._graph

# to get keys of a graph for looping
c._graph.keys()


print '120'
c._graph

some_dict = c._graph
value_to_remove = 'D'
res = {key: value for key, value in some_dict.items() if value != value_to_remove}
res
c._graph


some_dict = {1: "Hello", 2: "Goodbye", 3: "You say yes", 4: "I say no"}
value_to_remove = "You say yes"
some_dict = {key: value for key, value in some_dict.items() if value is not value_to_remove}
some_dict
some_dict = {key: value for key, value in some_dict.items() if value != value_to_remove}
some_dict

print '137'
c._graph[A]

## test of Master TIM
tbl_G = tbl.Table('G', card = 70, cum_cost=0, pred=1.0)
tbl_UC = tbl.Table('UC', card = 10000, cum_cost=0, pred=1.0)
tm_GaaUC = tbl.TM(table_name='GaaUC', card=7884, cum_cost=0, LR_tbls=[tbl_G, tbl_UC])
tbl_UCS = tbl.Table('UCS', card = 20000, cum_cost=0, pred=1.0)
tm_UCaaUCS = tbl.TM(table_name='UCaaUCS', card = 15838, cum_cost=0, LR_tbls=[tbl_UC, tbl_UCS])
tbl_EC = tbl.Table('EC', card = 10000, cum_cost=0, pred=1.0)
tm_UCSaaEC = tbl.TM(table_name='UCSaaEC', card = 15956, cum_cost=0, LR_tbls=[tbl_UCS, tbl_EC])
tbl_ECS = tbl.Table('ECS', card = 30000, cum_cost=0, pred=1.0)
tm_ECaaECS = tbl.TM(table_name='ECaaECS', card = 23800, cum_cost=0, LR_tbls=[tbl_EC, tbl_ECS])
tbl_CC = tbl.Table('CC', card = 10000, cum_cost=0, pred=1.0)
tm_CCaaUCS = tbl.TM(table_name='CCaaUCS', card = 15809, cum_cost=0, LR_tbls=[tbl_CC, tbl_UCS])
tbl_SCP = tbl.Table('SCP', card = 15000, cum_cost=0, pred=1.0)
tm_CCaaSCP = tbl.TM(table_name='CCaaSCP', card = 11923, cum_cost=0, LR_tbls=[tbl_CC, tbl_SCP])
tbl_CP = tbl.Table('CP', card = 10000, cum_cost=0, pred=1.0)
tm_CPaaSCP = tbl.TM(table_name='CCaaSCP', card = 12042, cum_cost=0, LR_tbls=[tbl_CP, tbl_SCP])
tbl_RQ = tbl.Table('RQ', card = 26, cum_cost=0, pred=1.0)
tm_RQaaCP = tbl.TM(table_name='RQaaCP', card = 7754, cum_cost=0, LR_tbls=[tbl_RQ, tbl_CP])

lis = []
lis.append(tbl_G)
lis.append(tbl_UC)
lis
lis[0] == 'G'
type(lis[0])

mas_conn = [(tbl_G, tm_GaaUC),(tbl_UC, tm_GaaUC), (tbl_UC, tm_UCaaUCS), (tbl_UCS, tm_UCaaUCS), (tbl_UCS, tm_UCSaaEC),
        (tbl_EC, tm_UCSaaEC), (tbl_EC, tm_ECaaECS), (tbl_ECS, tm_ECaaECS), (tbl_CC, tm_CCaaUCS), (tbl_UCS, tm_CCaaUCS),
        (tbl_CC, tm_CCaaSCP), (tbl_SCP, tm_CCaaSCP), (tbl_CP, tm_CPaaSCP), (tbl_SCP, tm_CPaaSCP), (tbl_RQ, tm_RQaaCP),
        (tbl_CP, tm_RQaaCP)]

        
print '164'
# possibly create connection from normal table to trace matrice(s)
master = Graph(mas_conn, directed=True)
pprint.pprint(master._graph)

conn_qry1 = [(tbl_G, tm_GaaUC),(tbl_UC, tm_GaaUC), (tbl_UC, tm_UCaaUCS), (tbl_UCS, tm_UCaaUCS), 
              (tbl_UCS, tm_UCSaaEC), (tbl_EC, tm_UCSaaEC)]
              

              
# tbl and tm distinguishable 
# extract pred conn from query conn
# allocate pred 
# remove all tbls
# process tms

## how can I call an object???

# has to put in a dict set




              
              
print tbl_G
pprint.pprint(vars(tbl_G))

type(tbl_G)

master._graph[tbl_SCP]

dic = dict(c._graph)

dic.keys()
keys = dic.keys()

for key in keys:
    print list(c._graph[key])[0]
    print key

for key in keys:
    print key

pprint.pprint(c._graph)
                   



connections = [('A', 'B'), ('A', 'B'), ('B', 'C'), ('B', 'D'),
                   ('C', 'D'), ('E', 'F'), ('F', 'C')]

g = Graph(connections)
pprint.pprint(g._graph)

type(g._graph)
g._graph.keys()
res = []
for key in g._graph.keys():
    if len(g._graph[key])>1:
        res.append(key)
res

g._graph[res[1]]

g._graph['A']
g._graph['C']



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


"""
        for key in keys:
            # if node_old is a key
            try:                
                nodes = self._graph[node_old]
                for node in nodes:
                    self.add(node_new, node)
            except KeyError:
                pass
"""
