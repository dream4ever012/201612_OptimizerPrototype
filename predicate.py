# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 15:35:45 2016

@author: HKIM85
"""
"""
to filter a list of object
[x for x in myList if x.n == 30]
"""

"""
TO-DO
1) at some point of time, Predicates class is to be seperated from Predicate
2) needs more design optimization in OO programming spirit.
    such as, 
3) test function needs to be in independent .py 
"""
class Predicate(object):
    
    def __init__(self, pred_name = 'DFT', sel = 1.0, norm_sel_bool = True): #, UDF_sel_bool = False):
        self.pred_name = pred_name # pred name follows after col_nanme + idx 
                                   # in case that multiple preds in a col exist
        self.norm_sel_bool = norm_sel_bool ### True: valid pred; False: dismiss
        #self.UDF_sel_bool = UDF_sel_bool
        self.sel = sel # always set to 1.0 and bool = False initially
        self.est_cost_pr = 0 # estimated cost per row: # ns or ms
        self.isDone = False
        
        """ norm_sel_bool and UDF_sel_bool defines if a table has any predicates """
        self.estNormSel()
        if (norm_sel_bool == False): self.getUDFSel()

    def __repr__(self):
        return self.pred_name

    def __str__(self):
        name = '{name: ' + self.pred_name + '}'
        sels = '{selectivity: ' + str(self.sel) + '}'
        est_cost_pr = '{est_cost_pr: ' + str(self.est_cost_pr) + '}'
        return (name + ' ' + sels + ' ' + est_cost_pr)
    
    # once set norm_sel_bool to be True
    def setSel(self, sel = 1.0):
        self.sel = sel

    def getSel(self):   
        return self.sel
    
    def getDone(self):
        return self.isDone
        
    def setDone(self):
        """ cannot reset the pred """
        self.isDone = True

    def estNormSel(self):
        if (self.norm_sel_bool == False):
            self.setNormSel(norm_sel = 1.0)
        # else: 
        # self.norm_sel = normSel estimation
        # self.est_cost_pr = scan cost per row
    
    def estNormCost(self): # norm cost per row == scan cost
        """ TO-DO: undistributed setting scan cost """
        """ But scan cost varies in distributed setting or in case of policy"""
        self.est_cost_pr = 1.0
        
    def getNormSelBool(self):
        return self.norm_sel_bool
        """
    def setUDFSel(self, UDF_sel = 1.0):
        if (self.norm_sel_bool == False):
            #self.UDF_sel_bool = True
            self.sel = UDF_sel
        else: print 'norm_predicate already set: cannot set UDF sel'

    def getUDFSel(self):
        return self.UDF_sel
        """
    def estUDFSel(self):
        if(self.UDF_sel_bool == False):
            self.setUDFSel(UDF_sel = 1.0)
        #else: 
            
    def estUDFCost(self, UDFcostF):
        """ may need another data structure to contain past performance"""
        """ TO-DO: have to define input and output of UDFcostF """
        None
    
    def getUDFSelBool(self):
        return self.UDF_sel_bool

###############################
# test1) create predicate and print
#### ===>> SUCCESS
# 
###############################         
def test0():
    print ' '
    print 'test0: create predicate and print'
    pred0 = Predicate(pred_name = 'pred0', norm_sel_bool = False)
    print pred0
    print '====== SUCCESS ======'

#test0()
       
class Predicates(object):
    """ TO-DO: support OR + NOT relation between predicates """
    #from sets import Set
    def __init__(self, preds = [], tot_cost = 0):
        self.preds = []
        for pred in preds:
            if (pred not in self.preds):
                self.preds.append(pred)
        self.preds.sort(key= lambda pred: pred.sel)
        self.exp_norm_sel = 0.0
        self.exp_norm_cost = 0.0
        self.update_exp_norm_sel()

    def add(self, pred):
        if (pred not in self.preds):
            self.preds.append(pred)
            self.preds.sort(key = lambda pred: pred.sel)
        
    def remove(self, pred):
        try:
            self.preds.remove(pred)
        except ValueError:
            pass
    
    def getPreds(self):
        return self.preds
        
    def getPredSel(self):
        if self.length() == 1:
            return self.preds[0].getSel()
        else:
            return None
            """ returning None means that predicates hasn't been aggregated to one selectivity """
            
    def update_exp_norm_sel(self):
        self.exp_norm_sel = self.getProdNormSel()
        
    def get_exp_norm_sel(self):
        return self.exp_norm_sel
    
    def getProdNormSel(self):
        """ Get the product of selectivity of each predicate """
        #sel_list = 
        from numpy import prod
        return prod([pred.sel for pred in [pred for pred in self.preds if pred.norm_sel_bool == True]])
    
    def getNormSelList(self):
        """ Get a list of selectivity of each predicate """
        tmp = [pred.sel for pred in [pred for pred in self.preds if pred.norm_sel_bool == True]]
        tmp.sort()
        return tmp
    
    def sort_by_sel(self):
        if (self.has_normPred()):
            self.preds.sort(key = lambda pred: pred.sel)
    
    def __repr__(self):
        return '{}'.format(self.preds)
    
    def length(self):
        return len(self.preds)
        
    def has_normPred(self):
        res = False
        if(self.length()>0):
            for pred in self.preds:
                if (pred.getNormSelBool()==True):
                    res = True
        return res
    
    def has_mult_normPred(self):
        res = False
        if(self.length()>1):
            for pred in self.preds:
                if (pred.getNormSelBool()==True):
                    res = True
        return res
                  
    def has_UDFPred(self):
        res = False
        if(self.length()>0):
            for pred in self.preds:
                if (pred.getUDFSelBool()==True):
                    res = True
        return res
        
    def display_all(self):
        for pred in self.preds:
            print pred


def test_prep():
    pred0 = Predicate(pred_name = 'pred0', norm_sel_bool = True)          
    pred1 = Predicate(pred_name = 'pred1', norm_sel_bool = True)
    pred2 = Predicate(pred_name = 'pred2', norm_sel_bool = True)
    # 
    preds0 = Predicates()
    preds0.add(pred0)
    preds0.add(pred1)
    preds0.add(pred2)
    return preds0

#preds1
###############################
# test1) display_all
#### ===>> SUCCESS
# 
###############################

def test1():
    print ' '
    print 'test1: display_all'
    print 'display pred0, pred1, pred2'
    preds0 = test_prep()
    preds0.display_all()
    print '====== SUCCESS ======'
    
#test1()

###############################
# test2) remove predicates
#### ===>> SUCCESS
# 
###############################

def remove(preds, pred):
    preds.remove(pred)
    

def test2():
    print ' '
    print 'test2: remove one predicate'
    print 'display pred0, pred1, pred2'
    
    preds1 = test_prep()
    pred1 = Predicate(pred_name = 'pred1', norm_sel_bool = True)
    preds1.display_all()
    remove(preds1, pred1)
    print ' '
    print 'remove(pred1)'
    preds1.display_all()
    print '====== SUCCESS ======'
    
#test2()

###############################
# test3) sort predicates by an attribute
#### ===>> SUCCESS
# 
###############################

preds0 = test_prep()
pred0 = Predicate(pred_name = 'pred0', norm_sel_bool = True)    

preds0.preds[0].setSel(sel = .8)
preds0.preds[1].setSel(sel = .6)
preds0.preds[2].setSel(sel = .2)


preds0 = test_prep()
pred0 = Predicate(pred_name = 'pred0', norm_sel_bool = True)    
# pred0.getSel()
# preds0.preds[0].getSel()

###############################
# test4) test the method getProdNormSel()
#### ===>> SUCCESS
# 
###############################

preds0.preds[0].setSel(sel = .8)
preds0.preds[1].setSel(sel = .6)
preds0.preds[2].setSel(sel = .2)

res = preds0.getProdNormSel()
"""
preds0
preds0.preds.sort(key = lambda pred: pred.sel)
preds0
"""

"""
print preds0.preds[0]
print preds0.preds[1]
print preds0.preds[2]


res = [pred for pred in preds0.preds if pred.norm_sel_bool == False]
print res

preds1 = sorted(preds0.preds, key = lambda pred: pred.pred_name)

print preds1[0]
preds1[0].setNormSel(norm_sel=0.7)

preds1
print preds1[0]
preds1[0].setNormSel(norm_sel = .11)
print preds1[0]
"""
