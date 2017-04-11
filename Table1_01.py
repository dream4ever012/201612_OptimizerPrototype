# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:28:09 2016

@author: HKIM85
"""

import ResourceString as rs
import utilities as utl
    
    
class Table(object):
    
    def __init__(self, table_name, card, cum_cost, pred, initial=rs.IsInitial.is_initial, 
                 DATA_DIR= rs.DIR_path.getDefault, FILE_NAME= rs.File_name.getDefault):
        
        self.table_name = table_name
        
        # DATA_DIR and FILE_NAME are required
        if (initial == rs.IsInitial.is_initial):
            
        if DATA_DIR == rs.IsDefault.is_default:
            self.DATA_DIR = rs.DIR_path.getDefault
        else: 
            self.DATA_DIR = DATA_DIR
        
        # two cases: FILE_NAME may be default or specified
        if FILE_NAME == rs.IsDefault.is_default:
            self.FILE_NAME = rs.File_name.getDefault
        else:
            self.FILE_NAME == FILE_NAME
        
        #### File path
        self.FILE = ("{0}/"+ self.FILE_NAME).format(self.DATA_DIR)
        #### 
        self.card = 0
        
        if pred == rs.IsDefault.is_default:
            self.pred = utl.Predicates.__init__
        else:
            self.pred = pred
    
    def getTableName():
        return self.table_name
    
    def getCum_cost():
        return self.cum_cost
    
    def setCum_cost():
        self.cum_cost = cum_cost
    
    
        
        
        
