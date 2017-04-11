# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:27:31 2017

@author: HKIM85
"""

import ExpMtrcs_tbl as exmTbl

class MicroJU(object):
    """ three TMs: midTM and otherTMs """
    def __init__(self, midTM, query):
        self.query = query
        self.midTM = midTM
        self.otherTMs = set([])
        #self.expectedCost = 0.0 """ TO-DO: has to go with Cost at distributed setting """
        self.expCard = 0.0
        self.expCost = 0.0
        self.isLegit = False
        
            
    def addOtherTMs(self, TM):
        if (self.isLegit == False):
            if (TM != self.midTM):
                self.otherTMs.add(TM)
            if (len(self.otherTMs) == 2):
                self.isLegit = True
        else:
            print '{} is full that {} cannot be added.'.format(self, TM)
    
    def getIsLegit(self):
        return self.isLegit
            
    def getMidTM(self):
        return self.midTM
    
    def getOtherTMs(self):
        return self.otherTMs
    
    def getLTM(self):
        return list(self.otherTMs)[0]
    
    def getRTM(self):
        return list(self.otherTMs)[1]
    
    def getMTM_tbls(self):
        return self.query.getQuery_vk().getValues(self.getMidTM())
    
    def getLTM_tbls(self):
        return self.query.getQuery_vk().getValues(self.getLTM())
    
    def getRTM_tbls(self):
        return self.query.getQuery_vk().getValues(self.getRTM())
    
    def getTables(self, query):
        return self.getMTM_tbls().union(self.getLTM_tbls()).union(self.getRTM_tbls())
    
    def getExpCard(self):
        return self.expCard
    
    def setExpCard(self, expCard):
        self.expCard = expCard
    
    def addExpCard(self, thisCard):
        self.expCard += thisCard
    
    def getExpCost(self):
        return self.expCost
    
    def addExpCost(self, thisCost):
        self.expCost = thisCost
    
    def updateCard(self, expCard):
        self.expCard = expCard
    
    def __repr__(self):
        return '{}: {}; {}'.format(self.midTM, self.otherTMs, self.isLegit)
    
    def __eq__(self, other):
        return (self.midTM == other.midTM) and (self.otherTMs == other.otherTMs)
    
    
class MicroJUlist(object):
    def __init__(self, microJUlist = [], excldShort = True):
        """ mJUlist: list of microJU """
        self.mJUlist = microJUlist
        self.excldShort = excldShort
        
    def getMJUlist(self):
        return self.mJUlist
    
    def append(self, microJU):
        if self.excldShort == True:
            # no redendancy/ only full microJU/ 
            if (microJU not in self.mJUlist) and (microJU.getIsLegit()): self.mJUlist.append(microJU)
        else: # full (midTM + twoTMs) and partial microJU
            if (microJU not in self.mJUlist): self.mJUlist.append(microJU)
    
    def __repr__(self):
        return '{}; {}'.format(self.mJUlist, self.excldShort)
    
    