# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:08:56 2022

@author: Du Ho
"""
Conversion from matlab code to python, handle with text and verify the structure
idea: develop node, define the function tree
develop catchkey, catch the keywords in the matlab function, check if this is built in function or variable
or custom function
+ built in, request, the equivalence
+ matrix will be use np.ndarray, some built in function for matrix we would use broadcasting, etc

A tokenizer or scanner analyzes a string to categorize groups of characters. 
This is a useful first step in writing a compiler or interpreter.

The text categories are specified with regular expressions. The technique is   
to combine those into a single master regular expression and to loop over successive matches: