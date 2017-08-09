# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:27:31 2017

@author: HKIM85
"""

import ExpMtrcs_tbl as emt
import utilities as utl
utl1 = utl.Utilities()

class MicroJU(object):
    """ three TMs: midTM and otherTMs """
    def __init__(self, midTM, query):
        self.query = query
        self.midTM = midTM
        self.otherTMs = set([])
        #self.expectedCost = 0.0 """ TO-DO: has to go with Cost at distributed setting """
        self.estCard = 0.0
        self.estCost = 0.0
        self.isLegit = False
        self.Rbetter = None
        # may not want to initiate this object when it is obviously not productive 
        self.expMtrcsDict = None
        if (self.isLegit == True):
            self.initiate_tbls_TMs_est_mtrcs() # after add other TMs
        
    def initiate_tbl_est_metrics(self, table):
        """ initiate table estimated metrics to _tbls """
        #expMtrcs_tbl = emt.ExpMtrcs_tbl(table)
        self.expMtrcsDict.add_predicate_tbl(table, emt.ExpMtrcs_tbl(table)) # expMtrcs_tbl)
    
    def initiate_tbls_est_metrics(self):
        """ initiate estimated metrics of tables in micro JU """
        for table in self.getMTM_tbls().union(self.getLTM_tbls()).union(self.getRTM_tbls()):
            self.initiate_tbl_est_metrics(table)

    def initiate_TM_est_metrics(self, TM):
        """ initiate estimated metrics of a TM to _TMs """
        self.expMtrcsDict.add_predicate_TM(TM, emt.ExpMtrcs_TM(TM))

    def initiate_TMs_est_metrics(self):
        """ initiate estimated metrics of a TM to _TMs """
        self.initiate_TM_est_metrics(self.getMidTM())
        self.initiate_TM_est_metrics(self.getLTM())
        self.initiate_TM_est_metrics(self.getRTM())
    
    def initiate_tbls_TMs_est_mtrcs(self):
        self.expMtrcsDict = emt.ExpMtrcs_dict()
        self.initiate_tbls_est_metrics()
        self.initiate_TMs_est_metrics()
        
    def getExpMtrcsDict(self):
        return self.expMtrcsDict
    
    def getExpMtrc_tbl(self, table):
        try:
            return self.expMtrcsDict.getExpMtrc_tbl(table)
        except AttributeError:
            pass    
    
    def getRbetter(self):
        return self.Rbetter
    
    def setRbetter(self):
        self.Rbetter = True
        
    def setLbetter(self):
        self.Rbetter = False

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

    def getMTM(self):
        return self.midTM
    
    def getOtherTMs(self):
        return self.otherTMs
    
    def getLTM(self):
        return sorted(self.otherTMs)[0]
    
    def getRTM(self):
        return sorted(self.otherTMs)[1]
    
    def getMTM_tbls(self):
        return self.query.getQuery_vk().getValues(self.getMidTM())
    
    def getLTM_tbls(self):
        return self.query.getQuery_vk().getValues(self.getLTM())
    
    def getRTM_tbls(self):
        return self.query.getQuery_vk().getValues(self.getRTM())
    
    def getTables(self, query):
        return self.getMTM_tbls().union(self.getLTM_tbls()).union(self.getRTM_tbls())
    
    def getEstCard(self):
        return self.estCard
    
    def setEstCard(self, estCard):
        self.estCard = estCard
    
    def addEstCard(self, thisCard):
        self.estCard += thisCard
    
    def getEstCost(self):
        return self.estCost
    
    def addEstCost(self, thisCost):
        self.estCost += thisCost
    
    def updateCard(self, expCard):
        self.expCard = expCard
        
    def update_normPreds_ExpMtrcsDict(self, cost_norm_preds):
        """ input: cost_norm_preds function """
        expMtrcsDict = self.getExpMtrcsDict()
        for table in expMtrcsDict.getTblGraph().keys():
            expMtrcs_tbl = expMtrcsDict.getExpMtrc_tbl(table)
            expMtrcs_tbl.add_exp_cum_cost(cost_norm_preds(table))       # cost of table scan
            expMtrcs_tbl.update_exp_card(table.getProdNormSel())        # update est. cardinality
            expMtrcs_tbl.grab_all_norm_preds_todo(table.getNormPreds()) # clear predicate to_do list
            expMtrcs_tbl.update_preds_done()                            # update norm_preds_done
    
    
    def getProdNormSel_set(self, table_set):
        prod_sel = 1.0
        for tbl1 in table_set: prod_sel *= tbl1.getProdNormSel()
        return prod_sel
      
    def cost_join_nl_by_card(self, TM1_card, TM2_card):
        if (TM1_card <= TM2_card):
            return TM1_card + TM1_card * TM2_card
        else:
            return TM2_card + TM1_card * TM2_card
    
    def get_lower_est_cost_mJU(self, MTM_card, otherTM_card, tbls_Monly, tbls_otherOnly, tbls_intersection, costF_join, norm_p_costF):
        """ get lower cost """
        MTM_card_ = MTM_card * self.getProdNormSel_set(tbls_Monly) # intermedicate MTM_card
        otherTM_card_ = otherTM_card * self.getProdNormSel_set(tbls_otherOnly)
        prodNSel_intrsctn = self.getProdNormSel_set(tbls_intersection)
        res = None
        res = costF_join(MTM_card_ * prodNSel_intrsctn, otherTM_card_) if (MTM_card_ <= otherTM_card_) else costF_join(MTM_card_, otherTM_card_ * prodNSel_intrsctn)
        res += (norm_p_costF(MTM_card) + norm_p_costF(otherTM_card)) # norm_pred scan cost
        return res
        
    def getEstJnCst_mJU(self, costF_join = utl1.cost_join_nl_by_card, norm_p_costF = utl1.cost_table_scan):
        
        """ get connected tbls to each TM """
        MTM_tbls, LTM_tbls, RTM_tbls = self.getMTM_tbls(), self.getLTM_tbls(), self.getRTM_tbls()
        MTM_card, LTM_card, RTM_card = self.getMTM().getCard(), self.getLTM().getCard(), self.getRTM().getCard()

        """ LTM = MTM """
        # p1_4: B; p2_5: C; p3_7: A
        p1_4 = MTM_tbls.intersection(LTM_tbls) 
        p2_5, p3_7 = MTM_tbls.difference(p1_4), LTM_tbls.difference(p1_4)

        """ MTM = RTM """
        p2_4 = MTM_tbls.intersection(RTM_tbls)
        p1_5, p3_6 = MTM_tbls.difference(p2_4), RTM_tbls.difference(p2_4)

        M_LTM_cost = self.get_lower_est_cost_mJU(MTM_card, LTM_card, p2_5, p3_7, p1_4, costF_join, norm_p_costF)
        M_RTM_cost = self.get_lower_est_cost_mJU(MTM_card, RTM_card, p1_5, p3_6, p2_4, costF_join, norm_p_costF)
        self.setRbetter() if M_RTM_cost < M_LTM_cost else self.setLbetter()
        
        
        
        return (min(M_LTM_cost,M_RTM_cost))
    

    """ 
    =================== get lower estimated mJU =========================
    """


    def toMTM(self, MTM_card, otherTM_card, MTM_tbls, otherTM_tbls):
        return MTM_card*self.getProdNormSel_set(MTM_tbls) <= otherTM_card*self.getProdNormSel_set(otherTM_tbls)

    """ 
    =================== get lower estimated mJU =========================
    """
    
    def __str__(self):
        return '{}: {}; {}'.format(self.midTM, self.otherTMs, self.isLegit, self.Rbetter)
    
    def __repr__(self):
        return '{}: {}; {}'.format(self.midTM, self.otherTMs, self.isLegit, self.Rbetter)
    
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
            
    def initiate_tbls_TMs_est_mtrcs(self):
        for mJU in self.mJUlist:
            mJU.initiate_tbls_TMs_est_mtrcs()
        
    def getMicroJUlist(self, query, excldShort = True):
        import itertools
        """ midTM, linked TM set ==> combination of link set ==> create MicroJU 
            ==> append to JUlist """
        mJUlist = MicroJUlist([])
        queryGraph_vk = query.getQuery_vk().getQueryGraph()
        for TM1 in queryGraph_vk.keys(): # first node      
            #print '{}: {}'.format(TM1, 'start')   
            otherTMs = set([])
            for table1 in queryGraph_vk[TM1]: # tbl-link
                #print '1 tl', table1, query._graph[table1]
                for TM2 in query.getQueryGraph()[table1]:
                    #print TM2
                    otherTMs.add(TM2) # linked TM set
                    #print 'otherTMs:', otherTMs
                if excldShort == True: otherTMs.discard(TM1)
                for TM3, TM4 in itertools.combinations(otherTMs, 2):
                    microJU = MicroJU(TM1, query)
                    microJU.addOtherTMs(TM3)
                    microJU.addOtherTMs(TM4)
                    #print 'microJU:', microJU
                    mJUlist.append(microJU)
        return mJUlist
    
    def update_normPreds_ExpMtrcsDict_mJUlist(self):
        for mJU in self.getMJUlist():
            MicroJU.update_normPreds_ExpMtrcsDict(mJU)
    
    def cal_agg_prod_card(self, *TM_list):
        """ A function that cal. product of cardinalities 
            input: a list of TMs """
        temp_card = 1
        for TM in TM_list: temp_card *= TM.getCard()
        return temp_card
    
    def cal_agg_exp_sel(self, tbl_set):
        """ A method that aggregate all predicates 
        output 1.0 when there is no predicates in a table 
        input: set of tbls """
        temp_sel = 1.0
        for table in list(tbl_set): temp_sel *= table.get_exp_norm_sel()
        return temp_sel
    
    def get_conn_tbls(self, query, mJU):
        """ get all connected tables to three tables in mJU 
            input: query, mJU; output: tbls_set connected to the three TMs """
        query_vk = query.getQuery_vk()
        return query_vk.getValues(mJU.getMidTM()).union(query_vk.getValues(mJU.getLTM())).union(query_vk.getValues(mJU.getRTM()))
    
    def updateExpCard(self, query):
        for mJU in self.mJUlist:
            midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
            res = self.cal_agg_exp_sel(self.get_conn_tbls(query, mJU)) * self.cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
            mJU.setExpCard(res)
    def updateEstCardCost_mJU(self,query):
        for mJU in self.mJUlist:
            """ update estCost """
            estCost = mJU.getEstJnCst_mJU()
            mJU.addEstCost(estCost)
            
            """ update estCard """
            midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
            res = self.cal_agg_exp_sel(self.get_conn_tbls(query, mJU)) * self.cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
            mJU.setEstCard(res)

    def updateEstCostCardCost_mJU(self, query):
        for mJU in self.mJUlist:
            
            """ update estCost """
            estCost = mJU.getEstJnCst_mJU()
            mJU.addEstCost(estCost)
            
            """ update estCard """
            midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
            res = self.cal_agg_exp_sel(self.get_conn_tbls(query, mJU)) * self.cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
            mJU.setEstCard(res)

            
    def mJUlist_sort_by_cost(self):
        self.getMJUlist().sort(key = lambda mJU: mJU.getEstCost())

    def mJUlist_sort_by_card(self):
        self.getMJUlist().sort(key = lambda mJU: mJU.getEstCard())

    def mJUlist_display(self):
        for mJU in self.getMJUlist():
            print mJU, mJU.getEstCost(), mJU.getEstCard()
    
    def __repr__(self):
        return '{}; {}'.format(self.mJUlist, self.excldShort)
    
    