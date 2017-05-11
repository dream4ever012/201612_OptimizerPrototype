# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 20:05:25 2017

@author: HKIM85

무엇이 되었는지 알아야 한다. predicate 진행한 테이블도 udf가 있을 수 있다.
"""
from collections import defaultdict
import copy
import utilities as utl

class ExpMtrcs_dict(object):
    """ an attribute in microJU """
    """ Key: tbl;  """
    def __init__(self):
        """"""
        """ directed graph by default """
        self._tbls = defaultdict()
        self._TMs = defaultdict()
    
    def add_predicate_tbl(self, tbl, exp_mtrc_tbl):
        """ have to initiate it """
        self._tbls[tbl] = exp_mtrc_tbl

    def add_predicate_TM(self, TM, exp_mtrc_TM):
        """ have to initiate it """
        self._TMs[TM] = exp_mtrc_TM
        
    def getTblGraph(self):
        return self._tbls
    
    def getExpMtrc_tbl(self, table):
        """ KeyError bypass """
        try:
            return self._tbls[table]
        except KeyError:
            pass
        """ AttributeError: 'NoneType' object has no attribute 'get_norm_preds_todo
            """
    
    def getTMGraph(self):
        return self._TMs
      
    def getTblKeys(self):
        """ to check related tables 
        output: list of registered tbl """
        return self._tbls.keys()
    
    def init(self, other):
        """ init self by other 
            ExpMtrc_tbl
        """
        for tbl in other.getKeys():
            """ has to be a deep copy that expected metrics get updated 
            doesn't change EcpMtrcs_tbl in other dict """
            self.add(tbl, copy.deepcopy(other.getGraph()[tbl]))
    
    def __str__(self):
        return '{}({})\r({})'.format(self.__class__.__name__, dict(self._tbls), dict(self._TMs))
        
    def __repr__(self):
        return '{}({})\r({})'.format(self.__class__.__name__, dict(self._tbls), dict(self._TMs))
                
    
class ExpMtrcs_tbl(object):

    def __init__(self, table):
        """ need to know current est. cum_cost/card and preds to do
            and if  """
        """ deep or swallow copy 
            TEST: attribute call by getters is call by value
        """
        self.table = table
        self.exp_card = table.getCard()
        self.exp_cum_cost = table.getCum_cost()
        self.norm_preds_todo = table.getNormPreds()
        self.udf_preds_todo = table.getUDFPreds()
        self.is_norm_preds = table.is_norm_preds()
        self.is_udf_preds = table.get_is_udf()
        self.norm_preds_done = False
        self.udf_preds_done = False
    
    def get_table(self):
        return self.table
    
    def set_exp_card(self, card):
        """ initially """
        self.exp_card = card
    
    def get_exp_card(self):
        return self.exp_card
    
    def update_exp_card(self, sel):
        self.exp_card *= sel
    
    def add_exp_cum_cost(self, tmp_cost):
        self.exp_cum_cost += tmp_cost
    
    def get_exp_cum_cost(self):
        return self.exp_cum_cost
    
    def get_is_norm_preds(self):
        return self.is_norm_preds
    
    def get_is_udf_preds(self):
        return self.is_udf_preds
    
    def get_norm_preds_todo(self):
        try:
            return self.norm_preds_todo
        except AttributeError:
            pass
    
    def grab_all_norm_preds_todo(self, preds_list):
        """ let's keep it """
        self.norm_preds_todo = [pred for pred in self.norm_preds_todo if pred not in preds_list]
    
    def get_udf_preds_todo(self):
        return self.udf_preds_todo
    
    def get_norm_preds_done(self):
        return self.norm_preds_done
    
    def update_norm_preds_done(self):
        self.norm_preds_done = True if ((len(self.norm_preds_todo) == 0)  & (self.is_norm_preds)) else False
        
    def get_udf_preds_done(self):
        return self.udf_preds_done
    
    def update_udf_preds_done(self):
        self.udf_preds_done = True if ((len(self.udf_preds_todo) == 0)  & (self.is_udf_preds)) else False
        
    def update_preds_done(self):
        self.update_norm_preds_done()
        self.update_udf_preds_done()
       
    def __str__(self):
        return 'exp_card:{}; exp_cum_cost:{}; (is_norm_preds:{}; preds_done:{}; norm_preds_todo:{}); (is_udf_preds:{}; preds_done:{}; udf_preds_todo:{})'.format(self.exp_card, self.exp_cum_cost,self.is_norm_preds, self.norm_preds_done, self.norm_preds_todo, self.is_udf_preds, self.udf_preds_done, self.udf_preds_todo)
        
    def __repr__(self):
        return 'exp_card:{}; exp_cum_cost:{}; (is_norm_preds:{}; preds_done:{}; norm_preds_todo:{}); (is_udf_preds:{}; preds_done:{}; udf_preds_todo:{})'.format(self.exp_card, self.exp_cum_cost,self.is_norm_preds, self.norm_preds_done, self.norm_preds_todo, self.is_udf_preds, self.udf_preds_done, self.udf_preds_todo)
    
class ExpMtrcs_TM(object):
    
    def __init__(self, TM):
        self.TM = TM
        self.exp_card = TM.getCard()
        self.exp_cum_cost = TM.getCum_cost()
    
    def get_TM(self):
        return self.TM
    
    def set_exp_card(self, card):
        """ initially """
        self.exp_card = card
    
    def get_exp_card(self):
        return self.exp_card
    
    def update_exp_card(self, sel):
        self.exp_card *= sel
    
    def add_exp_cum_cost(self, tmp_cost):
        self.exp_cum_cost += tmp_cost
    
    def get_exp_cum_cost(self):
        return self.exp_cum_cost
    
    def get_is_norm_preds(self):
        return self.is_norm_preds
    
    def get_is_udf_preds(self):
        return self.is_udf_preds
    
    def get_norm_preds_done(self):
        return self.norm_preds_done
    
    def get_udf_preds_done(self):
        return self.udf_preds_done
    
    def __str__(self):
        return 'exp_card:{}; exp_cum_cost:{})'.format(self.exp_card, self.exp_cum_cost)
        
    def __repr__(self):
        return 'exp_card:{}; exp_cum_cost:{})'.format(self.exp_card, self.exp_cum_cost)
                