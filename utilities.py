# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:48:10 2016

@author: HKIM85
"""


class Utilities(object):
    def cardCnt(self, path):
        None
            
    def cost_join_nl(self, TM1, TM2):
        return TM1.getCard()*TM2.getCard()

    def cost_join_nl_by_card(self, TM1_card, TM2_card):
        if (TM1_card <= TM2_card):
            return TM1_card + TM1_card * TM2_card
        else:
            return TM2_card + TM1_card * TM2_card
    
    def joinCost(self, table1, table2):
        table1.getCard
        None
        
    def cost_norm_preds(self, table):
        return table.card