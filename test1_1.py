# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 13:15:41 2017

@author: HKIM85
"""
class MyObject1:
    def __init__(self,value,meta):
        self.value = value
        self.meta = meta
    def __eq__(self,other):
        return self.value == other.value
    def __hash__(self):
        return hash(self.value)
        
##fix the eq and hash to work correctly
class MyObject:
    def __init__(self,value,meta):
        self.value = value
        self.meta = meta
    def __eq__(self,other):
        return self.value, self.meta == other.value, other.meta
    def __hash__(self):
        return hash((self.value)) #hash((self.value, self.meta))
    def __repr__(self):
        return "%s %s" % (self.value,self.meta)

a = MyObject('1','left')
b = MyObject('1','right')
c = MyObject('2','left')
d = MyObject('2','right')
e = MyObject('3','left')

print a == b # True
print a == c # False

k = list(set([a,c,e]))
k
res = sorted(list(set([a,c,e])), key=lambda obj:(obj))
res
union =  set([a,c,e]) | (set([b,d]))
print union

intersection = set([a,c,e]) & (set([b,d]))
print intersection

##sort the objects, so that older objs come before the newer equivalents
sl = sorted(union, key= lambda x: (x.value, x.meta) )
print sl

set([a,c,e]) & (set([b,d]))

for i in set([a,c,e]).intersection(set([b,d])):
    print "%s %s" % (i.value,i.meta)
#returns:
#1 right
#2 right

for i in set([a,c,e]).union(set([b,d])):
    print "%s %s" % (i.value,i.meta)
#returns:
#1 left
#3 left
#2 left    
