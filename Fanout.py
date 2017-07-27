# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:01:17 2017

@author: HKIM85
"""

#from Table1_1 import Table1_1 as tbl

from collections import defaultdict


class Fanouts(object):
    """ key value pair is unique for all fanouts throughout all TMs """
    """ chose dictionary list that we can easily pick the lowest fanout ratio """
    def __init__(self):
        """ TMtblpairs: (tbl, TM) tuple """
        """ directed graph by default """
        self._graph = defaultdict(list) 
    
    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in connections:

            fanout_temp = Fanout(node1, node2)
            self.add(fanout_temp)

    def add(self, fanout_obj):
        """ Add connection between node1 and node2 """
        if fanout_obj not in self._graph[fanout_obj.getTbl()]:
            self._graph[fanout_obj.getTbl()].append(fanout_obj)
            # sort all fanout object according to fanout ratio
            self._graph[fanout_obj.getTbl()].sort(key = lambda fanout: fanout.getFO())
            
    def merge(self, other1, other2):
        self.getGraph = dict(self.getGraph().items() + other1.items() + other2.items())
    
    def getValues(self, key):
        return self._graph[key]
    
    def getGraph(self):
        return self._graph

    def getLowestFO(self, other):
        # get an intersection => make it a list
        res = {key:self._graph[key] for key in self._graph if key in other._graph}
        # create a list of fanout
        temp = [fanout for fo_list in [res[key] for key in res.keys()] for fanout in fo_list]
        # sort by fanout
        temp.sort(key = lambda fanout: fanout.getFO())
        return temp[0] # return the lowest fanout

    def getAllFOs(self):
        """ input  : fanout object """
        """ output : fanout set """
        temp = set([])
        for key in self._graph:
            temp = temp.union(self.getValues(key))
        return temp
        
    def getFOs(self, tbl):
        """ return list of sorted fanouts that connects between the two TMs
            interesection: set of intersection tables between the two TMs
            otherwise return an empty list """
        if len(self._graph[tbl])==0: # if doesn't existed, empty list created
            del self._graph[tbl] # reset by deleting the empty list
            return []
        else:
            return self._graph[tbl]
        
    def getFOs_list(self, intersection):
        FOs_list = []
        for tbl in intersection:
            FOs_list.append(self.getFOs(tbl))
        return FOs_list

    def setGraph(self, graph):
        self._graph = graph
    
    def mergeFOs(self, other):
        """ TO-DO: testing """
        for key, values in other._graph.items():
            self._graph[key].extend(values)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

            
class Fanout(object):
    """ fanout """
    def __init__(self, n_tbl, TM):
        #self.TM = TM #cp.deepcopy(TM) # TM necessary to check 
        self.tbl = n_tbl #cp.deepcopy(n_tbl)
        self.fo_ratio = self.calFOratio()
    """
    def getTM(self):
        return self.TM
    """
    def getTbl(self):
        return self.tbl
        
    def getFO(self):
        return self.fo_ratio
        
    def calFOratio(self):
        card = self.getTbl().getCard()
        return 1.0/(card)**.5 if card !=0 else -1.0
    
    def __eq__(self, other):
        """ to prevent """
        return (self.tbl) == (other.tbl) # other.TM, self.TM, 
     
    def __str__(self):
        return '({}: {})'.format(self.getTbl(), self.getFO()) #, self.getTM()
    
    def __repr__(self):
        return '({}: {})'.format(self.getTbl(), self.getFO()) #, self.getTM()
    
    def __hash__(self):
        return hash(self.getTbl()) # self.getFO(), 
    
    
    
    
    """
    def getFOs(self, tbl):
        # return the lowest fanout that connects between the two TMs
        #    interesection: set of intersection tables between the two TMs
        #    otherwise return an empty list
        if len(self._graph[tbl])==0: # if doesn't existed, empty list created
            del self._graph[tbl] # reset by deleting the empty list
        else:
            return self._graph[tbl]
        
    def getFOs_list(self, intersection):
        FOs_list = []
        for tbl in intersection:
            FOs_list.append(self.getFOs(tbl))
        return FOs_list    
    
    def getFO(self, TM, intersection):
    """
    """ return the lowest fanout that connects between the two TMs
        interesection: set of intersection tables between the two TMs
        otherwise return an empty list """
    """
        if len(self._graph[TM])==0: # if doesn't existed, empty list created
            del self._graph[TM] # reset by deleting the empty list
        else:
            temp = [x for x in self._graph[TM] if x.getTbl() in intersection]
            temp.sort(key = lambda fanout: fanout.getFO())
            return temp[0]    
    """