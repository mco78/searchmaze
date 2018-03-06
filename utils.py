# -*- coding: utf-8 -*-
"""
Utility Functions for searchmaze.py
Created on Fri Mar  2 13:17:10 2018

@author: Marc Otten
"""
#LIBS
import numpy as np

#CUSTOM
import gui
from fixtures import GUI_STYLE

def array_addition(arr1, arr2):
    """element wise addition of two arrays ONLY with length 2"""
    a = np.array(arr1)
    b = np.array(arr2)
    result = a + b
    return [result[0], result[1]]
