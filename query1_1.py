

from collections import defaultdict
import Table1_1 as tbl
import predicate as pds
import Fanout as fo
import microJU as mju
import copy
#import pprint


"""
01/23/17) assuming there is no UDF predicates
0) UDF predicates may be on the same table: then we need to deal with this 
1) at this moment, we don't deal with this
2) non UDF predicates on the same table may be integrated as one predicate
"""

"""
TO-DO
1) this class may have to be pruned that only necessary method may be kept
2) may find a better library or class to do 

3))) query stack???
"""

class Query(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False, isVK = False):
        self._graph = defaultdict(set) # must update _graph_vk whenever update _graph
        self._directed = directed
        self.add_connections(connections)
        if (isVK == False): self.query_vk = self.swapKeyVal()
        self.update_fanouts(connections)
        self.mJUhstry = mju.MicroJUlist(microJUlist = [], excldShort = True)
        """ mJUhstry keeps a path for query execution: mJU carries proxy stats for tbls """
        """ having a swapped grpah may not be a good idea as this may not be the up-to-date"""

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """
        
        for node1, node2 in connections:
            self.add(node1, node2)
        
        
    def update_fanouts(self, connections):
        """ update all fanouts and then assign those to each TM accordingly """

        fanouts = fo.Fanouts()
        conn = copy.deepcopy(connections)
        fanouts.add_connections(conn)
        # does not create a fanout when key is TM (swapKeyVal)
        if self.getFstKey().getTMbool() == False: 
            for TM in self.getAllValues():
                for tbl_tmp in self.query_vk._graph[TM]:
                    for fanout in fanouts._graph[tbl_tmp]:
                        TM.addFO(fanout)
        
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
    
    def getKeys(self):
        return self._graph.keys()
    
    def getRelTbl(self, TM):
        return self._graph_vk[TM] 
    
    def getFstKey(self):
        return self._graph.items()[0][0]
        
    def getQueryGraph(self):
        return self._graph
    
    def getQuery_vk(self):
        return self.query_vk
        
    def concatKeyNames(self):
        temp = []
        for key in self._graph:
            temp.append(key.getTableName())
        return '_'.join(temp)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            """ Keys are not empty and values are not empty """
            is_equal = True
            # key comparision
            self_keys = self.getKeys()
            self_keys.sort(key=lambda node: node.table_name)
            theO_keys = other.getKeys()
            theO_keys.sort(key=lambda node: node.table_name)
            if self_keys != theO_keys: is_equal = False
            
            # value comparison
            for self_key, theO_key in zip(self_keys, theO_keys):
                self_values = list(self._graph[self_key])
                self_values.sort(key=lambda node: node.table_name)
                other_values = list(other._graph[theO_key])
                other_values.sort(key=lambda node: node.table_name)
                if (self_values != other_values): is_equal = False
            return is_equal
        else: return False
            

    def getValues(self, key):
        return self._graph[key]

    def get_AllNodes_set(self):
        allNodes = set([])    
        #allNodes = self.getKeys()
        for key in self._graph:
            allNodes.add(key)
            for node in self._graph[key]:
                allNodes.add(node)
        return allNodes
        
    def get_AllNodes(self):
        allNodes = set([])    
        #allNodes = self.getKeys()
        for key in self._graph:
            allNodes.add(key)
            for node in self._graph[key]:
                allNodes.add(node)
        return sorted(list(allNodes), key=lambda node: node.table_name)
        
    def getAllValues(self):
        """ input  : query object """
        """ output : TM Set """
        temp = set([])
        for key in self._graph:
            temp = temp.union(self.getValues(key))
        return temp
    
    def swapKeyVal(self):
        """ input query object """
        """ swap key-value pair """
        conn = [(val,key) for key in self._graph for val in self._graph[key]]
        return Query(conn, directed=True, isVK = True)
    
    def displayFOs(query):
        for TM in query.getAllValues():
            print TM.fanouts
    
    def splitToNano(self):
        """ input: MicroQuery """
        """ output: two nanoquery """
        """self."""
    
    def microOpt(self):
        sub_qry1, subqry2 = self.splitToNano()
    
    # find all normal preds in a table and update card and sel
#    def clear_mult_norm_pred(self):
#        keys = self._graph.keys()
#        nodesW_multPreds = [node for node in keys if node.has_mult_normPred()]
#        nodesW_multPreds.sort(key = lambda pred: pred.)
#        for node in nodesW_multPreds:
#            node.
     
    """ COMPLETE this function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! URGENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    allNodes = self.get_AllNodes()
    nodesW_multPreds = [node for node in allNodes if node.has_mult_normPred()]
    
    processNorm_preds(self): @ Table1_1.py
    """        
    def processPredicate(self, tbls, TM, cost_join):
        """ input: set of tbls// TM
            output: TM, associated tbls get updated """
        """ TO-DO: should work on UDF predicate as well """
        #if(any(tbl for tbl in tbls if tbl.has_UDFPred())):
        """ should deal with the UDF_Pred """
        tbls_list = list(tbls)
        tbls_list.sort(key = lambda tbl: tbl.getNormPreds().getProdNormSel())
        for tbl_ in tbls_list:
            tbl_.processNorm_preds() # aggregates multiple norm predicates into on
            TM.addCum_cost(tbl_.getCum_cost()) # update all cost to a target TM
            tbl_.resetCum_cost() # reset tbl cost to 0
            """ ATTENTION: support various join methods"""
            TM.addCum_cost(cost_join(tbl_, TM)) # estimate cost of join and addCum
            TM.updateCard(tbl_.getNormPreds().getProdNormSel()) # has to update after process
            """ TM.cum_cost += tbl.cum_cost
            tbl.cum_cost = 0
            TM.cum_cost += join_cost(tbls, TM)
            TM.card = TM.card*tbl.getNormPreds().getProdNormSel()
            """
            
    def div_int_lf_rg(self):
        """ input: two TMs and related tables """
        leftTbls = self._graph.items()[0][1]
        rightTbls = self._graph.items()[1][1]
        intersection = leftTbls.intersection(rightTbls)
        left = leftTbls.difference(intersection)
        right = rightTbls.difference(intersection)
        """ left: normal tables exclusive to left TM """
        """ output left == right: sets of normal tables, leftTM, rightTM """
        return left, intersection, right, self._graph.items()[0][0], self._graph.items()[1][0]
        """ each set of normal tables may not be more than one as TM_cluster """    

    def cost_join_nl(self, key_node, node):
        return key_node.card*node.card
        
    def nano_opt(self, cost_join):
        import copy
        """ input: nano query + self.cost_join_[method]"""
        """ ouput TM_cluster and associated tbls """
        
        """ optimization for 3+a tbls and 2 TMs """
        """ two scheme: lowest (and lower) cardinality, lowestet selectivity """
        """ choose lowest total SELECTIVITY in this method """
        """ distinguish of right and left does not matter """
        
        """ TO-DO: right now each tables has one pred in preds but has to 
        work with multiple tables with multiple preds """
        """ However, it would not be efficient to process all preds at every option """
        """ for display all path purpose: yes, we should do all preds processing dynamically """
        """ So, deepcopy of query would be the one with all multiple preds in preds """
        """ for optimization: no, we don't have to process all preds at every deep copies """
        query_dc = copy.deepcopy(self)
    
        query_dc_vk = query_dc.swapKeyVal() # same table object
        lfOnly, intersection, rghOnly, leftTM, rightTM = self.div_int_lf_rg(query_dc_vk)
        """ output: lfOnly, intersection, rghOnly:set of tbls; leftTM, rightTM: TM """
        """ TO-DO: write processPredicate(tbl, TM) """
        
        self.processPredicate(lfOnly, leftTM, cost_join)
        self.processPredicate(rghOnly, rightTM, cost_join)
        if leftTM.getCard() > rightTM.getCard(): # apply predicates intersection where card is lower
            self.processPredicate(intersection, rightTM, cost_join)
        else:
            self.processPredicate(intersection, leftTM, cost_join)
        return self.processJoin_nl(leftTM, rightTM) # nested loop join
        """%^@^%@!$^&^&^%*$**%&*%&*&
        
        
        
        
        
        
        
        
        
        
        
        &*&^*%&*%^&*$^&$^&$%^&$^&$"""
    """ this would update two TMs into TM cluster and replace it on the graph """
    
    # clear NonUDFPred: randomly look at
    """
    Three options
    0) default: random blind processing: don't care the order of processing and consider the assoicated 
    1) ascending/descending order of processing (by selectivity)
        - keep to sort by selectivity to process asscending or dscending order
    2) foresee
        - check the associated TMs' expected cardinalities by checking the neighboring selectivity
    3) hybrid of 1) and 2)
    """
    
         
    #### TO-DO: do sophisticated clearing preds check set
    def snapshot_AllNodes(self):
        # 1) loop all keys and elements and put everything in a set
        # 2) then print all elements
        """ pprint.pprint(vars(tbl_G)) """
        res_list = self.get_AllNodes()
        print res_list
        for node in res_list:
            print vars(node)
        
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
        """ TO-DO: to update LR-tbls of TM """
        # if node_old is a key
        if node_old in self._graph:
            for node in self._graph[node_old]:
                # key .add(set)
                self._graph[node_new].add(node)
                if not self._directed:
                    self._graph[node].add(node_new)

        for key in self._graph.keys():
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

        
        
def prep_preds6():
    pred6 = pds.Predicate(pred_name = 'pred6', norm_sel_bool = True)
    pred6.setSel(sel = 0.8)
    preds6 = pds.Predicates()
    preds6.add(pred6)
    return preds6

def prep_preds7():
    pred_0_6 = pds.Predicate(pred_name = 'pred_0_6', norm_sel_bool = True)
    pred_0_6.setSel(sel = 0.6)
    preds7 = pds.Predicates()
    preds7.add(pred_0_6)
    return preds7
    
def prep_preds8():
    pred_0_4 = pds.Predicate(pred_name = 'pred_0_4', norm_sel_bool = True)
    pred_0_4.setSel(sel = 0.4)
    preds8 = pds.Predicates()
    preds8.add(pred_0_4)
    return preds8

def pred_query3():
    """ test case for nano optimization """
    preds6 = prep_preds6()
    preds7 = prep_preds7()
    preds8 = prep_preds8()
    A = tbl.Table(table_name = 'A', card = 5000, cum_cost = 0, preds = preds6)
    B = tbl.Table(table_name = 'B', card = 5000, cum_cost = 0, preds = preds7)
    AB = tbl.TM(table_name='AB', card = 10000, cum_cost = 0)
    C = tbl.Table(table_name = 'C', card = 5000, cum_cost = 0, preds = preds8)
    BC = tbl.TM(table_name='BC', card = 10000, cum_cost = 0)
    D = tbl.Table(table_name = 'D', card = 6000, cum_cost = 0, preds = preds6)
    
    conn = [(A, AB), (D, AB), (B, AB), (B, BC), (C, BC)]
    query = Query(conn, directed=True)
    return query
"""
query = pred_query3()

query._graph
import copy
query_dc = copy.deepcopy(query)
query_dc_vk = query_dc.swapKeyVal()

type(query)
type(query_dc_vk)




#OFT = oft.pred_query3

isinstance(query_dc_vk, Query) 
isinstance(query, Query)


lfOnly, intersection, rghOnly, leftTM, rightTM = query_dc_vk.div_int_lf_rg()
type(query_dc_vk)

query._graph.keys()[0].norm_preds.preds[0].sel
query._graph.keys()[2].norm_preds.preds[0].sel
query._graph.keys()[3].norm_preds.preds[0].sel

query._graph.keys()[0].norm_preds.preds[0] == query._graph.keys()[3].norm_preds.preds[0]
"""
###############################
# creates tables
# test: clearning simple predicates
#### ===>> SUCCESS
#
# 
###############################

def test_prep():
    pred0 = pds.Predicate(pred_name = 'pred0', norm_sel_bool = True)          
    pred1 = pds.Predicate(pred_name = 'pred1', norm_sel_bool = True)
    pred2 = pds.Predicate(pred_name = 'pred2', norm_sel_bool = True)
    # 
    preds0 = pds.Predicates()
    preds0.add(pred0)
    preds0.add(pred1)
    preds0.add(pred2)
    return preds0
"""
preds0 = test_prep()

A = tbl.Table('A', card = 100000, cum_cost = 0, preds = preds0)
B = tbl.Table('B', card = 100000, cum_cost = 0, preds = preds0)
C = tbl.Table('C', card = 100000, cum_cost = 0, preds = preds0)
AB = tbl.TM(table_name='AB', card = 150000, cum_cost = 0)
BC = tbl.TM(table_name='BC', card = 200000, cum_cost = 0)

"""


"""
vars(A)
print A

conn = [(A, AB), (B ,AB), (B ,BC), (C, BC)]
simple_pred = Query(conn, directed=True)        
pprint.pprint(simple_pred._graph)

C in simple_pred._graph

simple_pred.snapshot_AllNodes()

res = simple_pred.get_AllNodes()
res
"""



###############################
# creates tables
# test: clearning simple predicates
#### ===>> SUCCESS
###############################
"""
A = tbl.Table('A', card=100000, cum_cost=0, preds = preds0)
B = tbl.Table('B', card=100000, cum_cost=0, preds = preds0)
C = tbl.Table('C', card=100000, cum_cost=0,preds = preds0)
AB = tbl.TM(table_name='AB', card=200000, cum_cost=0)
BC = tbl.TM(table_name='BC', card=150000, cum_cost=0)

conn = [(A, AB), (B ,AB), (B ,BC), (C, BC)]
        
        
simple_pred = Query(conn, directed=True)        
#simple_pred.snapshot_AllNodes()
simple_pred._graph
BC in simple_pred._graph
simple_pred._graph
AB==BC
type(simple_pred._graph)

path = simple_pred.find_path(A, BC, path=[])
#print path
AB
"""
"""
connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),
                   ('C', 'D'), ('E', 'F'), ('F', 'C')]
g = Query(connections, directed=True)
g._graph                   
'A' in g._graph
type(g._graph)
"""

#pprint.pprint(simple_pred._graph)


#simple_pred.clearNonUDFPred(simple_pred.cost_join_nl)
#pprint.pprint(simple_pred._graph)

        
###############################
# creates tables
# test: intersection test
# does this 
###############################
"""
A = tbl.Table('A', card=100000, cum_cost=0, preds = preds0)
B = tbl.Table('B', card=100000, cum_cost=0, preds = preds0)
C = tbl.Table('C', card=100000, cum_cost=0, preds = preds0)
D = tbl.Table('D', card=100000, cum_cost=0, preds = preds0)
E = tbl.Table('E', card=100000, cum_cost=0, preds = preds0)
AB = tbl.TM(table_name='AB', card=0, cum_cost=0)
BC = tbl.TM(table_name='BC', card=0, cum_cost=0)
BD = tbl.TM(table_name='BD', card=0, cum_cost=0)
DE = tbl.TM(table_name='DE', card=0, cum_cost=0)

conn = [(A, AB), (B ,AB), (B ,BC), (B ,BD), (C, BC), (D, BD), (D, DE), (E, DE)]
c = Query(conn, directed=True)        

c_vk = c.swapKeyVal()

B1 = tbl.Table('B', card=110000, cum_cost=0, preds = preds0)
ab = {A, B}

ab.add(B1)
ab

"""
""" FINDINGS: if the table name is the same it is not updated."""





"""
# make dict 
pprint.pprint(c._graph)


#c.clearNonUDFPred(c.cost_join_nl)

pprint.pprint(c._graph)
"""

"""
pprint.pprint(c._graph)
defaultdict(<type 'set'>, {A: set([B]), B: set([C, D])})

del c._graph[B]

pprint.pprint(c._graph)

defaultdict(<type 'set'>, {A: set([B])})
"""

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
tbl_G = tbl.Table('G', card = 70, cum_cost=0,preds = preds0)
tbl_UC = tbl.Table('UC', card = 10000, cum_cost=0, preds = preds0)
tm_GaaUC = tbl.TM(table_name='GaaUC', card=7884, cum_cost=0, related_tbls=[tbl_G, tbl_UC])
tbl_UCS = tbl.Table('UCS', card = 20000, cum_cost=0, preds = preds0)
tm_UCaaUCS = tbl.TM(table_name='UCaaUCS', card = 15838, cum_cost=0, related_tbls=[tbl_UC, tbl_UCS])
tbl_EC = tbl.Table('EC', card = 10000, cum_cost=0, preds = preds0)
tm_UCSaaEC = tbl.TM(table_name='UCSaaEC', card = 15956, cum_cost=0, related_tbls=[tbl_UCS, tbl_EC])
tbl_ECS = tbl.Table('ECS', card = 30000, cum_cost=0, preds = preds0)
tm_ECaaECS = tbl.TM(table_name='ECaaECS', card = 23800, cum_cost=0, related_tbls=[tbl_EC, tbl_ECS])
tbl_CC = tbl.Table('CC', card = 10000, cum_cost=0, preds = preds0)
tm_CCaaUCS = tbl.TM(table_name='CCaaUCS', card = 15809, cum_cost=0, related_tbls=[tbl_CC, tbl_UCS])
tbl_SCP = tbl.Table('SCP', card = 15000, cum_cost=0, preds = preds0)
tm_CCaaSCP = tbl.TM(table_name='CCaaSCP', card = 11923, cum_cost=0, related_tbls=[tbl_CC, tbl_SCP])
tbl_CP = tbl.Table('CP', card = 10000, cum_cost=0, preds = preds0)
tm_CPaaSCP = tbl.TM(table_name='CCaaSCP', card = 12042, cum_cost=0, related_tbls=[tbl_CP, tbl_SCP])
tbl_RQ = tbl.Table('RQ', card = 26, cum_cost=0, preds = preds0)
tm_RQaaCP = tbl.TM(table_name='RQaaCP', card = 7754, cum_cost=0, related_tbls=[tbl_RQ, tbl_CP])

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
master = Query(mas_conn, directed=True)
pprint.pprint(master._graph)

conn_qry1 = [(tbl_G, tm_GaaUC),(tbl_UC, tm_GaaUC), (tbl_UC, tm_UCaaUCS), (tbl_UCS, tm_UCaaUCS), 
              (tbl_UCS, tm_UCSaaEC), (tbl_EC, tm_UCSaaEC)]
"""              

              
# tbl and tm distinguishable 
# extract pred conn from query conn
# allocate pred 
# remove all tbls
# process tms

## how can I call an object???

# has to put in a dict set



"""
c._graph           
              
print tbl_G
pprint.pprint(vars(tbl_G))

type(tbl_G)

master._graph[tbl_SCP]

dic = dict(c._graph)

dic.keys()
keys = dic.keys()
print keys

len(list(c._graph[A]))
"""

""" list index out of range if the key does not have any """
"""
for key in keys:
    print list(c._graph[key])[0]
    print key
"""
"""
for key in keys:
    print key

pprint.pprint(c._graph)
                   

from sets import Set
self._graph = defaultdict(set)

connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),
                   ('C', 'D'), ('E', 'F'), ('F', 'C')]

g = Query(connections)
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



        for key in keys:
            # if node_old is a key
            try:                
                nodes = self._graph[node_old]
                for node in nodes:
                    self.add(node_new, node)
            except KeyError:
                pass
"""
