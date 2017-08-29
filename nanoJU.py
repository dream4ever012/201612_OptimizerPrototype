# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 05:07:57 2017

@author: hkim85
"""
import utilities as utl

class nJU(object):
    ### 
    def __init__(self, mJU, isLeft=True):
        ### pointers to the MTM and otherTM
        self.MTM = mJU.getMTM()
        self.otherTM = mJU.getLTM() if isLeft else mJU.getRTM()
        self.loTM = mJU.getRTM() if isLeft else mJU.getLTM() ## loTM: leftover TM
        self.isLeft = isLeft # if isLeft, left nano unit; otherwise right nano unit (MTM, RTM)
        ### 
        #self.MTM_tbls, self.otherTM_tbls = mJU.getMTM_tbls(), mJU.getLTM_tbls() if isLeft else mJU.getRTM_tbls()
        #MTM_tbls, otherTM_tbls, loTM_tbls = mJU.getMTM_tbls(), mJU.getLTM_tbls() if isLeft else mJU.getRTM_tbls(), mJU.getRTM_tbls() if isLeft else mJU.getLTM_tbls()
        MTM_tbls = mJU.getMTM_tbls()
        otherTM_tbls = mJU.getLTM_tbls() if isLeft else mJU.getRTM_tbls()
        loTM_tbls = mJU.getRTM_tbls() if isLeft else mJU.getLTM_tbls()
        ### TMjoinUnit
        #self.tbls_inter = self.MTM_tbls.intersection(self.otherTM_tbls)
        tbls_inter = MTM_tbls.intersection(otherTM_tbls)
        #self.tbls_MTMonly, self.tbls_otherTMonly = self.MTM_tbls.difference(tbls_inter), self.otherTM_tbls.difference(tbls_inter)
        tbls_MTMonly, tbls_otherTMonly = MTM_tbls.difference(tbls_inter), otherTM_tbls.difference(tbls_inter)
        self.tbls_loTMonly = loTM_tbls.difference(MTM_tbls).difference(otherTM_tbls)
               
        ### craete lists of normPreds objects
        self.predsMTMonly = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = True, isMTM = True) for table in tbls_MTMonly if table.has_normPred()]
        self.predsMotherTMboth = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = False, isMTM = True) for table in tbls_inter if table.has_normPred()]
        self.predsOtherTMonly = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = True, isMTM = False) for table in tbls_otherTMonly if table.has_normPred()]
        self.predsLoTMonly = [normPred_nju(normPred_nju_pre(mJU, table, isLeft = False if self.isLeft else True, isOnly = True, isMTM = False)) for table in self.tbls_loTMonly if table.has_normPred()]
                                                                        # left oveer TM does NOT belong to nJU and Only and not MTM
        self.TM_join = TM_join_nju_pre(mJU, hasLTM = True if self.isLeft else False)
        self.allPredsNjoin =  self.predsMTMonly +self.predsOtherTMonly + self.predsMotherTMboth + [self.TM_join]
        self.cumCost = 0.0
        self.pathList = pathList(self.allPredsNjoin, self)
        
    def getMTM(self):
        return self.MTM
    
    def getLoTM(self):
        return self.loTM
    
    def getPredsLoTMonly(self):
        return self.predsLoTMonly
    
    def getOtherTM(self):
        return self.otherTM
    
    def getPathList(self):
        return self.pathList
        
    def getCumcost(self):
        return self.cumCost
    
    def getAllPredsNjoin(self):
        return self.allPredsNjoin
    
    def addCumcost(self, cost):
        self.cumCost += cost
        
    def getTbls_liTMonly(self):
        return self.tbls_loTMonly
    
    def getIsLeft(self):
        return self.isLeft
    
    def processPathList(self):
        self.pathList.processPath()
        
    def whereIsIt(self, table):
        ### to identify where a predicate belong to       
        if table in self.predsMTMonly: return 0
        elif table in self.predsMotherTMboth: return 1
        elif table in self.predsOtherTMonly: return 2
        
    def sortPathBySumcost(self):
        self.pathList.sortPathBySumcost()
    
    def __repr__(self):
        return '(All preds:{}; isLeft:{}; cumCost:{})'.format([pred for pred in self.allPredsNjoin], self.isLeft, self.cumCost)
    
class TM_join_nju_pre(object):
    def __init__(self, mJU, hasLTM = True):
        self.mJU = mJU
        self.MTM = self.mJU.getMTM()
        self.otherTM = self.mJU.getLTM() if hasLTM else self.mJU.getRTM()
        self.hasLTM = hasLTM
    
    def getMJU(self):
        return self.mJU
    
    def getMTM(self):
        return self.MTM
    
    def getOtherTM(self):
        return self.otherTM
    
    def getHasLTM(self):
        return self.hasLTM
    
    def __repr__(self):
        return '((MTM: {}); (otherTM: {}); hasLTM: {})'.format(self.MTM, self.otherTM, self.hasLTM )

            
class TM_join_nju(object):
    def __init__(self, tm_join_nju_pre):  #mJU, hasLTM = True, joinCostF = utl.Utilities().cost_join_nl_by_card):
        self.MTM = tm_join_nju_pre.getMJU().getMTM()
        #self.MTMName = MTM.getTableName()
        self.MTMCard = self.MTM.getCard()
        self.hasLTM = tm_join_nju_pre.getHasLTM() # if hasLTM this.TMjoin is left nano Junit
        self.otherTM = tm_join_nju_pre.getMJU().getLTM() if self.hasLTM else tm_join_nju_pre.getMJU().getRTM()
        self.otherTMCard = self.otherTM.getCard()
        self.ClsTM = (self.MTM, self.otherTM)
        self.ClsTMCard = None ### if None: It hasn't been processed.
        self.costTMjoin = 0.0
        self.joinCostF = utl.Utilities().choose_join_method(self.MTMCard, self.otherTMCard)
        
    def getMTM(self):
        return self.MTM
    
    def getMTMCard(self):
        return self.MTMCard
    
    def getOtherTM(self):
        return self.otherTM
    
    def getOtherTMCard(self):
        return self.otherTMCard
    
    #def setMTMCard(self, card):
        ### have to check if revising card would not change the card of the original table 
        ### CONFIRMED! call by value getCard 
    #    self.MTMCard = card
        
    #def setOtherTMCard(self, card):
    #    self.otherTMCard = card
        
    def getCostTMjoin(self):
        return self.costTMjoin
    
    def setCostTMjoin(self, cost):
        self.costTMjoin = cost
        
    def getClsTMCard(self):
        return self.ClsTMCard
    
    def setClsTMCard(self, card):
        self.ClsTMCard = card
    
    # have to be done at path level; this method outputs only join card and cost
    # have to work on the stats
    def doTMjoin(self):
        ### join Card ### 
        #joinCard = MTM.getJoinCardByCard(self.getMTMCard(), self.getOtherTMCard(), self.MTM.getLowestFO(self.otherTM))
        #joinCost = self.joinCostF(self.getMTMCard(), self.getOtherTM())      
        #return joinCard, joinCost
        pass 
    
    def __repr__(self):
        return '(({}: {}); ({}: {}); {}; {})'.format(self.MTM, self.MTMCard, self.otherTM, self.otherTMCard, self.costTMjoin, self.hasLTM )


class normPred_nju_pre(object):
    """ object to do the permutation """
    def __init__(self, mJU, table, isLeft, isOnly = True, isMTM = True):
        ### isLeft: to LTM
        self.mJU = mJU
        self.table = table
        self.isOnly = isOnly
        self.isMTM = isMTM
        self.isLeft = isLeft
        
    def getTbl(self):
        return self.table
    
    def getIsOnly(self):
        return self.isOnly
    
    def getIsMTM(self):
        return self.isMTM
    
    def getMJU(self):
        return self.mJU
    
    def getIsLeft(self):
        return self.isLeft
    
    def __repr__(self):
        return '(Tbl: {}; isOnly: {}; isMTM: {}; isLeft: {})'.format(self.table, self.isOnly, self.isMTM, self.isLeft)
    
    
# creating two for Inctn; how to specify the target?
class normPred_nju(object):
    ### stats place-holder 
    def __init__(self, nP_nju_pre): # table, nJU, isOnly = True, isMTM = True):
        ### normPred_nju doesn't have to know if it is isOnly
        self.TM = nP_nju_pre.getMJU().getMTM() if nP_nju_pre.getIsMTM() else nP_nju_pre.getMJU().getLTM() if nP_nju_pre.getIsLeft() else nP_nju_pre.getMJU().getRTM()
        self.table = nP_nju_pre.getTbl()
        self.tblCard = self.table.getCard()
        self.tblProdNormSel = self.table.getProdNormSel()
        self.isOnly = nP_nju_pre.getIsOnly() # either MTM/otherTM-only or Insctn # otherwise 
        self.isMTM = nP_nju_pre.getIsMTM()
        self.costPred = 0.0
    
    def getTbl(self):
        return self.table
    
    def getTblCard(self):
        return self.tblCard
    
    def setTblCard(self, card):
        self.tblCard = card
    
    def getTM(self):
        return self.TM
    
    def getTblProdNormSel(self):
        return self.tblProdNormSel
    
    def getIsOnly(self):
        return self.isOnly
    
    def getIsMTM(self):
        return self.isMTM
    
    def getCostPred(self):
        return self.costPred
    
    def setCostPred(self, cost):
        self.costPred  = cost
    
    #def setCostPred(self, cost):
    #    self.costPred = cost
        
    #def addCostPred(self, cost):
    #    self.costPred += cost
    """  
    def doPred_nju(self, cost_tbl_scan = utl.cost_table_scan):
        self.costPred += cost_tbl_scan(self.tblCard) # update scan cost
        self.tblCard = self.tblCard *self.tblProdNormSel # update table card
        self.costPred += self.joinCostF()
    """
    
    def __repr__(self):
        return '({}; {}; {}; {})'.format(self.table, self.tblCard, self.tblProdNormSel, self.costPred)
    
class pathList(object):
    """ create permutation and instantiate path object and norm_pred/TMjoin objects """
    def __init__(self, all_ops, nJU):
        """  """
        import itertools    
        self.IntToMTMlist = [path(all_ops, list(path_tup), nJU, IntPtoMTM = True) for path_tup in itertools.permutations(all_ops)]
        ##### self.IntToOtherTMlist = [path(all_ops, list(path_tup), nJU, IntPtoMTM = False) for path_tup in itertools.permutations(all_ops)]
        ### assign all intersection to otherTM
        
        #self.expectedCost = 0.0 """ TO-DO: has to go with Cost at distributed setting """
        self.estCard = 0.0
        self.estCost = 0.0
        self.isLegit = False
        self.Rbetter = None

    def getIntToMTMlist(self):
        return self.IntToMTMlist
    
    def getIntToOtherTMlist(self):
        return self.IntToOtherTMlist
    
    def getIsLegit(self):
        return self.isLegit
    
    def getRbetter(self):
        return self.Rbetter
    
    def processPath(self):
        #for path_ITM, path_ITO in zip(self.IntToMTMlist, self.IntToOtherTMlist):
        #    path_ITM.processPath()
        for path_ITM in self.IntToMTMlist:
            path_ITM.processPath()
            ##### path_ITO.processPath()    
            
    def sortPathBySumcost(self):
        self.IntToMTMlist.sort(key=lambda path: sum(path.cost))
        ##### self.IntToOtherTMlist.sort(key=lambda path: sum(path.cost))

    def __repr__(self):
        return '(IntToMTMlist: {})'.format(self.IntToMTMlist) #, self.IntToOtherTMlist) , \n \n IntToOtherTMlist: {}
          
    
class path(object):
    def __init__(self, all_ops, path_tup, nJU, IntPtoMTM):
        ### IntPtoMTM Intersection tables to MTM if IntPtoMTM is True else to otherTM
        self.statHolder = self.createStatsDict(all_ops) #dictionary (table, card)
        """ TO-DO: look up methods for dict """
        self.path = path_tup
        self.pathMatObj_list = [] ### this is where stats would be updated
        self.instMatPredObj_list()
        self.cost = [] ### cost of each pred/TMjoin
        self.nJU = nJU        

    def __repr__(self):
        return '(statHolder:{}; path:{}; cost:{} \n)'.format(self.statHolder, self.pathMatObj_list, self.cost)
   
    def createStatHolder(self, op):
        """ input instance of normPred_nju or TM_join_nju """
        if isinstance(op, normPred_nju_pre):
            table = op.getTbl()
            return (table, table.getCard())
        elif isinstance(op, TM_join_nju_pre):
            MTM = op.getMTM()
            OtherTM = op.getOtherTM()                                  ### stats for TMcls
            return (MTM, MTM.getCard()), (OtherTM, OtherTM.getCard()), ((MTM, OtherTM), 0)

    def createStatsDict(self, all_ops):
        """ call createStatHolder """
        list_tup =( [self.createStatHolder(op) for op in all_ops[0:-1]] 
            + [tup for tup in self.createStatHolder(all_ops[-1])])
        return dict((table, card) for table, card in list_tup)
    
    """
    def instantiatePth(self, path_tup):
        temp = []
        for obj in path_tup:
            temp.append(obj, 0)
    """
    
    def getPath(self):
        return self.path
    
    def getPathMatObj_list(self):
        return self.pathMatObj_list
    
    def getStat(self, table):
        try:
            return self.statHolder[table]
        except KeyError:
            pass ## Nonetype error: table doesn't exist in StatHolder
            
    def getTMjoinStat(self):
        try:
            TM_join_obj = self.pathMatObj_list[-1]
            return TM_join_obj, self.statHolder[TM_join_obj.getMTM(), TM_join_obj.getOtherTM()]
        except KeyError:
            pass
    
    def updateCard(self, tbl1, card):
        ### add card to stat holder
        ### do nothing if tbl does not exist in the stat dict
        try:
            self.statHolder[tbl1] = card
        except KeyError:
            pass
        
    def updateCost(self, cost):
        ### have to reset the cost list if recalcuate cost
        self.cost.append(cost)
    
    def instMatPredObj_list(self):
        for pred_obj in self.path: self.pathMatObj_list.append(self.instMatPredObj(pred_obj))
    
    def instMatPredObj(self, pred_obj):
        if isinstance(pred_obj, normPred_nju_pre):
            return normPred_nju(pred_obj)
        elif isinstance(pred_obj, TM_join_nju_pre):
            return TM_join_nju(pred_obj)

    def processPath(self):
        for pred_obj in self.pathMatObj_list:
            self.processObj(pred_obj) #, cost_table_scan = utl.Utilities().cost_table_scan, cost_join_nl_by_card = utl.Utilities().cost_join_nl_by_card)
    
    def processObj(self, pred_obj): #cost_table_scan = utl.Utilities().cost_table_scan, cost_join_nl_by_card = utl.Utilities().cost_join_nl_by_card):
        ### TO-Do: can define join method dynamically as utillities package
        ### process either normPred or TMjoin
        temp_cost = 0.0
        if isinstance(pred_obj, normPred_nju): ### pred obj is table
            # table scan cost
            table = pred_obj.getTbl()
            temp_cost = utl.Utilities().cost_table_scan(self.getStat(table)) # cost of table scan
            # update table card
            pred_obj.setTblCard(self.getStat(table)*pred_obj.getTblProdNormSel()) ### set pred card
            self.updateCard(table, self.getStat(table)*pred_obj.getTblProdNormSel()) ### update to statholder
            
            # join cost
            TM = pred_obj.getTM()
            TMcard = self.getStat(TM)
            tableCard = self.getStat(table)
            temp_cost += utl.Utilities().cost_join_nl_by_card(tableCard, TMcard)
            # update TM card
            self.updateCard(TM, utl.Utilities().card_join_TM_tbl_by_card(TMcard, pred_obj.getTblProdNormSel()))
            pred_obj.setCostPred(temp_cost) ### update temp_cost tp pred_obj
            
            """ UPDATE PRED OBJ + MAKE SURE STATHOLDER"""
                
        elif isinstance(pred_obj, TM_join_nju): ### pred obj is TM join
            # TM join cost
            MTM, OtherTM = pred_obj.getMTM(), pred_obj.getOtherTM()
            MTMcard = self.getStat(MTM)
            OtherTMcard = self.getStat(OtherTM)
            temp_cost = utl.Utilities().cost_join_nl_by_card(MTMcard, OtherTMcard) ### cost of TM join
            # update TMClsCard                
            self.updateCard((MTM, OtherTM), utl.Utilities().card_join_TM_TM_by_card(MTMcard, OtherTMcard, MTM.getLowestFO(OtherTM).getFO()))
            pred_obj.setCostTMjoin(temp_cost) ### update TMjoin cost to TMjoin obj
        self.updateCost(temp_cost) ### update pred/TMjoin cost to statHolder