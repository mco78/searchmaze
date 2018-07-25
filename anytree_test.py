# -*- coding: utf-8 -*-
"""
Testing Tree Structure


Created on Wed Jul 25 17:01:13 2018

@author: Marc Otten
"""

class Tree(object):
    def __init__(self, name, parent):
        self. name
        self.parent = parent
        self.children = []
        self.goal = False
    
    def create_child(self):
        self.children.append(Tree(self))
        

"""
a   -> b    -> c
            -> d    
    -> e    -> f
    -> g    -> h
            -> i
"""           

tree_structure = []
tree_structure.append(Tree("a"))
