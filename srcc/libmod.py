# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 13:15:18 2022

@author: Du Ho
"""

import numpy as np
import os, sys
import unittest

def check(a):
    if not isinstance(a,np.ndarray):
        a = np.array(a)
    return a

def isscalar(a):
    a = check(a)
    if np.isscalar(a):
        return True
    else:
        return False