# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:27:31 2017

@author: HKIM85
"""

import ExpMtrcs_tbl as emt

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
        # may not want to initiate this object when it is obviously not productive 
        self.expMtrcsDict = None 
        
    def initiate_tbl_est_metrics(self, table, expMtrcsDict):
        """ initiate table estimated metrics to _tbls """
        expMtrcsDict.add_predicate_tbl(table, emt.ExpMtrcs_tbl(table))
    
    def initiate_tbls_est_metrics(self, expMtrcsDict):
        """ initiate estimated metrics of tables in micro JU """
        for table in self.getMTM_tbls().union(self.getLTM_tbls()).union(self.getRTM_tbls()):
            self.initiate_tbl_est_metrics(table, expMtrcsDict)

    def initiate_TM_est_metrics(self, TM, expMtrcsDict):
        """ initiate estimated metrics of a TM to _TMs """
        expMtrcsDict.add_predicate_TM(TM, emt.ExpMtrcs_TM(TM))

    def initiate_TMs_est_metrics(self, expMtrcsDict):
        """ initiate estimated metrics of a TM to _TMs """
        self.initiate_TM_est_metrics(self.getMidTM(), expMtrcsDict)
        self.initiate_TM_est_metrics(self.getLTM(), expMtrcsDict)
        self.initiate_TM_est_metrics(self.getRTM(), expMtrcsDict)
    
    def initiate_tbls_TMs_est_mtrcs(self):
        self.expMtrcsDict = emt.ExpMtrcs_dict()
        self.initiate_tbls_est_metrics(self.expMtrcsDict)
        self.initiate_TMs_est_metrics(self.expMtrcsDict)

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
    
    