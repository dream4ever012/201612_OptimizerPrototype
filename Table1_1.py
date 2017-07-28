# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:28:09 2016

@author: HKIM85
"""
#cd 'C:\Users\hkim85\Desktop\Caleb\OneDrive\Documents\Caleb\2016_PhDinCS\201603_IndStudy\201612_OptimizerPrototype'

#import ResourceString as rs
#import utilities as utl
import predicate as pds
import Fanout as fo

from itertools import chain
from collections import defaultdict

class TM(object):   
    def __init__(self, table_name='DFT', card=0, cum_cost=0):
        self.table_name = table_name
        self.card = card
        self.cum_cost = cum_cost
        """ related tbls and right tables for fanout """
        self.fanouts = fo.Fanouts() # later check with 'is None' to see if TM is connected with Normal Table
        self.TMbool = True
        self.isClstr = False
                
    # cannot change Table name after instantiation
    def __str__(self):
        return self.table_name#'{}'.format(self.table_name)
    
    def __repr__(self):
        return '{}'.format(self.table_name) # self.table_name
        
    def getTableName(self):
        return self.table_name
        # return self.table_name
        
    def getTMbool(self):
        return self.TMbool
    
    # cannot change cardinality
    def getCard(self):
        return self.card
        
    def getFanouts(self):
        return self.fanouts
    
    def getLowestFO(self, other):
        return self.getFanouts().getLowestFO(other.getFanouts())
        
    def getCum_cost(self):
        return self.cum_cost
    
    def getIsClstr(self):
        return self.isClstr
    
    def updateCard(self, sel):
        self.card *= sel    
        
    def addCum_cost(self, tmp_cost):
        self.cum_cost += tmp_cost
    
    def addFO(self, fanout_obj):
        self.fanouts.add(fanout_obj)
        
    """ https://docs.python.org/2/reference/datamodel.html """    
    def __eq__(self, other):
        return self.table_name == other.table_name
        
    def __hash__(self):
        return hash(self.table_name)
    
    
class TM_clstr(TM):
    def __init__(self, mJU):
        """ query object contains TM_cluster query """
        card, cum_cost = mJU.getEstCard(), mJU.getEstCost()
        lTM, mTM, rTM = mJU.getLTM(), mJU.getMTM(), mJU.getRTM()
        """ TO-DO: built how to combine all names, still """
        TM.__init__(self, table_name=('{}_{}_{}'.format(lTM.getTableName(), mTM.getTableName(), rTM.getTableName())), card=card, cum_cost = cum_cost)
        self.isClstr = True
        self.clstrdTMs = set([])
        self.initClstrdTMs(lTM, mTM, rTM)
        self.fanouts = fo.Fanouts()
        """ inherit fanouts from other TMs """
        self.aggregateFanouts(mJU)
  
    def getIsClstr(self):
        return self.isClstr
    
    def getclstrdTMs(self):
        return self.clstrdTMs

    def initClstrdTMs(self, lTM, mTM, rTM):
        """ get all clustered TM """
        temp = set([])
        self.clstrdTMs = ((temp.union(lTM.getclstrdTMs()) if lTM.isClstr == True else set([])).union((mTM.getclstrdTMs()) if mTM.isClstr == True else set([]))).union((rTM.getclstrdTMs()) if rTM.isClstr == True else set([]))
    
    def hasIdtclTMs(self, other):
        return self.getclstrdTMs() == other.getclstredTMs()
    
    def aggregateFanouts(self, mJU):
        """ inherit fanouts from mJU """ 
        res = defaultdict(list, dict(chain(mJU.getMTM().getFanouts().getGraph().items(), 
                                           mJU.getLTM().getFanouts().getGraph().items(), 
                                           mJU.getRTM().getFanouts().getGraph().items() )))
        
        self.fanouts.setGraph(res)

    def __eq__(self, other):
        if other.getIsClstr() ==True:
            return self.clstrdTMs == other.clstrdTMs
        else: 
            return False


class Table(object):    
    def __init__(self, table_name='DFT', card=0, cum_cost=0, 
                 preds=pds.Predicates()):
        self.table_name = table_name
        self.card = card
        self.cum_cost = cum_cost
        # to check 
        self.TMbool = False
        # to contain normal predicates
        self.norm_preds = pds.Predicates([pred for pred in preds.getPreds() if pred.norm_sel_bool == True])
        # to contain UDF predicates
        self.UDF_preds = pds.Predicates([pred for pred in preds.getPreds() if pred.norm_sel_bool == False])
        if (self.UDF_preds.has_UDFPred()==False): self.is_UDF = False
        else: self.is_UDF = True
        self.exp_norm_sel = self.get_exp_norm_self()
    
    # cannot change Table name after instantiation
    """ https://docs.python.org/2/reference/datamodel.html """
    def __str__(self):
        return self.table_name#'{}'.format(self.table_name)
    
    def __repr__(self):
        return '{}'.format(self.table_name) # self.table_name
        
    def __hash__(self):
        return hash(self.table_name)
    
    def __eq__(self, other):
        return self.table_name == other.table_name
    
    def getNormPreds(self):
        return self.norm_preds.getPreds()
    
    def getProdNormSel(self):
        return self.norm_preds.getProdNormSel()
    
    def getUDFPreds(self):
        return self.UDF_preds.getPreds()
    
    def getNormSelList(self):
        return self.getNormPreds() #.getNormSelList()
        
    def getTableName(self):
        return self.table_name
        # return self.table_name
        
    def get_exp_norm_self(self):
        return self.norm_preds.get_exp_norm_sel()
        
    def getNormPredSel(self):
        """ works only when preds has only one pred. 
        Otherwise, this function returns None """
        return self.norm_preds.getPredSel()
        
    # cannot change cardinality
    def getCard(self):
        return self.card
    
    def setCard(self, card):
        self.card = card
    
    def getCum_cost(self):
        return self.cum_cost
    
    def getTMbool(self):
        return self.TMbool
      
    def get_exp_norm_sel(self):
        return self.exp_norm_sel
    
    def get_is_udf(self):
        return self.is_UDF
    
    def is_norm_preds(self):
        return (len(self.getNormPreds())>0)
        
    def resetCum_cost(self):
        self.cum_cost = 0.0
    
    def addCum_cost(self, tmp_cost):
        self.cum_cost += tmp_cost
        
    def updateCard(self, sel):
        self.card = self.card * sel
        
    """ functions for Predicates """
    """ TO-DO: test this functions """
    def add_pred(self, pred, is_norm_pred=True):
        if (is_norm_pred==True):
            self.norm_preds.add(pred)
        elif (is_norm_pred==False):
            self.UDF_preds.add(pred)
        
    def remove_pred(self, pred, is_norm_pred=True):
        if (is_norm_pred == True):
            self.norm_preds.remove(pred)
        elif (is_norm_pred == False):
            self.UDF_preds.remove(pred)
    
    def has_normPred(self):
        return self.norm_preds.has_normPred()
    
    def has_mult_normPred(self):
        return self.norm_preds.has_mult_normPred()
    
    def has_UDFPred(self):
        return self.UDF_preds.has_UDFPred()
    
    """ TO-DO: How to delete """
    
    """ TO-DO: test if this works """
    def processNorm_preds(self):
        if (self.has_normPred()):
            self.norm_preds.sort_by_sel()
        temp_sel = 1.0
        for pred in  self.norm_preds.getPreds():
            """ update cum_cost + card"""
            self.addCum_cost(self.card)
            self.updateCard(pred.getSel())
            temp_sel = temp_sel * pred.sel
        temp_pred = pds.Predicate(pred_name = 'temp_pred', norm_sel_bool = True)
        temp_pred.setSel(temp_sel)
        self.norm_preds = pds.Predicates([temp_pred])
        

   
    


        
    
    
"""
tm1 = TM(table_name='DFT', card=0, cum_cost=0, related_tbls= [])
try:
    tm1.norm_preds
except AttributeError:
    print 'AttributeError'
"""

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

preds0 = test_prep()
###############################
# test1) create a table with normal predicates
#### ===>> SUCCESS
# 
###############################
def test1():
    A = Table('A', card=80000, cum_cost=0, preds=preds0)
    print vars(A)
    
#test1()

B = Table('B', card=60000, cum_cost=0, preds=pds.Predicates())
C = Table('C', card=100000, cum_cost=0,preds=pds.Predicates())
D = Table('C', card=100000, cum_cost=0,preds=pds.Predicates())



name = 'Z'
table = {}

table[name] = Table(name, card=100000, cum_cost=0,preds=pds.Predicates())
#print table

