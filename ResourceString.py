# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 13:03:47 2016

@author: HKIM85
"""

from enum import Enum

# Enumerate file name and DATA_DIR
class IsDefault(Enum):
    __order__ = 'is_default not_default'
    is_default = 0
    not_default = 1
    # default_DIR = 'C:/Users/hkim85/Desktop/Caleb/OneDrive/Documents/Caleb/2016_PhDinCS/201603_IndStudy/201612_OptimizerPrototype'

class IsInitial(Enum):
    __order__ = 'is_initial'
    is_initial = 0
    not_initial = 1
    
class File_name:
    
    def __init__(self):
        self.default = 'A.csv'
    
    def getDefault(self):
        return self.default

        
class DIR_path:
    
    def __init__(self):
        self.default = 'C:/Users/hkim85/Desktop/Caleb/OneDrive/Documents/Caleb/2016_PhDinCS/201603_IndStudy/201612_OptimizerPrototype'
    
    def getDefault(self):
        return self.default
 
        
