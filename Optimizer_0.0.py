# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:50:22 2017

@author: HKIM85
"""


#import predicate as pds
import ObjectsForTesting as oft
import microJU as mju
import utilities

class Optimizer(object):
    def __init__(self, query = oft.prep_query0(), excldShort = True):
        self.query = query
        self.mJUlist = None
        self.updateMicroJU()

    def processNorm_preds(self):
        """ normal predicates in a single table"""
        norm_tbls = self.query.getKeys()
        for norm_tbl in norm_tbls:
            norm_tbl.processNorm_preds()
            
    def snapshot_query(self):
        self.query.snapshot_AllNodes()

    def updateMicroJU(self, excldShort = True):
        import itertools
        """ midTM, linked TM set ==> combination of link set ==> create MicroJU 
            ==> append to JUlist """
        """ output empty list when there are no MicroJU in the current query 
            ==> there are """
        mJUlist = mju.MicroJUlist() # list of micro join unit
        queryGraph_vk = self.query.getQuery_vk().getQueryGraph()
        for TM1 in queryGraph_vk.keys(): # first node      
            #print '{}: {}'.format(TM1, 'start')   
            otherTMs = set([])
            for table1 in queryGraph_vk[TM1]: # tbl-link
                #print '1 tl', table1, query._graph[table1]
                for TM2 in self.query.getQueryGraph()[table1]:
                    #print TM2
                    otherTMs.add(TM2) # linked TM set
                    #print 'otherTMs:', otherTMs
                for TM3, TM4 in itertools.combinations(otherTMs, 2):
                    microJU = mju.MicroJU(TM1)
                    microJU.addOtherTMs(TM3)
                    microJU.addOtherTMs(TM4)
                    #print 'microJU:', microJU
                    mJUlist.append(microJU)
        self.mJUlist = mJUlist

    def cal_agg_exp_sel(self, tbl_set):
        """ A method that aggregate all predicates 
        output when there is no predicates in a table 
        input: set of tbls """
        temp_sel = 1.0
        for table in list(tbl_set): temp_sel *= table.get_exp_norm_sel()
        return temp_sel

    def get_conn_tbls(self, mJU):
        query_vk = self.query.getQuery_vk()
        return query_vk.getValues(mJU.getMidTM()).union(query_vk.getValues(mJU.getLTM())).union(query_vk.getValues(mJU.getRTM()))
    
    def cal_agg_prod_card(self, *TM_list):
        """ A function that cal. product of cardinalities 
            input: a list of TMs """
        temp_card = 1
        for TM in TM_list: temp_card *= TM.getCard()
        return temp_card
    
    def getEstCardmJUlist(self):
        for mJU in self.mJUlist.getMJUlist():
            midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
            res = self.cal_agg_exp_sel(self.get_conn_tbls(self.query, mJU)) * self.cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
            mJU.setExpCard(res)
            
    
    """ FINDINGS 
    -- expected cardinality may be the same or very similar
    -- then we have to check the expected cost for each of such mJUs
    
    preds0 = prep_preds0()
    preds1 = prep_preds1()
    preds2 = prep_preds2()
    preds3 = prep_preds3()
    preds4 = prep_preds4()
            
    A = tbl.Table('A', card=100000, cum_cost=0, preds = preds0)
    B = tbl.Table('B', card=80000, cum_cost=0, preds = preds1)
    C = tbl.Table('C', card=60000, cum_cost=0, preds = preds2)
    D = tbl.Table('D', card=40000, cum_cost=0, preds = preds3)
    E = tbl.Table('E', card=20000, cum_cost=0, preds = preds4)
    AB = tbl.TM(table_name='AB', card=500000, cum_cost=0)
    BC = tbl.TM(table_name='BC', card=700000, cum_cost=0)
    CD = tbl.TM(table_name='CD', card=850000, cum_cost=0)
    BE = tbl.TM(table_name='BE', card=900000, cum_cost=0)
    CE = tbl.TM(table_name='CE', card=1200000, cum_cost=0)

    conn = [(A, AB), (B, AB), (B, BC), (C, BC), (B, BE), (C, CE), (C, CD), (D, CD), (E, BE), (E, CE)]
    #conn = [(A, AB), (B, AB), (B, BC), (C, BC)]
    #conn = [(A, AB), (B, AB)]
    query = qry.Query(conn, directed=True) 
    
    for mJU in mJUlist.getMJUlist():
    print mJU, mJU.getExpCard()
    BC: set([BE, AB]); True 290304000000.0
    BE: set([AB, BC]); True 290304000000.0
    AB: set([BE, BC]); True 290304000000.0
    BC: set([AB, CD]); True 356165071662.0
    BC: set([AB, CE]); True 446952246792.0
    BE: set([AB, CE]); True 995328000000.0
    BC: set([BE, CD]); True 2.67123803747e+12
    BC: set([CE, CD]); True 4.11264e+12
    CE: set([CD, BC]); True 4.11264e+12
    CD: set([CE, BC]); True 4.11264e+12
    BC: set([BE, CE]); True 4.19017731367e+12
    BE: set([CE, BC]); True 7.2576e+12
    CE: set([BE, BC]); True 8.38035462734e+12
    CE: set([BE, CD]); True 9.15853041417e+12
    
    IMPLICATION)
    -- in the long run this would be realized in distributed system.
    -- then we may go by differnt path according to other metrics (network reliability)
    
    """
    

    def div_int_lf_rg(self):
        """ input: two TMs and related tables """
        leftTbls = self.getQueryGraph().items()[0][1]
        rightTbls = self.getQueryGraph().items()[1][1]
        intersection = leftTbls.intersection(rightTbls)
        left = leftTbls.difference(intersection)
        right = rightTbls.difference(intersection)
        """ left: normal tables exclusive to left TM """
        """ output left == right: sets of normal tables, leftTM, rightTM """
        return left, intersection, right, self._graph.items()[0][0], self._graph.items()[1][0]
        """ each set of normal tables may not be more than one as TM_cluster """
    
    def cost_join_nl(self, key_node, node):
        return key_node.card*node.card

    def updateExpCard(self):
        for mJU in self.mJUlist:
            None
    
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

    def nano_opt(self, cost_join = cost_join_nl):
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
    
        lfOnly, intersection, rghOnly, leftTM, rightTM = self.div_int_lf_rg(query_dc.getQueryGraph_vk())
        """ output: lfOnly, intersection, rghOnly:set of tbls; leftTM, rightTM: TM """
        """ TO-DO: write processPredicate(tbl, TM) """
        
        self.processPredicate(lfOnly, leftTM, cost_join)
        self.processPredicate(rghOnly, rightTM, cost_join)
        if leftTM.getCard() > rightTM.getCard(): # apply predicates intersection where card is lower
            self.processPredicate(intersection, rightTM, cost_join)
        else:
            self.processPredicate(intersection, leftTM, cost_join)
        return self.processJoin_nl(leftTM, rightTM) # nested loop join
    
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

    

        


    #### TO-DO: have to update total cost
    """ UPDATE this function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! URGENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    def clearNonUDFPred(self, costFunction):
        None
        """ AFTER cleared multi preds in a single table """
        """TO-DO: to update LR-tbls: NO may be necessary for UDF later"""
        """TO-DO: do nothing when doesn't have any predicates"""
"""        # to get keys in the graph
        keys = self._graph.keys()
        # apply each predicate to an associated TM with the lowest card
        has_normTbl = False
        for key in keys:
            if key.TMbool == False: # have to check as TM does not have 
                has_normTbl = True
                key_sel = key.norm_preds[0].sel
                if key_sel != 1.0:
                    temp = key
                    temp_low = float("inf")
                    for node in self._graph[key]:
                        if temp_low > node.card:
                            temp_low = node.card
                            temp = node
                    temp.card = temp.card*key_sel
                    temp.cum_cost += (key.cum_cost + costFunction(key.norm_preds[0], temp))
        # delete all normal tables without UDF (UDF not assumed as of 1/4/2017)
        if (has_normTbl==True):
            for key in keys:
                temp_list = []
                # 
                for node in self._graph[key]:
                    temp_list.append(node)
                    if len(temp_list) == 1:
                        pass
                    else:
                        # this is possible when only dealing with the predicates table (normal table)
                        import itertools
                        elements = [list(x) for x in itertools.combinations(temp_list, 2)]
                        for nodes in elements:
                            # add new connectinos among TMs
                            self.add(nodes[0],nodes[1])
                # delete all normal tables
                del self._graph[key]


"""


###############################
# test1) create a query and clear multiple predicates in a single table
#### ===>> SUCCESS
###############################
def test1():   
    qry = oft.prep_query0()
    optimizer = Optimizer(query = qry)
    optimizer.snapshot_query()
    optimizer.processNorm_preds()
    optimizer.snapshot_query()
#test1()


###############################
# test1) to make sure that temp_pred created would not but repetative
#### ===>> SUCCESS
###############################

def test2():
    qry = oft.prep_query0()
    optimizer = Optimizer(query = qry)
    optimizer.processNorm_preds()

    keys = optimizer.query.getKeys()
    keys[0].norm_preds.preds[0].sel = 0.2
    print keys[0].norm_preds.preds[0].sel
    print keys[2].norm_preds.preds[0].sel

#test2()


