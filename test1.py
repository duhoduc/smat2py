# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 16:51:26 2022

@author: Du Ho
"""

import os, sys
import json
import csv
import re
space = ' '

path_to_main = os.path.dirname(os.path.abspath(__file__))
path_to_examples = path_to_main+os.sep+'examples'+os.sep
# Check files in folder
for thing in os.listdir(path_to_examples):
    thing = os.path.join(path_to_examples,thing)
    if thing.endswith('.m'):
        with open(thing,'r') as file:
            newlines = file.readlines()
    print(newlines)

def splitVars(varNames,delimiter = ','):
    # for return and varNames
    bad_chars = '[]() '
    varNames = varNames.replace(bad_chars,'')
    for bad_char in bad_chars:
        varNames = varNames.replace(bad_char,'')
    varNames_ = varNames.split(delimiter)
    return varNames_

def handleFunction(line):
    lls = line.strip('function').strip('\n').split('=') # should be 
    if len(lls) == 1:
        # no return
        returnVars = ''
        isReturn = False
        funNamesVars = lls.replace('=','').split('(')
        if len(funNamesVars) == 1: # not varargin
            funName = funNamesVars[0]
        else:
            funName = funNamesVars[0]
            funVars = splitVars(funNamesVars[1])
    else:
        returnVars = splitVars(lls[0])
        isReturn = True
        funNamesVars = lls[1].strip(')').split('(')
        if len(funNamesVars) == 1: # not varargin
            funName = funNamesVars[0]
        else:
            funName = funNamesVars[0]
            funVars = splitVars(funNamesVars[1])
    
    pyline = 'def'+space+','.join(returnVars)+' = '+funName+'(' + ','.join(funVars) + '):'
    print(pyline)
    return pyline, isReturn
    
pylines = []*len(newlines)
for idx,line in enumerate(newlines):
    #handle the function
    if line.startswith('function'):
        handleFunction(line)
        
# with open('path_to_examples+'):
    