# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 14:48:48 2017

@author: HKIM85
"""

import predicate as pds
import Table1_1 as tbl
import query1_1 as qry
import Fanout as fo
import microJU as mju
import utilities as utl
import ExpMtrcs_tbl as emt
import time
"""                      """
""" PREDICATE/PREDICATES """
"""                      """
""" CAUTION: Any name of either pred or preds must not be repeated!!! """

def prep_preds00():
    pred00 = pds.Predicate(pred_name = 'pred00', norm_sel_bool = True)
    preds00 = pds.Predicates()
    preds00.add(pred00)
    return preds00

def prep_preds0():
    pred0 = pds.Predicate(pred_name = 'pred0', norm_sel_bool = True)          
    pred0_1 = pds.Predicate(pred_name = 'pred0_1', norm_sel_bool = True)
    pred0_2 = pds.Predicate(pred_name = 'pred0_2', norm_sel_bool = True)
    # 
    pred0.setSel(sel = 0.8)
    pred0_1.setSel(sel = 0.6)
    pred0_2.setSel(sel = 0.4)
    
    preds0 = pds.Predicates()
    preds0.add(pred0)
    preds0.add(pred0_1)
    preds0.add(pred0_2)
    return preds0


    
def prep_preds1():
    pred1 = pds.Predicate(pred_name = 'pred1', norm_sel_bool = True)          
    # 
    pred1.setSel(sel = 0.8)
    preds1 = pds.Predicates()
    preds1.add(pred1)
    return preds1
    
def prep_preds2():
    pred2 = pds.Predicate(pred_name = 'pred2', norm_sel_bool = True)
    # 
    pred2.setSel(sel = 0.6)
    
    preds2 = pds.Predicates()
    preds2.add(pred2)
    return preds2    

""" TABLE """

def prep_query0():
    preds0 = prep_preds0()
    preds1 = prep_preds1()
    preds2 = prep_preds2()
    A = tbl.Table('A', card = 100000, cum_cost = 0, preds = preds0)
    B = tbl.Table('B', card = 100000, cum_cost = 0, preds = preds1)
    C = tbl.Table('C', card = 100000, cum_cost = 0, preds = preds2)
    AB = tbl.TM(table_name='AB', card = 150000, cum_cost = 0)
    BC = tbl.TM(table_name='BC', card = 200000, cum_cost = 0)
    
    conn = [(A, AB), (B ,AB), (B ,BC), (C, BC)]
    query = qry.Query(conn, directed=True) 
    
    return query
    


""" QUERY """


""" PREDICATES FOR MICRO OPTIMIZATION TEST CASE1 """
def prep_preds3():
    pred3 = pds.Predicate(pred_name = 'pred3', norm_sel_bool = True)
    pred3.setSel(sel = 0.9)  
    preds3 = pds.Predicates()
    preds3.add(pred3)
    return preds3


def prep_preds4():
    pred4 = pds.Predicate(pred_name = 'pred4', norm_sel_bool = True)
    pred4.setSel(sel = 0.8)
    preds4 = pds.Predicates()
    preds4.add(pred4)
    return preds4
    
def prep_preds5():    
    pred5 = pds.Predicate(pred_name = 'pred5', norm_sel_bool = True)
    pred5.setSel(sel = 0.8)
    preds5 = pds.Predicates()
    preds5.add(pred5)
    return preds5

def prep_preds6():
    pred6 = pds.Predicate(pred_name = 'pred6', norm_sel_bool = True)
    pred6.setSel(sel = 0.8)
    preds6 = pds.Predicates()
    preds6.add(pred6)
    return preds6

def prep_preds7():
    pred_0_6 = pds.Predicate(pred_name = 'pred_0_6', norm_sel_bool = True)
    pred_0_6.setSel(sel = 0.6)
    preds7 = pds.Predicates()
    preds7.add(pred_0_6)
    return preds7
    
def prep_preds8():
    pred_0_4 = pds.Predicate(pred_name = 'pred_0_4', norm_sel_bool = True)
    pred_0_4.setSel(sel = 0.4)
    pred_0_7 = pds.Predicate(pred_name = 'pred_0_7', norm_sel_bool = True)
    pred_0_7.setSel(sel = 0.7)
    preds8 = pds.Predicates()
    preds8.add(pred_0_4)
    preds8.add(pred_0_7)
    return preds8
    
def pred_query1():
    preds3 = prep_preds3()
    preds4 = prep_preds4()
    preds5 = prep_preds5()
    preds6 = prep_preds6()
    SCP = tbl.Table(table_name = 'SCP', card = 1500, cum_cost = 0, preds = preds3)
    CC = tbl.Table(table_name = 'CC', card = 10000, cum_cost = 0, preds = preds4)
    SCP_CC = tbl.TM(table_name='SCP_CC', card = 12000, cum_cost = 0)
    UCS = tbl.Table(table_name = 'UCS', card = 20000, cum_cost = 0, preds = preds5)
    CC_UCS = tbl.TM(table_name='CC_UCS', card = 16000, cum_cost = 0)
    EC = tbl.Table(table_name = 'EC', card = 10000, cum_cost = 0, preds = preds6)
    UCS_EC = tbl.TM(table_name='UCS_EC', card = 8000, cum_cost = 0)
    
    conn = [(SCP, SCP_CC), (CC, SCP_CC), (CC, CC_UCS), (UCS, CC_UCS), (UCS, UCS_EC), (EC, UCS_EC)]
    query = qry.Query(conn, directed=True)
    
    return query
    
def pred_query2():
    """ test case for nano optimization """
    preds6 = prep_preds6()
    preds7 = prep_preds7()
    preds8 = prep_preds8()
    A = tbl.Table(table_name = 'A', card = 5000, cum_cost = 0, preds = preds6)
    B = tbl.Table(table_name = 'B', card = 5000, cum_cost = 0, preds = preds7)
    AB = tbl.TM(table_name='AB', card = 10000, cum_cost = 0)
    C = tbl.Table(table_name = 'C', card = 5000, cum_cost = 0, preds = preds8)
    BC = tbl.TM(table_name='BC', card = 10000, cum_cost = 0)
    
    conn = [(A, AB), (B, AB), (B, BC), (C, BC)]
    query = qry.Query(conn, directed=True)
    return query

def pred_query3():
    """ test case for nano optimization """
    preds5 = prep_preds5()
    preds6 = prep_preds6()
    preds7 = prep_preds7()
    preds8 = prep_preds8()
    A = tbl.Table(table_name = 'A', card = 5000, cum_cost = 0, preds = preds6)
    B = tbl.Table(table_name = 'B', card = 5000, cum_cost = 0, preds = preds7)
    AB = tbl.TM(table_name='AB', card = 10000, cum_cost = 0)
    C = tbl.Table(table_name = 'C', card = 5000, cum_cost = 0, preds = preds8)
    BC = tbl.TM(table_name='BC', card = 10000, cum_cost = 0)
    D = tbl.Table(table_name = 'D', card = 6000, cum_cost = 0, preds = preds5)
    
    conn = [(A, AB), (D, AB), (B, AB), (B, BC), (C, BC)]
    query = qry.Query(conn, directed=True)
    return query
    
def pred_query4():
    """ test case for nano optimization """
    preds5 = prep_preds5()
    preds6 = prep_preds6()
    preds7 = prep_preds7()
    preds8 = prep_preds8()
    A = tbl.Table(table_name = 'A', card = 5000, cum_cost = 0, preds = preds6)
    B = tbl.Table(table_name = 'B', card = 5000, cum_cost = 0, preds = preds7)
    AB = tbl.TM(table_name='AB', card = 10000, cum_cost = 0)
    C = tbl.Table(table_name = 'C', card = 5000, cum_cost = 0, preds = preds8)
    BC = tbl.TM(table_name='BC', card = 10000, cum_cost = 0)
    D = tbl.Table(table_name = 'D', card = 6000, cum_cost = 0, preds = preds5)
    
    conn = [(A, AB), (D, AB), (B, AB), (B, BC), (C, BC)]
    query = qry.Query(conn, directed=True)
    return query

def pred_query5():
    """ test case for nano optimization """
    preds5 = prep_preds5()
    preds6 = prep_preds6()
    preds7 = prep_preds7()
    preds8 = prep_preds8()
    A = tbl.Table(table_name = 'A', card = 5000, cum_cost = 0, preds = preds6)
    B = tbl.Table(table_name = 'B', card = 5000, cum_cost = 0, preds = preds7)
    AB = tbl.TM(table_name='AB', card = 10000, cum_cost = 0)
    C = tbl.Table(table_name = 'C', card = 5000, cum_cost = 0, preds = preds8)
    BC = tbl.TM(table_name='BC', card = 10000, cum_cost = 0)
    D = tbl.Table(table_name = 'D', card = 6000, cum_cost = 0, preds = preds5)
    
    conn = [(A, AB), (D, AB), (B, AB), (B, BC), (C, BC)]
    query = qry.Query(conn, directed=True)
    return conn, query

def getMicroJUlist(query, excldShort = True):
    import itertools
    """ midTM, linked TM set ==> combination of link set ==> create MicroJU 
        ==> append to JUlist """
    mJUlist = mju.MicroJUlist([])
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
                microJU = mju.MicroJU(TM1, query)
                microJU.addOtherTMs(TM3)
                microJU.addOtherTMs(TM4)
                #print 'microJU:', microJU
                mJUlist.append(microJU)
    return mJUlist

""" for testing only """
""" delete after testing"""
#tic = time.time()*1000000000
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
query = qry.Query(conn, directed=True) 
#toc= time.time()*1000000000
#print "query graph fetch", (toc-tic)
#conn = [(A, AB), (B, AB), (B, BC), (C, BC)]
#conn = [(A, AB), (B, AB)]


""" ############################################### """
""" TO-DO make sure that norm_pred has been cleared """
""" ############################################### """

"""
# clear predicates
# get table
tbl11 = query.getKeys()[0]
# get norm_selectivity
sel = tbl11.get_exp_norm_sel()

mJUlist = getMicroJUlist(query)
"""

"""
mJU cost card 
"""
#mJU = mJUlist.getMJUlist()[0]
""" get three TMs """
#midTM = mJU.getMidTM() #BC
#LTM = mJU.getLTM() # CE
#RTM = mJU.getRTM() # CD

""" get connected tbls to each TM """
"""
midTM_tbls = mJU.getMTM_tbls()
LTM_tbls = mJU.getLTM_tbls()
RTM_tbls = mJU.getRTM_tbls()
"""

""" DIVIDE AND CONQUER """
""" (1) mid_TM = LTM vs. midTM = RTM """
"""
for table in midTM_tbls:
    sel_list = table.getNormSelList()
    tbl_card = table.getCard()
    pred_cost = 0.0
"""  

""" TO-DO distinguish functions for rough """
def cal_agg_exp_sel(tbl_set):
    """ A method that aggregate all predicates 
    output 1.0 when there is no predicates in a table 
    input: set of tbls """
    temp_sel = 1.0
    for table in list(tbl_set): temp_sel *= table.get_exp_norm_sel()
    return temp_sel


def get_conn_tbls(query, mJU):
    query_vk = query.getQuery_vk()
    return query_vk.getValues(mJU.getMidTM()).union(query_vk.getValues(mJU.getLTM())).union(query_vk.getValues(mJU.getRTM()))

""" 
get_conn_tbls(query, mJUlist.getMJUlist()[0])   
    
tbl_set = midTM_tbls.union(LTM_tbls).union(RTM_tbls)
"""

""" product of all nor_pred_sel """
#cal_agg_exp_sel(tbl_set)

def cal_agg_prod_card(*TM_list):
    """ A function that cal. product of cardinalities 
        input: a list of TMs """
    temp_card = 1
    for TM in TM_list: temp_card *= TM.getCard()
    return temp_card

""" product of all TM. card """
#cal_agg_prod_card(midTM, LTM, RTM)

""" get lowest fanout """
#midTM.getLowestFO(LTM)
#midTM.getLowestFO(RTM)


""" update expected """
"""
for mJU in mJUlist.getMJUlist():
    res = cal_agg_exp_sel(get_conn_tbls(query, mJU)) * cal_agg_prod_card(mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()) * mJU.getMidTM().getLowestFO(mJU.getLTM()).getFO() *mJU.getMidTM().getLowestFO(mJU.getRTM()).getFO()
    mJU.setEstCard(res)

for mJU in mJUlist.getMJUlist():
    midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
    res = cal_agg_exp_sel(get_conn_tbls(query, mJU)) * cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
    mJU.setEstCard(res)

mJUlist.getMJUlist()[1].getEstCard()
mJUlist.getMJUlist().sort(key = lambda mJU: mJU.getEstCard())
"""

"""
for mJU in mJUlist.getMJUlist():
    print mJU, mJU.getExpCard()
"""



""" update expected cost """

#mJUlist = getMicroJUlist(query)
#mJU = mJUlist.getMJUlist()[0]


# mJUlist_display(mJUlist)

""" get three TMs """
"""
MTM = mJU.getMidTM() #BC
LTM = mJU.getLTM() # BE
RTM = mJU.getRTM() # AB
"""
""" get connected tbls to each TM """
"""
MTM_tbls = mJU.getMTM_tbls()
LTM_tbls = mJU.getLTM_tbls()
RTM_tbls = mJU.getRTM_tbls()
"""

A.getNormPreds()
""" get selectivity of preds """
def getPredSel_list(table):
    return [pred.sel for pred in [pred for pred in table.getNormPreds() if pred.norm_sel_bool == True]]

# tmp_sel = [pred.sel for pred in [pred for pred in A.getNormPreds() if pred.norm_sel_bool == True]]
# tmp_sel

""" get preds """
def getPred_list(table):
    return [pred for pred in [pred for pred in table.getNormPreds() if pred.norm_sel_bool == True]]

# tmp_pred = [pred for pred in [pred for pred in A.getNormPreds() if pred.norm_sel_bool == True]]
# tmp_pred[2].getSel()



"""
for table in MTM_tbls.union(LTM_tbls).union(RTM_tbls):
    expMtrcsTbl = emt.ExpMtrcs_tbl(table)
    expMtrcsDict.add_predicate_tbl(table, expMtrcsTbl)
"""
    
def initiate_tbl_est_metrics(table, expMtrcsDict):
    """ initiate table estimated metrics to _tbls """
    expMtrcsDict.add_predicate_tbl(table, emt.ExpMtrcs_tbl(table))
    
def initiate_tbls_est_metrics(mJU, expMtrcsDict):
    """ initiate estimated metrics of tables in micro JU """
    for table in mJU.getMTM_tbls().union(mJU.getLTM_tbls()).union(mJU.getRTM_tbls()):
        initiate_tbl_est_metrics(table, expMtrcsDict)

def initiate_TM_est_metrics(TM, expMtrcsDict):
    """ initiate estimated metrics of a TM to _TMs """
    expMtrcsDict.add_predicate_TM(TM, emt.ExpMtrcs_TM(TM))

def initiate_TMs_est_metrics(mJU, expMtrcsDict):
    """ initiate estimated metrics of a TM to _TMs """
    initiate_TM_est_metrics(mJU.getMidTM(), expMtrcsDict)
    initiate_TM_est_metrics(mJU.getLTM(), expMtrcsDict)
    initiate_TM_est_metrics(mJU.getRTM(), expMtrcsDict)
    
def initiate_tbls_TMs_est_mtrcs(mJU):
    expMtrcsDict = emt.ExpMtrcs_dict()
    initiate_tbls_est_metrics(mJU, expMtrcsDict)
    initiate_TMs_est_metrics(mJU, expMtrcsDict)
    return expMtrcsDict

#expMtrcsDict = initiate_tbls_TMs_est_mtrcs(mJU)


""" 
TEST:
    deepcopy 
when attrribute is called by getters 
"""
"""
expMtrcsDict.getTblGraph().keys()
expMtrcsDict.getTblGraph()[E].get_exp_card() 
expMtrcsDict.getTblGraph()[E].set_exp_card(10000)
expMtrcsDict.getTblGraph()[E].get_exp_card() 
expMtrcsDict.getTblGraph()[E].set_exp_card(E.getCard())
expMtrcsDict.getTblGraph()[E].get_exp_card() 
E.getCard()
"""



""" E BE - B - BC - B - AB - A  """
"""
p1 = MTM_tbls.intersection(LTM_tbls) # mid & LTM: B
p2 = RTM_tbls.intersection(MTM_tbls) # RTM & mid: B
p3 = LTM_tbls.intersection(RTM_tbls) # LTM & RTM: B

p4 = MTM_tbls.intersection(LTM_tbls).intersection(RTM_tbls) # mid & LTM & RTM: B
p1_4 = p1.difference(p4)
p2_4 = p2.difference(p4)
p3_4 = p3.difference(p4)
p5 = MTM_tbls.difference(p1).difference(p2) # C
p6 = RTM_tbls.difference(p2).difference(p3) # A
p7 = LTM_tbls.difference(p3).difference(p1) # E
"""
"""
Three sets
p1_4 = MTM_tbls.intersection(LTM_tbls) # mid & LTM: B
p2_4 = RTM_tbls.intersection(MTM_tbls) # RTM & mid: B
p3_4 = LTM_tbls.intersection(RTM_tbls) # LTM & RTM: B
p1 = p1_4.difference(RTM_tbls)
p2 = p2_4.difference(LTM_tbls)
p3 = p3_4.difference(MTM_tbls)
p4 = MTM_tbls.intersection(LTM_tbls).intersection(RTM_tbls) # mid & LTM & RTM: B
p4 = p1_4.intersection(p2_4)
p5 = MTM_tbls.difference(p1_4).difference(p2)
p6 = RTM_tbls.difference(p2_4).difference(p3)
p7 = LTM_tbls.difference(p3_4).difference(p1)
"""



"""
TWO SETS
"""
""" LTM = MTM """
"""
p1_4 = MTM_tbls.intersection(LTM_tbls) # mid & LTM: B
p3_7 = LTM_tbls.difference(p1_4)
p2_5 = MTM_tbls.difference(p1_4)
"""


"""
for table in p1_4:
    print table, table.getProdNormSel()
table.getNormPreds()[0].getSel()
list(p1_4)[0].getNormPreds()[0].getSel()
list(p3_7)[0].getNormPreds()[0].getSel()
list(p2_5)[0].getNormPreds()[0].getSel()
"""


"""
for table in p3_7:
    table.getProdNormSel()
    mJU.getExpMtrcsDict().getTblGraph()[table]
""" 

def cost_norm_preds(table):
    return table.card



""" 
mJU.getExpMtrcsDict().getTblGraph()[A]

A.getProdNormSel()
type(A.getNormPreds())
table_est_mtrc = mJU.getExpMtrc_tbl(A)
table_est_mtrc.set_exp_card(A.getCard())
table_est_mtrc
"""



""" clear norm_preds """
"""
# cost of table scan
expMtrcsDict.getExpMtrc_tbl(A).add_exp_cum_cost(cost_norm_preds(A))
# update est. cardinality
expMtrcsDict.getExpMtrc_tbl(A).update_exp_card(A.getProdNormSel())
# 
preds = A.getNormPreds()
expMtrcsDict.getExpMtrc_tbl(A).clear_all_norm_preds_todo(preds)
expMtrcsDict.getExpMtrc_tbl(A)
#getExpMtrc_tbl(A).get_norm_preds_todo() = [pred for pred in p_todo if pred not in preds]
# set norm_pred_done: YES
"""

""" clear norm predicates in mJU """
# initiates 
"""
mJU.initiate_tbls_TMs_est_mtrcs()
expMtrcsDict = mJU.getExpMtrcsDict()
expMtrcsDict.getTblGraph()
"""

""" initial set up """
"""
for table in expMtrcsDict.getTblGraph().keys():
    # cost of table scan
    expMtrcsDict.getExpMtrc_tbl(table).add_exp_cum_cost(cost_norm_preds(table))
    # update est. cardinality
    expMtrcsDict.getExpMtrc_tbl(table).update_exp_card(table.getProdNormSel())
    # clear predicate to_do list
    expMtrcsDict.getExpMtrc_tbl(table).clear_all_norm_preds_todo(table.getNormPreds())
"""
#expMtrcsDict

#expMtrcsDict.getExpMtrc_tbl(A).get_norm_preds_done()

#mJU.initiate_tbls_TMs_est_mtrcs()
"""
list(mJU.otherTMs)[0]
sorted(mJU.otherTMs)[0]

mJU.expMtrcsDict

mJU.initiate_tbls_TMs_est_mtrcs()
mJU.getExpMtrcsDict().getExpMtrc_tbl(E).get_norm_preds_done()
mJU.getExpMtrcsDict().getExpMtrc_tbl(B)

p_todo = mJU.getExpMtrcsDict().getExpMtrc_tbl(B).get_norm_preds_todo()
preds = A.getNormPreds()

C.card
"""


"""
def update_normPreds_ExpMtrcsDict(mJU):
    expMtrcsDict = mJU.getExpMtrcsDict()
    for table in expMtrcsDict.getTblGraph().keys():
        expMtrcs_tbl = expMtrcsDict.getExpMtrc_tbl(table)
        # cost of table scan
        expMtrcs_tbl.add_exp_cum_cost(cost_norm_preds(table))#.update_exp_card(table.getProdNormSel()).grab_all_norm_preds_todo(table.getNormPreds())
        # update est. cardinality
        expMtrcs_tbl.update_exp_card(table.getProdNormSel())
        # clear predicate to_do list
        expMtrcs_tbl.grab_all_norm_preds_todo(table.getNormPreds())
        # update norm_preds_done
        expMtrcs_tbl.update_preds_done()

def update_normPreds_ExpMtrcsDict_mJUlist(mJUlist):
    for mJU in mJUlist.getMJUlist():
        mJU.initiate_tbls_TMs_est_mtrcs()   # initiate tbls TM metrics
        update_normPreds_ExpMtrcsDict(mJU)  # update table scan cost, update exp card, update predicate to do list, update nor_pred_done boolean
"""
"""
mJU.initiate_tbls_TMs_est_mtrcs()
mJU.getExpMtrcsDict().getTblGraph()[B]
mJU.getExpMtrcsDict().getTMGraph()

#update_normPreds_ExpMtrcsDict(mJU)
update_normPreds_ExpMtrcsDict_mJUlist(mJUlist)
"""


"""
e.g) AB  join BC
res = {x:AB.getFanouts().getGraph()[x] for x in AB.getFanouts().getGraph() if x in BC.getFanouts().getGraph()}
mJU 

res1  = [x[0] for x in res.values()]
res1.sort(key=lambda fanout: fanout.getFO()) # get fanout 

res1[0].getFO()
"""

# cost of join


# est. card.
#res1[0].getFO()*



"""
for mJU in mJUlist.getMJUlist():
    print mJU
mJUlist.getMJUlist()[10].getExpMtrcsDict()
""" 

""" check if all norm_preds are cleared """
"""
mJUlist.getMJUlist()[0].getExpMtrcsDict()
mJUlist.getMJUlist()[4].getExpMtrcsDict()
mJUlist.getMJUlist()[8].getExpMtrcsDict()
"""

""" update estimated metrics in all mJU """
"""
for mJU in mJUlist.getMJUlist():
    mJU.initiate_tbls_TMs_est_mtrcs()
    update_normPreds_ExpMtrcsDict(mJU)
"""

"""
for mJU in mJUlist.getMJUlist():
    mJU.initiate_tbls_TMs_est_mtrcs()
""" 


"""
TEST: initiate mJUlist ==> update all metrics
"""
#mJUlist = getMicroJUlist(query)
#mJUlist.initiate_tbls_TMs_est_mtrcs() ### initiate
"""
mJU = mJUlist.getMJUlist()[7]
mJU.getExpMtrcsDict().getExpMtrc_tbl(C)

MTM = mJU.getMidTM() #BC
LTM = mJU.getLTM() # BE
RTM = mJU.getRTM() # AB
"""

""" get connected tbls to each TM """
"""
MTM_tbls = mJU.getMTM_tbls()
LTM_tbls = mJU.getLTM_tbls()
RTM_tbls = mJU.getRTM_tbls()
"""

"""
TWO SETS
"""
"""
MTM_card = MTM.getCard()
LTM_card = LTM.getCard()
RTM_card = RTM.getCard()
"""

#p3_4 = LTM_tbls.intersection(RTM_tbls) # LTM & RTM: B





def getProdNormSel_set(table_set):
    prod_sel = 1.0
    for tbl1 in table_set: prod_sel *= tbl1.getProdNormSel()
    return prod_sel

#MTM_card*getProdNormSel_set(p2_5)
#LTM_card*getProdNormSel_set(p3_7)


def toMTM(MTM_card, otherTM_card, MTM_tbls, otherTM_tbls):
    return MTM_card*getProdNormSel_set(MTM_tbls) <= otherTM_card*getProdNormSel_set(otherTM_tbls)

#MTM_card + LTM_card + (MTM_card*LTM_card*)

utility = utl.Utilities()


def get_lower_est_cost_mJU(MTM_card, otherTM_card, tbls_Monly, tbls_otherOnly, tbls_intersection, costF_join, norm_p_costF):
    """ input: MTM_card, otherTM_card, tbls_Monly, tbls_otherOnly, tbls_intersection, """
    MTM_card_ = MTM_card * getProdNormSel_set(tbls_Monly) # intermedicate MTM_card
    otherTM_card_ = otherTM_card * getProdNormSel_set(tbls_otherOnly)
    prodNSel_intrsctn = getProdNormSel_set(tbls_intersection)
    
    res = costF_join(MTM_card_ * prodNSel_intrsctn, otherTM_card_) if (MTM_card_ <= otherTM_card_) else costF_join(MTM_card_, otherTM_card_ * prodNSel_intrsctn)
    res += (norm_p_costF(MTM_card) + norm_p_costF(otherTM_card)) # norm_pred scan cost
    return res
    """
    if (toMTM(MTM_card, otherTM_card, tbls_Monly, tbls_otherOnly) == True):
        return costFunction(MTM_card_int * prodNormSel_intersection, otherTM_card_int)
    else:
        return costFunction(MTM_card_int, otherTM_card_int * prodNormSel_intersection)
    """

    def cost_join_nl_by_card(self, TM1_card, TM2_card):
        if (TM1_card <= TM2_card):
            return TM1_card + TM1_card * TM2_card
        else:
            return TM2_card + TM1_card * TM2_card

A.getProdNormSel()
B.getProdNormSel()
C.getProdNormSel()
D.getProdNormSel()

""" ############################################### """
""" TEST: get_lower_est_cost_mJU                    """
""" ############################################### """
"""
MTM_card = 6000
otherTM_card = 10000
MTM_card_ = MTM_card * getProdNormSel_set({A}) # intermedicate MTM_card
otherTM_card_ = otherTM_card * getProdNormSel_set({B,C})
prodNSel_intrsctn = getProdNormSel_set({D})
    

res = utility.cost_join_nl_by_card(MTM_card_ * prodNSel_intrsctn, otherTM_card_) if (MTM_card_ <= otherTM_card_) else utility.cost_join_nl_by_card(MTM_card_, otherTM_card_ * prodNSel_intrsctn)
res += ( utility.cost_table_scan(MTM_card) +  utility.cost_table_scan(otherTM_card)) # n

get_lower_est_cost_mJU(6000, 10000, {A} , {B, C}, {D}, utility.cost_join_nl_by_card, utility.cost_table_scan)
"""
"""
MTM = mJU.getMidTM() #BC
LTM = mJU.getLTM() # BE
RTM = mJU.getRTM() # AB

#mJU.getEstJnCst_mJU()


MTM_tbls = mJU.getMTM_tbls()
LTM_tbls = mJU.getLTM_tbls()
RTM_tbls = mJU.getRTM_tbls()

MTM_card = MTM.getCard()
LTM_card = LTM.getCard()
RTM_card = RTM.getCard()

p1_4 = MTM_tbls.intersection(LTM_tbls) 
p2_5 = MTM_tbls.difference(p1_4)
p3_7 = LTM_tbls.difference(p1_4)

p2_4 = MTM_tbls.intersection(RTM_tbls)
p1_5 = MTM_tbls.difference(p2_4)
p3_6 = RTM_tbls.difference(p2_4)

M_LTM_cost = get_lower_est_cost_mJU(MTM_card, LTM_card, p2_5, p3_7, p1_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
M_RTM_cost = get_lower_est_cost_mJU(MTM_card, RTM_card, p1_5, p3_6, p2_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
#mJU.addEstCost(min(M_LTM_cost,M_RTM_cost))
"""

def getEstJnCst_mJU(mJU):
    """ get connected tbls to each TM """
    MTM_tbls, LTM_tbls, RTM_tbls = mJU.getMTM_tbls(), mJU.getLTM_tbls(), mJU.getRTM_tbls()
    
    """ TWO SETS """
    MTM_card, LTM_card, RTM_card = mJU.getMidTM().getCard(), mJU.getLTM().getCard(), mJU.getRTM().getCard()

    """ LTM = MTM """
    p1_4 = MTM_tbls.intersection(LTM_tbls)
    p2_5, p3_7 = MTM_tbls.difference(p1_4), LTM_tbls.difference(p1_4)

    """ MTM = RTM """
    p2_4 = MTM_tbls.intersection(RTM_tbls)
    p1_5, p3_6 = MTM_tbls.difference(p2_4), RTM_tbls.difference(p2_4)

    M_LTM_cost = get_lower_est_cost_mJU(MTM_card, LTM_card, p2_5, p3_7, p1_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
    M_RTM_cost = get_lower_est_cost_mJU(MTM_card, RTM_card, p1_5, p3_6, p2_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
    #mJU.addEstCard(min(M_LTM_cost,M_RTM_cost))
    return (min(M_LTM_cost,M_RTM_cost))

def getEstJnCst_mJU_exst(mJU):
    """ get connected tbls to each TM """
    MTM_tbls, LTM_tbls, RTM_tbls = mJU.getMTM_tbls(), mJU.getLTM_tbls(), mJU.getRTM_tbls()
    
    """ TWO SETS """
    MTM_card, LTM_card, RTM_card = mJU.getMidTM().getCard(), mJU.getLTM().getCard(), mJU.getRTM().getCard()

    """ LTM = MTM """
    p1_4 = MTM_tbls.intersection(LTM_tbls)
    p2_5, p3_7 = MTM_tbls.difference(p1_4), LTM_tbls.difference(p1_4)

    """ MTM = RTM """
    p2_4 = MTM_tbls.intersection(RTM_tbls)
    p1_5, p3_6 = MTM_tbls.difference(p2_4), RTM_tbls.difference(p2_4)

    M_LTM_cost = get_lower_est_cost_mJU(MTM_card, LTM_card, p2_5, p3_7, p1_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
    M_RTM_cost = get_lower_est_cost_mJU(MTM_card, RTM_card, p1_5, p3_6, p2_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
    #mJU.addEstCard(min(M_LTM_cost,M_RTM_cost))
    return (min(M_LTM_cost,M_RTM_cost))


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
    
    def hasLTM(self):
        return self.hasLTM
    
    def __repr__(self):
        return '((MTM: {}); (otherTM: {}); hasLTM: {})'.format(self.MTM, self.otherTM, self.hasLTM )

            
class TM_join_nju(object):
    def __init__(self, tm_join_nju_pre):  #mJU, hasLTM = True, joinCostF = utl.Utilities().cost_join_nl_by_card):
        self.MTM = tm_join_nju_pre.getMJU().getMTM()
        #self.MTMName = MTM.getTableName()
        self.MTMCard = self.MTM.getCard()
        self.otherTM = tm_join_nju_pre.getMJU().getLTM() if hasLTM else tm_join_nju_pre.getMJU().getRTM()
        self.otherTMCard = self.otherTM.getCard()
        self.hasLTM = tm_join_nju_pre.hasLTM() # if hasLTM this.TMjoin is left nano Junit
        self.ClsTM = (self.MTM, self.otherTM)
        self.ClsTMCard = None ### if None: It hasn't been processed.
        self.costTMjoin = 0.0
        self.joinCostF = joinCostF
        
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
    
    #def setCostTMjoin(self, cost):
    #    self.costTMjoin = cost
        
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
    
    def getTblProdNormSel(self):
        return self.tblProdNormSel
    
    def getIsOnly(self):
        return self.isOnly
    
    def getIsMTM(self):
        return self.isMTM
    
    def getCostPred(self):
        return self.costPred
    
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
        predsMTMonly = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = True, isMTM = True) for table in tbls_MTMonly if table.has_normPred()]
        predsMotherTMboth = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = False, isMTM = True) for table in tbls_inter if table.has_normPred()]
        predsOtherTMonly = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = True, isMTM = False) for table in tbls_otherTMonly if table.has_normPred()]
        self.predsLoTMonly = [normPred_nju_pre(mJU, table, isLeft = self.isLeft, isOnly = True, isMTM = False) for table in tbls_loTMonly if table.has_normPred()]
        self.TM_join = TM_join_nju_pre(mJU, hasLTM = True if self.isLeft else False)
        self.allPredsNjoin =  predsMTMonly + predsOtherTMonly + predsMotherTMboth + [self.TM_join]
        self.cumCost = 0.0
        self.pathList = pathList(self.allPredsNjoin, self)
        """
        """
        
    def getMTM(self):
        return self.MTM
    
    def getOtherTM(self):
        return self.otherTM
    
    def getPathList(self):
        return self.pathList
        
    def getCumcost(self):
        return self.cumCost
    
    def getAllPredsNjoin(self):
        ### 
        return self.allPredsNjoin
    
    def addCumcost(self, cost):
        self.cumCost += cost
        
    def getTbls_liTMonly(self):
        return self.tbls_loTMonly
    
    def __repr__(self):
        return '(All preds:{}; isLeft:{}; cumCost:{})'.format([pred for pred in self.allPredsNjoin], self.isLeft, self.cumCost)
    """
    def __repr__(self):
        return '(MTM:{}; otherTM:{}; isLeft:{}; cumCost:{})'.format(self.MTM, self.otherTM, self.isLeft, self.cumCost)
    """
    
    
class pathList(object):
    """ create permutation and instantiate path object and norm_pred/TMjoin objects """
    def __init__(self, all_ops, nJU):
        """  """
        import itertools    
        self.IntToMTMlist = [path(all_ops, list(path_tup), nJU, IntPtoMTM = True) for path_tup in itertools.permutations(all_ops)]
        self.IntToOtherTMlist = [path(all_ops, list(path_tup), nJU, IntPtoMTM = False) for path_tup in itertools.permutations(all_ops)]
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
    
    def processPres(self, IntToMTM = True, doIntToMTMlist=True):
        for path in self.IntToMTMlist if doIntToMTMlist == True else self.IntToOtherTMlist:
            path.processPath()     
    
    def __repr__(self):
        return '({}, {})'.format(self.IntToMTMlist, self.IntToOtherTMlist)
          
    
class path(object):
    def __init__(self, all_ops, path_tup, nJU, IntPtoMTM = True):
        ### IntPtoMTM Intersection tables to MTM if IntPtoMTM is True else to otherTM
        self.statHolder = self.createStatsDict(all_ops) #dictionary (table, card)
        """ TO-DO: look up methods for dict """
        self.path = path_tup
        self.pathMatObj_list = [] ### this is where stats would be updated
        self.instMatPredObj_list()
        self.cost = [] ### cost of each pred/TMjoin
        self.nJU = nJU        

    def __repr__(self):
        return '(statHolder:{}; path:{}; cost:{})'.format(self.statHolder, self.pathMatObj_list, self.cost)
   
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
            + [self.createStatHolder(op) for op in [all_ops[-1]]])
        return dict((table, card) for table, card in list_tup)
    
    """
    def instantiatePth(self, path_tup):
        temp = []
        for obj in path_tup:
            temp.append(obj, 0)
    """
    
    def getPath(self):
        return self.path
    
    def getStat(self, table):
        try:
            return self.statHolder[table]
        except KeyError:
            pass ## Nonetype error: table doesn't exist in StatHolder
    
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
            self.updateCard(table, self.getStat(table)*pred_obj.getTblProdNormSel())
            
            # join cost
            TM = self.nJU.getMTM() if self.nJU.isMTM() else self.nJU.getOtherTM()
            TMcard = self.getStat(TM)
            tableCard = self.getStat(table)
            temp_cost += utl.Utilities().cost_join_nl_by_card(tableCard, TMcard)
            # update TM card
            self.updateCard(TM, utl.Utilities().card_join_TM_tbl_by_card(TMcard, pred_obj.getTblProdNormSel()))
                
        elif isinstance(pred_obj, TM_join_nju): ### pred obj is TM join
            # TM join cost
            MTM, OtherTM = pred_obj.getMTM(), pred_obj.getOtherTM()
            MTMcard = self.getStat(MTM)
            OtherTMcard = self.getStat(OtherTM)
            temp_cost = utl.Utilities().cost_join_nl_by_card(MTMcard, OtherTMcard)
            # update TMClsCard                
            self.updateCard((MTM, OtherTM), utl.Utilities().card_join_TM_TM_by_card(MTMcard, OtherTMcard, MTM.getLowestFO(OtherTM).getFO()))
            self.updateCost(temp_cost)
            
    
    
B
mJUlist = mju.MicroJUlist().getMicroJUlist(query)
mJUlist = getMicroJUlist(query)
mJU = mJUlist.getMJUlist()[0]

isLeft = True


### create prelist
nju = nJU(mJU, isLeft=True)
nju.getAllPredsNjoin()

def createStatHolder(op):
    """ input instance of normPred_nju or TM_join_nju """
    if isinstance(op, normPred_nju_pre):
        table = op.getTbl()
        return (table, table.getCard())
    elif isinstance(op, TM_join_nju_pre):
        MTM = op.getMTM()
        OtherTM = op.getOtherTM()                                  ### stats for TMcls
        return (MTM, MTM.getCard()), (OtherTM, OtherTM.getCard()), ((MTM, OtherTM), 0)

def createStatsDict(all_ops):
    """ call createStatHolder """
    ### all regular tables and TMs
    list_tup =( [createStatHolder(op) for op in all_ops[0:-1]] 
                + [createStatHolder(op) for op in [all_ops[-1]]])
    return dict((table, card) for table, card in list_tup)
    

""" ### cretaed all stats
createStatsDict(nju.getAllPredsNjoin())

nju.getAllPredsNjoin()[0]
isinstance(nju.getAllPredsNjoin()[0], normPred_nju_pre)
nju.getAllPredsNjoin()[0].getTbl()
nju.getAllPredsNjoin()[0].getTbl().getCard()

createStatHolder(nju.getAllPredsNjoin()[0])

nju.getAllPredsNjoin()[3]
isinstance(nju.getAllPredsNjoin()[3], TM_join_nju_pre)
nju.getAllPredsNjoin()[3].getMTM()
nju.getAllPredsNjoin()[3].getMTM().getCard()

nju.getAllPredsNjoin()[3].getOtherTM()
nju.getAllPredsNjoin()[3].getOtherTM().getCard()

createStatHolder(nju.getAllPredsNjoin()[3])
"""
## ClsTM hasn't instantiated yet

all_ops = nju.getAllPredsNjoin()
list_tup =( [createStatHolder(op) for op in all_ops[0:-1]] 
                + [createStatHolder(op) for op in [all_ops[-1]]])

type(all_ops[-1])

isinstance(all_ops[-1], TM_join_nju_pre)


[createStatHolder(op) for op in [all_ops[-1]]]

import itertools
a = list(itertools.permutations(nju.getAllPredsNjoin()))
len(a)
type(a[0][0])

############################################################################

path_l = pathList(nju.getAllPredsNjoin(), nju)
path_l

### instantiate full pred obj according to path_tup
for pred_obj in a[0]:
    temp_cost = 0.0
    if isinstance(pred_obj, normPred_nju): ### pred obj is table
        # table scan cost
        table = pred_obj.getTbl()
        temp_cost = utl.Utilities().cost_table_scan(self.getStat(table)) # cost of table scan
        # update table card
        self.updateCard(table, self.getStat(table)*pred_obj.getTblProdNormSel())
        
        # join cost
        TM = self.nJU.getMTM() if self.nJU.isMTM() else self.nJU.getOtherTM()
        TMcard = self.getStat(TM)
        tableCard = self.getStat(table)
        temp_cost += utl.Utilities().cost_join_nl_by_card(tableCard, TMcard)
        # update TM card
        self.updateCard(TM, utl.Utilities().card_join_TM_tbl_by_card(TMcard, pred_obj.getTblProdNormSel()))
                
    elif isinstance(pred_obj, TM_join_nju): ### pred obj is TM join
        # TM join cost
        MTM, OtherTM = pred_obj.getMTM(), pred_obj.getOtherTM()
        MTMcard = self.getStat(MTM)
        OtherTMcard = self.getStat(OtherTM)
        temp_cost = utl.Utilities().cost_join_nl_by_card(MTMcard, OtherTMcard) # update cost of TM join
        # update TMClsCard                
        self.updateCard((MTM, OtherTM), utl.Utilities().card_join_TM_TM_by_card(MTMcard, OtherTMcard, MTM.getLowestFO(OtherTM).getFO()))
        self.updateCost(temp_cost)
    
    
a[0]





# pre to full object loop and crete full object tuple ==> check if each path tuple is 




############################################################################



predsMTMonly = [normPred_nju_pre(mJU, table, isOnly = True, isMTM = True, isLeft) for table in tbls_MTMonly if table.has_normPred()]
predsMotherTMboth = [normPred_nju_pre(mJU, table, isOnly = False, isMTM = True, isLeft) for table in tbls_intersection if table.has_normPred()]
predsOtherTMonly = [normPred_nju_pre(mJU, table, isOnly = True, isMTM = False, isLeft) for table in tbls_otherTMonly if table.has_normPred()]

type(nju.getAllPredsNjoin()[0])
isinstance(nju.getAllPredsNjoin()[0], normPred_nju_pre)


### do permutation ==> instanciate normPred_nju_pre



tbls_inter = MTM_tbls.intersection(otherTM_tbls)
tbls_MTMonly, tbls_otherTMonly = MTM_tbls.difference(tbls_inter), otherTM_tbls.difference(tbls_inter)
tbls_loTMonly = loTM_tbls.difference(MTM_tbls).difference(otherTM_tbls)

### created normPred_nju: one per a table
predsMTMonly = [normPred_nju_pre(nju, table, isOnly = True, isMTM = True) for table in tbls_MTMonly if table.has_normPred()]
predsOtherTMonly = [normPred_nju_pre(nju, table, isOnly = True, isMTM = False) for table in tbls_otherTMonly if table.has_normPred()]
predsLoTMonly = [normPred_nju_pre(nju, table, isOnly = True, isMTM = False) for table in tbls_loTMonly if table.has_normPred()]

TM_join = TM_join_nju_pre(nju, hasLTM = True if isLeft else False)

allPredsNjoin =predsMTMonly + predsOtherTMonly + predsLoTMonly + [TM_join]

print '{}'.format([pred for pred in allPredsNjoin])

### permutations 
import itertools
a = list(itertools.permutations(allPredsNjoin))

type(a[0][0])

### create 

a = list(itertools.permutations(allPredsNjoin))


all_ops = allPredsNjoin

type(all_ops)

all_path = itertools.permutations(all_ops)

type(all_path)

type(a[0][0])
isinstance(a[0][0], normPred_nju_pre)
(normPred_nju(a[0][0].getTbl(), nju, a[0][0].getIsOnly(), a[0][0].getIsMTM()))


### create stat dict


### stat instantiate full objects for each preds

### 0) create 






#################################
#need clsTMCard ()
##################################

all_ops[0]

def createStatholder(op):
    """ input instance of normPred_nju or TM_join_nju """
    if isinstance(op, normPred_nju):
        return (op.getTbl(), op.getTblCard())
    elif isinstance(op, TM_join_nju):
        return (op.getMTM(), op.getMTMCard()), (op.getOtherTM(), op.getOtherTMCard()), (op.getClsTMCard())

def createStatsDict(all_ops):
    StatHolder_list = [createStatholder(op) for op in all_ops]
    t =( StatHolder_list[0:-1] 
        + [StatHolder_list[-1][0]] 
        + [StatHolder_list[-1][1]]
        + [StatHolder_list[-1][2]])
    return dict((x,y) for x, y in t)

dict1 = createStatsDict(all_ops)
dict1[CD] =1

dict1.update()

def add(dict1, tbl1, card):
    """ Add connection between node1 and node2 """
    dict1[dict1].add(card)


import itertools
res1 = itertools.permutations(all_ops)


print (type(res1))
for tup in res1:
    print (tup)
    print len(tup)

        

            
res = list(itertools.permutations(all_ops))

""" process a path """
# grip stat dicts and path
dict_path = dict1  ### methods that would check 
path = res[0]

dict_path
dict_path[B]

type(path[0])
isinstance(path[0], normPred_nju)


#1 check if obj is normPred_nju
if isinstance(path[0], normPred_nju):
    path[0].getTbl()
    path[0].getTblCard()
    path[0].getTblProdNormSel()
    ## update table card and pred expense (table scan)
    path[0].setCostPred(0)
    path[0].setCostPred(path[0].getCostPred() + utl.Utilities().cost_table_scan(dict_path[path[0].getTbl()]))
    dict_path[path[0].getTbl()] = dict_path[path[0].getTbl()]*path[0].getTblProdNormSel()
    dict_path[path[0].getTbl()] = 80000
    ## update TM card and pred expensde (table join)
    path[0].setCostPred(path[0].getCostPred() + utl.Utilities().cost_table_scan(path[0].getTblCard()))
    path[0].getCostPred()
    path[0].setCostPred(0)

#2 check if obj is TM_join_nju
if isinstance(path[0], TM_join_nju):

print (type(res))
for tup in res:
    print (tup)

type(res)
res[0]
type(res[0])

res[0][0]
type(res[0][0])
"""
for pred in res:
    print pred
"""
(list(itertools.permutations(all_ops))*2)[0][0].tblCard = 80000
(list(itertools.permutations(all_ops))*2)[1][0].tblCard


res_temp =[]
[res_temp.append(obj) for obj in res]
res_temp

tic = time.time()
for i in range(10000):
    all_ops = all_preds + [TM_join]
    itertools.permutations(all_ops)
toc = time.time()
res = itertools.permutations(all_ops)
print type(res)
[ele for ele in res]
for ele in res:
    print type(ele)

toc-tic

# sort by prod of selectivity
predsMTMonly.sort(key = lambda normPred_nju: normPred_nju.getTblProdNormSel())
### MTMonly cannot be multiple b/c two TMs are connected via one table
### this gives an insight that TM cluster should inherit all UDF predicates from tables
predsLTMonly.sort(key = lambda normPred_nju: normPred_nju.getTblProdNormSel())
predsInsctn.sort(key = lambda normPred_nju: normPred_nju.getTblProdNormSel())

isinstance(all_preds[0], normPred_nju)

res = itertools.permutations(all_preds)

"""
for pred in res:
    print pred
"""
    
mJU.getMTM().getTableName()

""" insctn * 2"""

TM_join.MTMCard
TM_join.MTM
BC.getCard()


class nano_path(object):
    def __init__(self, mJU):
        pass


class normPred_njuList(object):
    def __init__(self, normPred_njuList = []):
        self.normPred_njuList = normPred_njuList
        
    def getNP_njuList(self):
        return self.normPred_njuList
    
    def append(self, normPred_nju):
        if self.excldShort == True:
            # no redendancy/ only full microJU/ 
            if (microJU not in self.mJUlist) and (microJU.getIsLegit()): self.mJUlist.append(microJU)
        else: # full (midTM + twoTMs) and partial microJU
            if (microJU not in self.mJUlist): self.mJUlist.append(microJU)
    

class nJUpathList(object):
    ### nJU: permutation
    def __init__(self, njuPList = [], isLeft = True):
        self.njuPList = njuPList
        self.isLeft = isLeft
        self.cumCost = 0.0
        
    def getNjuPList(self):
        return self.njuPList
    
    def getCumCost(self):
        return self.cumCost
    
    
class nJUpath(object):
    ### def process: 
    ### dynamic stats dictionary;;;; table: card
    def __init__(self, path_tup): # input path_tuple
            
        self.path_tup 

class dd(object):
    
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
        
    
       


"""
predsInsctn  = [normPred_nju(table) for table in tbls_intersection if table.has_normPred()]
otherTM, tbls_intersection, tbls_MTMonly, tbls_otherTMonly
self.MTM, self.otherTM = MTM.getCard(), otherTM.getCard()
self.tblsMTMonly = [(tbl1.getTableName(), tbl1.getProdNormSel()  for tbl1 in tbls_MTMonly if tbl1.has_normPred()]
"""
"""
res = getEstJnCst_mJU(mJUlist.getMJUlist()[0])

mJU = mJUlist.getMJUlist()[0]
### get connected tbls to each TM ###
MTM_tbls = mJU.getMTM_tbls()
LTM_tbls = mJU.getLTM_tbls()
RTM_tbls = mJU.getRTM_tbls()

### TWO SETS ###
MTM = mJU.getMidTM() #
LTM = mJU.getLTM() # 
RTM = mJU.getRTM() # 

MTM_card = MTM.getCard()
LTM_card = LTM.getCard()
RTM_card = RTM.getCard()

### LTM = MTM ###
p1_4 = MTM_tbls.intersection(LTM_tbls) 
p2_5 = MTM_tbls.difference(p1_4)
p3_7 = LTM_tbls.difference(p1_4)

### MTM = RTM ###
p2_4 = MTM_tbls.intersection(RTM_tbls)
p1_5 = MTM_tbls.difference(p2_4)
p3_6 = RTM_tbls.difference(p2_4)

M_LTM_cost = get_lower_est_cost_mJU(MTM_card, LTM_card, p2_5, p3_7, p1_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
M_RTM_cost = get_lower_est_cost_mJU(MTM_card, RTM_card, p1_5, p3_6, p2_4, utility.cost_join_nl_by_card, utility.cost_table_scan)
"""


# get estCost

def updateEstCostCardCost_mJU(mJUlist, query):
    for mJU in mJUlist.getMJUlist():
        
        """ update estCost """
        estCost = getEstJnCst_mJU(mJU)
        mJU.addEstCost(estCost)
        
        """ update estCard """
        midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
        res = cal_agg_exp_sel(get_conn_tbls(query, mJU)) * cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
        mJU.setEstCard(res)
# 
def mJUlist_sort_by_cost(mJUlist):
    #mJUlist.getMJUlist().sort(key = lambda mJU: mJU.getEstCard())
    mJUlist.getMJUlist().sort(key = lambda mJU: mJU.getEstCost())

def mJUlist_sort_by_card(mJUlist):
    #mJUlist.getMJUlist().sort(key=lambda mJU: mJU.getEstCost())
    mJUlist.getMJUlist().sort(key = lambda mJU: mJU.getEstCard())

def mJUlist_display(mJUlist):
    for mJU in mJUlist.getMJUlist():
        print mJU, mJU.getEstCost(), mJU.getEstCard()


query = qry.Query(conn, directed=True) 


tic= time.time()

""" ############################################### """
""" TEST000: create mJUlist & update est. card/cost """
""" ############################################### """
### create mJUlist
mJUlist = mju.MicroJUlist().getMicroJUlist(query)
### update mJUlist metrics
mJUlist.updateEstCostCardCost_mJU(query)
#mJUlist_sort_by_cost(mJUlist)
mJUlist.mJUlist_sort_by_card()
"""
for i in range(1000):
    mJUlist = getMicroJUlist(query)    
    mJUlist.updateEstCostCardCost_mJU(query)
    #mJUlist_sort_by_cost(mJUlist)
    mJUlist.mJUlist_sort_by_card()
toc= time.time()
print "query graph fetch", (toc-tic)
"""
#mJUlist.mJUlist_display()

cost0 = mJUlist.getMJUlist()[0].getEstCost()

""" ############################################### """
""" TEST00: aggregateFanouts + initiating TM_clustr """
""" ############################################### """


a = mJUlist.getMJUlist()[0].getMTM().getFanouts().getGraph()
b = mJUlist.getMJUlist()[0].getLTM().getFanouts().getGraph()
c = mJUlist.getMJUlist()[0].getRTM().getFanouts().getGraph()

from collections import defaultdict
from itertools import chain

### identify the cheapest mJU by cardinality
mJU = mJUlist.getMJUlist()[0]
mJU.getRbetter()


res = defaultdict(list, dict(chain(mJU.getMTM().getFanouts().getGraph().items(), 
                                   mJU.getLTM().getFanouts().getGraph().items(), 
                                   mJU.getRTM().getFanouts().getGraph().items() )))

tbl.TM_clstr(mJU).getFanouts().getGraph()
tbl.TM_clstr(mJU).getCard()


AB_BC_BE = tbl.TM_clstr(mJU)
AB_BC_BE.getCum_cost()

""" ############################################### """
""" TEST00: aggregateFanouts + initiating TM_clustr """
""" ############################################### """


""" ############################################### """
""" TEST01: update query graph                      """
""" ############################################### """
import copy 
query1 = copy.deepcopy(query)

### 
mJU.getMTM()
mJU.getLTM()
mJU.getRTM()
query1.substitute(mJU.getMTM(), AB_BC_BE)
query1.substitute(mJU.getLTM(), AB_BC_BE)
query1.substitute(mJU.getRTM(), AB_BC_BE)
query1.resetKeyVal()

query1.getQuery_vk()
query1.getQueryGraph()

len(query1.getAllValues())


""" ############################################### """
""" TEST10: aggregateFanouts + initiating TM_clustr """
""" ############################################### """
mJUlist4 = mju.MicroJUlist().getMicroJUlist(query1, excldShort = True)  
mJUlist4.getMJUlist()

### update mJUlist 
mJUlist4.updateEstCostCardCost_mJU(query1)
mJUlist4.mJUlist_sort_by_card()
#mJUlist4.mJUlist_display()

cost1 = mJUlist4.getMJUlist()[1].getEstCost()

mJU_CE_BE_BC_AB_CD = mJUlist4.getMJUlist()[1]
CE_BE_BC_AB_CD = tbl.TM_clstr(mJU_CE_BE_BC_AB_CD)

tic= time.time()
"""
for i in range(1000):
    query2 = copy.deepcopy(query1)
toc= time.time()
print "query graph fetch", (toc-tic)
"""
query2 = copy.deepcopy(query1)
mJU_CE_BE_BC_AB_CD.getMTM()
mJU_CE_BE_BC_AB_CD.getLTM()
mJU_CE_BE_BC_AB_CD.getRTM()
query2.substitute(mJU_CE_BE_BC_AB_CD.getMTM(), CE_BE_BC_AB_CD)
query2.substitute(mJU_CE_BE_BC_AB_CD.getLTM(), CE_BE_BC_AB_CD)
query2.substitute(mJU_CE_BE_BC_AB_CD.getRTM(), CE_BE_BC_AB_CD)
query2.resetKeyVal()
query2

query3 = copy.deepcopy(query2)
query3.getKeys()[0].getCard()

query3 = copy.deepcopy(query2)
mJUlist5 = mju.MicroJUlist().getMicroJUlist(query3, excldShort = True)  
mJUlist5.getMJUlist()

mJUlist6 = mju.MicroJUlist().getMicroJUlist(query3, excldShort = False)  
mJUlist6.getMJUlist()

excldShort = False

"""
mJUlist = mju.MicroJUlist([])
query = query1
queryGraph_vk = query.getQuery_vk().getQueryGraph()
for TM1 in queryGraph_vk.keys(): # first node
    print '{}: {}'.format(TM1, 'start')   
    otherTMs = set([])
    for table1 in queryGraph_vk[TM1]: # tbl-link
        print '1 tl', table1, query._graph[table1]
        for TM2 in query.getQueryGraph()[table1]:
            print TM2
            otherTMs.add(TM2) # linked TM set
            print 'otherTMs:', otherTMs
            otherTMs.discard(TM1)
            for TM3, TM4 in itertools.combinations(otherTMs, 2):
                microJU = mju.MicroJU(TM1, query)
                microJU.addOtherTMs(TM3)
                microJU.addOtherTMs(TM4)
                print 'microJU:', microJU
                mJUlist.append(microJU)

mJUlist.mJUlist_display()

cost0 + cost1
"""



"""
for TM3, TM4 in itertools.combinations(otherTMs, 2):
    print TM3, TM4


query1.getQueryGraph()[A]
query1.getQueryGraph()[C]
query1.getQueryGraph()[E]
query1.getQueryGraph()[B]

import itertools
mJUlist4 = mju.MicroJUlist([])
queryGraph_vk = query1.getQuery_vk().getQueryGraph()


for TM1 in queryGraph_vk.keys(): # first node      
    print '{}: {}'.format(TM1, 'start')   
    otherTMs = set([])
    for table1 in queryGraph_vk[TM1]: # tbl-link
        print '1 tl', table1, query._graph[table1]
        for TM2 in query1.getQueryGraph()[table1]:
            print TM2
            otherTMs.add(TM2) # linked TM set
            print 'otherTMs:', otherTMs
        otherTMs.discard(TM1)
        for TM3, TM4 in itertools.combinations(otherTMs, 2):
            microJU = mju.MicroJU(TM1, query1)
            microJU.addOtherTMs(TM3)
            microJU.addOtherTMs(TM4)
            print 'microJU:', microJU
            mJUlist4.append(microJU)
mJUlist4


TMs = queryGraph_vk.keys()
queryGraph_vk[TMs[0]]

queryGraph_vk[queryGraph_vk.keys()[0]]

for TM2 in query1.getQueryGraph()[E]:
    otherTMs.add(TM2) # linked TM set

for TM3, TM4 in itertools.combinations(otherTMs, 2):
    print TM3, TM4

    
otherTMs
"""

list(mJUlist.getMJUlist()[0].getTables(query))[0].getCum_cost()



""" creating TM_cluster """


query.getQueryGraph()

"""
========================================

updateEstCostCardCost_mJU(mJUlist,query)
mJUlist_sort_by_cost(mJUlist)
mJUlist_sort_by_card(mJUlist)

"""


"""
Recursively
"""
"""
TO-DO: do what 
"""


"""
mJU
midTM, LTM, RTM = mJU.getMidTM(), mJU.getLTM(), mJU.getRTM()
res = cal_agg_exp_sel(get_conn_tbls(query, mJU)) * cal_agg_prod_card(midTM, LTM, RTM) * midTM.getLowestFO(LTM).getFO() *midTM.getLowestFO(RTM).getFO()
mJU.setEstCard(res)

mJUlist.getMJUlist()[1].getEstCard()
"""

    



#getEstJnCst_mJU(mJU)
#mJU.addEstCost(mJU.getEstJnCst_mJU())
#mJU.getEstCost()
#mJU.estCost = 0.0
#mJU.getEstCard()




""" cost of the two """
"""
if (toMTM(MTM_card, LTM_card, p2_5, p3_7) == True):
    print 'MTMfirst'
    ans = utility.cost_join_nl_by_card(MTM_card*getProdNormSel_set(p2_5) * getProdNormSel_set(p1_4),  LTM_card * getProdNormSel_set(p3_7))
else:
    print 'otherTMfirst'
    ans = utility.cost_join_nl_by_card(MTM_card*getProdNormSel_set(p2_5),  LTM_card*getProdNormSel_set(p3_7) * getProdNormSel_set(p1_4))
ans

if (toMTM(MTM_card, RTM_card, p1_5, p3_6) == True):
    print 'MTMfirst'
    ans1 = utility.cost_join_nl_by_card(MTM_card*getProdNormSel_set(p1_5) * getProdNormSel_set(p2_4),  RTM_card * getProdNormSel_set(p3_6))
else:
    print 'otherTMfirst'
    ans1 = utility.cost_join_nl_by_card(MTM_card*getProdNormSel_set(p1_5),  RTM_card*getProdNormSel_set(p3_6) * getProdNormSel_set(p2_4))
ans1
ans - ans1
"""


"""
mJUlist.getMJUlist()[0].initiate_tbls_TMs_est_mtrcs()
mJUlist.getMJUlist()[0].getExpMtrcsDict().getExpMtrc_tbl(A)

mJUlist.getMJUlist()[1].initiate_tbls_TMs_est_mtrcs()
mJUlist.getMJUlist()[1].getExpMtrcsDict().getExpMtrc_tbl(A)

mJUlist.getMJUlist()[2].getExpMtrcsDict().getExpMtrc_tbl(A)

mJUlist.getMJUlist()[6].getExpMtrcsDict().getExpMtrc_tbl(B)
len(mJUlist.getMJUlist())
"""

#mJU.initiate_tbls_TMs_est_mtrcs()
""" 

"""
"""
mJU.getExpMtrcsDict().getExpMtrc_tbl(A)

mJU.getExpMtrcsDict()

mJU = mJUlist.getMJUlist()[4]
"""

"""
mJU.getExpMtrc_tbl(A).get_norm_preds_todo()
mJU.getExpMtrcsDict().getExpMtrc_tbl(A)
mJU.getExpMtrc_tbl(A).get_norm_preds_todo()
"""
"""
mJU.getMidTM()
mJU.getOtherTMs()

LTM_tbls = mJU.getLTM_tbls()
MTM_tbls = mJU.getMTM_tbls()
RTM_tbls = mJU.getRTM_tbls()

p1_4 = MTM_tbls.intersection(LTM_tbls) 
p2_4 = RTM_tbls.intersection(MTM_tbls) 
p3_4 = LTM_tbls.intersection(RTM_tbls)
p1 = p1_4.difference(RTM_tbls)
p2 = p2_4.difference(LTM_tbls)
p3 = p3_4.difference(MTM_tbls)
p4 = MTM_tbls.intersection(LTM_tbls).intersection(RTM_tbls)
p4 = p1_4.intersection(p2_4)
p5 = MTM_tbls.difference(p1_4).difference(p2)
p6 = RTM_tbls.difference(p2_4).difference(p3)
p7 = LTM_tbls.difference(p3_4).difference(p1)

"""
""" LTM = MTM """
"""
p1_4 = MTM_tbls.intersection(LTM_tbls) # mid & LTM: B
p3_7 = LTM_tbls.difference(p1_4)
p2_5 = MTM_tbls.difference(p1_4)
"""
""" 1) look for the estimated metric dictionary """ 
"""
[table.getProdNormSel() for table in p1_4]
[table.getProdNormSel() for table in p3_7]
[table.getProdNormSel() for table in p2_5]
"""


""" MTM = RTM """
"""
p2_4 = MTM_tbls.intersection(RTM_tbls) # mid & LTM: B
p3_6 = RTM_tbls.difference(p2_4)
p1_5 = MTM_tbls.difference(p2_4)

[table.getProdNormSel() for table in p2_4]
[table.getProdNormSel() for table in p3_6]
[table.getProdNormSel() for table in p1_5]
"""


"""
for table in p1_4:
    print table, table.getProdNormSel()
mJU.initiate_tbls_TMs_est_mtrcs()
"""


"""
for pred in A.getNormPreds():
    table_est_mtrc.get_norm_preds_todo().remove(pred)
intersection_preds_todo = [pred for pred in p_todo if pred not in preds]
len(intersection_preds_todo)

p_todo = [pred for pred in p_todo if pred not in preds]

"""


""" MTM = RTM """
"""
p2_4 = RTM_tbls.intersection(MTM_tbls) # RTM & mid: B
P1_5 = MTM_tbls.difference(p2_4)
p3_6 = RTM_tbls.difference(p2_4)
"""

"""
res = []
for table in p1_4:
    res.append([pred.sel for pred in [pred for pred in table.getNormPreds() if pred.norm_sel_bool == True]])
res    
"""

# nanoJU
#MTM.getCard()
#LTM.getCard()


# MTM.getCard() * 




    
"""
하려고 하는 바: normselList ==> loop  해서 
tmp card =>  predicate cost

p2 = midTM_tbls.intersection(LTM_tbls) # B
p3 = midTM_tbls.difference(LTM_tbls).difference(RTM_tbls) # C
p4 = RTM_tbls.intersection(midTM_tbls) # B
p5 = RTM_tbls.difference(midTM_tbls) # A
"""    





""" predicate selectivity """
"""
ps1 = cal_agg_exp_sel(p1)
ps2 = cal_agg_exp_sel(p2)
ps3 = cal_agg_exp_sel(p3)
ps4 = cal_agg_exp_sel(p4)
ps5 = cal_agg_exp_sel(p5)
ps2_4 = cal_agg_exp_sel(p2_4)
ps4_2 = cal_agg_exp_sel(p4_2)
ps1_5 = cal_agg_exp_sel(p1_5)
ps5_1 = cal_agg_exp_sel(p5_1)
"""

utls = utl.Utilities()
"""
utls.cost_join_nl(midTM, LTM)
utls.cost_join_nl(midTM, RTM)
utls.cost_join_nl(midTM, LTM)
"""


#utls.cost_join_nl()


query

midTM = mJUlist.getMJUlist()[0].getMidTM()
LTM = mJUlist.getMJUlist()[0].getLTM()
RTM = mJUlist.getMJUlist()[0].getRTM()




join_fo = midTM.getLowestFO(LTM)
# join cardinality
midTM.getCard() * LTM.getCard() * midTM.getLowestFO(LTM).getFO()
# join cost_nl
midTM.getCard() * LTM.getCard()

""" TM cluster """
# card
# fanouts


s = midTM.getFanouts()
other1 = LTM.getFanouts()

type(other1)

#s = dict(s.getGraph().items() + other1.getGraph().items()+ other1.getGraph().items())
#s

# combined fanouts dict
#union = dict(s.getGraph().items() + other1.getGraph().items()+ other1.getGraph().items())

# create a dictionary of fanouts with tables as keys
res = {key:s._graph[key] for key in s._graph if key in other1._graph}
a = [fanout for fo_list in [res[key] for key in res.keys()] for fanout in fo_list]

a.sort(key = lambda fanout: fanout.getFO())


# sort by fanout
midTM.getLowestFO(LTM)

midTM_tbls = query.getQuery_vk().getValues(midTM)
LTM_tbls = query.getQuery_vk().getValues(LTM)
RTM_tbls = query.getQuery_vk().getValues(RTM)
temp=set([])
temp= temp.union(midTM_tbls)
temp= temp.union(LTM_tbls)
temp= temp.union(RTM_tbls)
temp
"""
fo_e_bc = fo.Fanout(E, BC)
midTM.fanouts.add(fo_e_bc)
midTM.fanouts
"""
list(temp)
# expected combined selectivity of all norm predicates in mJUlist
from numpy import prod
prod([tbl1.get_exp_norm_sel() for tbl1 in temp])

# get the fanout dictionary list
FOs1_graph = LTM.getFanouts().getGraph()
FOs1_graph.items()

FOs2_graph = RTM.getFanouts().getGraph()
FOs2_graph.items()

# get an intersection
res = {key:FOs1_graph[key] for key in FOs1_graph if key in FOs2_graph}





def join_cost_nl (TM1, TM2):
    return TM1.getCard() * TM2.getCard()




"""
[AB, BC, CE] == [AB, BC, CE]
query_vk = query.swapKeyVal() 
query_vk._graph[BC]
"""
""" loop through the table"""
"""
query_vk._graph.keys()[0] # TM key : loop
query_vk._graph[query_vk._graph.keys()[0]] # normal tables connected to 
for TM1 in query_vk._graph.keys(): # first node
    #print '{}: {}'.format(TM1, 'start')
    for table1 in query_vk._graph[TM1]: # tbl-link
"""

"""
queryGraph_vk = query.getQuery_vk().getQueryGraph()
for TM1 in queryGraph_vk.keys():
    None
    #print TM1
"""


mJUlist = getMicroJUlist(query)


microJUlist = mJUlist.getMJUlist()

midTM = microJUlist[0].getMidTM()
LTM = microJUlist[0].getLTM()
RTM = microJUlist[0].getRTM()

#def estCard_mJU(mJU):

mJU = microJUlist[0]



midTM = mJU.getMidTM()
LTM = mJU.getLTM()
RTM = mJU.getRTM()

# (0) get connected tables
tbls_LTM = query.getQuery_vk().getQueryGraph()[LTM]
tbls_MTM = query.getQuery_vk().getQueryGraph()[midTM]
tbls_RTM = query.getQuery_vk().getQueryGraph()[RTM]


""" first round: MTM/LTM """
#def get
# (1) get tables 
intersection = tbls_MTM.intersection(tbls_LTM)
mtm = tbls_MTM.difference(intersection)
other = tbls_LTM.difference(intersection)

# estimate cardinality of midTM with exclusively connected tables
midTM_card_upd = midTM.getCard()
for table in mtm:
    midTM_card_upd *= table.get_exp_norm_sel()
midTM_card_upd

# estimate cardinality of other with exclusively connected tables
otherTM_card_upd = LTM.getCard()
for table in other:
    otherTM_card_upd *= table.get_exp_norm_sel()
otherTM_card_upd

# assing intersection to the table with lower est. cardinality than the other
for table in intersection:
    if midTM_card_upd <= otherTM_card_upd:
        midTM_card_upd *= table.get_exp_norm_sel()
    else:
        otherTM_card_upd *= table.get_exp_norm_sel()

midTM_card_upd
otherTM_card_upd

midTM.getFanouts().getFOs(B)

midTM.card
LTM.card
""" intermediate estimated cardinality before join """ 
midTM_card_upd
otherTM_card_upd



intersection
""" join prep """
# get fanouts in the intersection
k = [fanout for tbl1 in midTM.getFanouts().getGraph() for fanout in midTM.getFanouts().getFOs(tbl1) if tbl1 in intersection]
# sort the fanouts
k.sort(key = lambda fanout: fanout.getFO())
k[0]

midTM_card_upd * otherTM_card_upd * k[0].getFO()
""" this is optimized way of implementing """
""" faster way do anyhow """


  
    

a = [x for x in midTM.getFanouts().getAllFOs() if x.getTbl() in intersection]
a.sort(key = lambda fanout: fanout.getFO())
a
    

midTM.getFanouts()

midTM.getFanouts().getFOs_list(intersection)
LTM.getFanouts().getFOs_list(intersection)

list(query._graph.items()[0][1])[0].fanouts

fanouts = fo.Fanouts()
import copy
conn1 = copy.deepcopy(conn)
fanouts.add_connections(conn1)
type(list(fanouts.getAllFOs())[0])

query.getFstKey().getTMbool()
query


LTM


midTM = microJUlist[0].getMidTM()
LTM = microJUlist[0].getLTM()
RTM = microJUlist[0].getRTM()



list(tbls_LTM)[0]
list(tbls_LTM)[0].get_exp_norm_sel()
list(tbls_LTM)[1]
list(tbls_LTM)[1].get_exp_norm_sel()

list(tbls_MTM)[0]
list(tbls_MTM)[0].get_exp_norm_sel()
list(tbls_MTM)[1]
list(tbls_MTM)[1].get_exp_norm_sel()

list(tbls_LTM)[0].norm_preds.exp_norm_sel

list(tbls_LTM)[1].norm_preds.exp_norm_sel

tbls_LTM


LTbls = query.getQuery_vk().getQueryGraph()[LTM]
RTbls = query.getQuery_vk().getQueryGraph()[RTM]
intersection = LTbls.intersection(RTbls)
left = LTbls.difference(intersection)
right = RTbls.difference(intersection)

query.getQuery_vk().getQueryGraph()[midTM]
query.getQuery_vk().getQueryGraph()[LTM]
query.getQuery_vk().getQueryGraph()[RTM]

mJU = microJUlist[0]

def div_int_lf_rg(mJU):
    """ input: two TMs and related tables """
    #midTM = microJUlist[0].getMidTM()
    LTM = microJUlist[0].getLTM()
    RTM = microJUlist[0].getRTM()
    
    LTbls = query.getQuery_vk().getQueryGraph()[LTM]
    RTbls = query.getQuery_vk().getQueryGraph()[RTM]
    intersection = LTbls.intersection(RTbls)
    left = LTbls.difference(intersection)
    right = RTbls.difference(intersection)
    """ left: normal tables exclusive to left TM """
    """ output left == right: sets of normal tables, leftTM, rightTM """
    return left, intersection, right, 
    """ each set of normal tables may not be more than one as TM_cluster """  


list(microJUlist[0].getOtherTMs())





"""
def updateExpCard(self):
    for mJU in self.mJUlist:
"""
def cost_join_nl(key_node, node):
    return key_node.card*node.card
    
def processPredicate(tbls, TM, cost_join):
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

def nano_opt(micro_JU, cost_join = cost_join_nl):
    """ I would like to build nano_opt not transfering actual object """

    """ input: micro_JU + self.cost_join_[method]"""
        
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
    
    #query_dc = copy.deepcopy()
    """
    query_dc_vk = query_dc.swapKeyVal() # same table object
    lfOnly, intersection, rghOnly, leftTM, rightTM = self.div_int_lf_rg(query_dc_vk)
    """
    """ output: lfOnly, intersection, rghOnly:set of tbls; leftTM, rightTM: TM """
    """ TO-DO: write processPredicate(tbl, TM) """
    """
    self.processPredicate(lfOnly, leftTM, cost_join)
    self.processPredicate(rghOnly, rightTM, cost_join)
    if leftTM.getCard() > rightTM.getCard(): # apply predicates intersection where card is lower
        self.processPredicate(intersection, rightTM, cost_join)
    else:
        self.processPredicate(intersection, leftTM, cost_join)
    return self.processJoin_nl(leftTM, rightTM) # nested loop join
    """
#dd = None
#dd = getMicroJU(query)
#query._graph    



        #for table : None
""" make function get TM by key, get key by TM"""
###############################
# test: fanouts are created with a deepcopy
#### ===>> SUCCESS
###############################

def test_deepcopy_FO():
    query = qry.Query(conn, directed=True) 
    BC.table_name = 'BC1'
    query.displayFOs()


###############################
# test: to create fanouts and allocate to each TM
#### ===>> SUCCESS
###############################

def displayFOs(query):
    for TM in query.getAllValues():
        print TM.fanouts
"""
displayFOs(query)
list(query.getAllValues())[1].fanouts

fanouts1._graph[D][0].getFO()

fanouts1._graph[B][0].getFO()
fanouts1._graph[B][0].getTM()
fanouts1._graph[B][0].getTbl()

"""
"""
fanouts1._graph[B][0].fo_ratio
fanouts1._graph[B][1].fo_ratio
"""

###############################
# test: merge
#### ===>> SUCCESS
###############################

###############################
# test: crete a fanout dictionary
# (TM, tbl): fanout
# has to check if fanout does not change after being created
# can we refer the fanout with different object address
# how can we update TM_cluster
#### ===>> SUCCESS
###############################    

def test10():    

    conn, query =  pred_query5()

    conn
    from collections import defaultdict
    conn[0][0].card = 11000

    fanout_dict = defaultdict(float)
    import copy
    TMtbls = copy.deepcopy(conn)

    TMtbls[0][0].card/(TMtbls[0][1].card)**.5
    
    TM, tbl1 = TMtbls[0]
    TM.card = 11000
    TM

    fanout_dict[(TM, tbl1)] = (TM.card/(tbl1.card)**.5)

    for TM, tbl1 in TMtbls:
        fanout_dict[(TM, tbl1)] = (TM,TM.card/(tbl1.card)**.5)

#test10()
###############################
# test: can we sort by normselectivity?
#### ===>> SUCCESS
###############################    
def test11():
    query = pred_query4()
    query_vk = query.swapKeyVal()
    tbls = query_vk.getAllValues()
    tbls_list = list(tbls)
    tbls_list
    tbls_list.sort(key = lambda tbl: tbl.getNormPreds().getProdNormSel())
    print tbls_list
    
#test11()
    
"""
any(tbl for tbl in tbls_list if tbl.has_normPred())
[tbl for tbl in tbls_list if tbl.has_normPred()]
any(tbl for tbl in tbls_list if tbl.has_UDFPred())
"""



    
""" TEST CASE """
    
#query = pred_query2()

""" shallow copy """

#query_dc = query



"""
# change card of table A: 5k to 6k
query_dc._graph.items()[0][0].card = 6000
#print query_dc._graph.items()[0][0].card
#print query._graph.items()[0][0].card
"""
""" works!! """


#(query._graph.items()[0][1] & query_dc._graph.items()[0][1]).pop().card


#query = pred_query2()
""" deep copy """
#import copy
#query_dc = copy.deepcopy(query)
# change card of table A: 5k to 6k
#query_dc._graph.items()[0][0].card = 6000
#print query_dc._graph.items()[0][0].card
#print query._graph.items()[0][0].card

""" change the card of AB for testing 10k to 11111"""
""" 
elem = query_dc._graph.items()[0][1].pop()
elem.card = 11111
elem.card
query_dc._graph.items()[0][1].add(elem)
query_dc._graph.items()[0][1]
query_dc._graph

query_dc_vk = query_dc.swapKeyVal()
query_vk = query.swapKeyVal()

query_dc_vk == query_vk

query_dc_vk.snapshot_AllNodes()

intersection = query_dc_vk._graph.items()[0][1] & query_dc_vk._graph.items()[1][1]
intersection
elem2 = intersection.pop()
elem2

leftOnly = query_dc_vk._graph.items()[0][1] - intersection
leftOnly
for ele in leftOnly:
    print ele, ele.card, ele.norm_preds.length() #.getSel()
    

    
elem3 = leftOnly.pop()
elem3.getNormPredSel()
elem3.card = 6600
query_dc_vk.snapshot_AllNodes()

leftOnly.add(elem3)
elem4 = leftOnly.pop()
elem4.card = 6700

#### soft copy 
leftOnly.add(elem4)


query_dc_vk.snapshot_AllNodes()


rightOnly = query_dc_vk._graph.items()[1][1] - intersection

elem1 = rightOnly.pop()
elem1
elem1
"""


#& query_vk._graph.items()[0][1]


""" update the old graph with the updated one """
""" SUCCESS """
""" SUCCESS """
#query = query_dc

""" swap key value """

#query_dc_vk = query_dc.swapKeyVal()
#query_dc_vk._graph.keys()

#query.snapshot_AllNodes()


""" update: old and new """
""" has to have same """

# check if the two query are identical in terms of length and 

#query_dc == query

#query_dc

"""
query_an_set = query.get_AllNodes_set()
query_dc_an_set = query_dc.get_AllNodes_set()

query_an_set
query_dc_an_set

query_an_list = query.get_AllNodes()
query_dc_an_list = query_dc.get_AllNodes()

query_an_list
query_dc_an_list

for old, new in zip(query_an_list, query_dc_an_list):
    old = new

query_an_list[0].card

A_old = copy.copy(query._graph.items()[0][0])
A_old.card = 600
vars(A_old)
A_new = copy.copy(query_dc._graph.items()[0][0])
A_old = copy.deepcopy(A_new)
A_old.card
query.snapshot_AllNodes()



    
query_an_list[0].card
query_dc_an_list[0].card

query_an_list[0] = copy.deepcopy(query_dc_an_list[0])

query_an_list[0].card
query_dc_an_list[0].card


query._graph.keys()[0].card=5000

query.snapshot_AllNodes()
"""

""" doesn't get the original one updated """

    
#query_lfTM_vk.
"""
query.getQueryGraph()

conn = [(val,key) for key in query._graph for val in query._graph[key]]
conn

a = qry.Query(conn, directed=True)



a.getQueryGraph()
    
lfOnly, intersection, rghOnly, leftTM, rightTM = div_int_lf_rg(a)

lfOnly_list = list(lfOnly)
intersection_list = list(intersection)
import copy
#lfOnly_list.sort((key=lambda node: node.table_name))

import copy
query = pred_query3()
query._graph
query_dc = copy.deepcopy(query)
query_dc_vk = query_dc.swapKeyVal()
lfOnly, intersection, rghOnly, leftTM, rightTM = div_int_lf_rg(query_dc_vk)
"""    