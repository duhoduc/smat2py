# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:54:35 2022

@author: Du Ho
"""

# Define constant similar between matlab and python

#Arithmetic Operators
Arithmetic_Operators = [ "+", "+", "-", "-", ".*", "*", "./", "/", ".\\ ", "\\", ".^", "^", ".'", "'"  ]
Relational_Operators = ["==","~=",">","<","<=",">="]
Logical_Operators = ["&","|","&&","||","~"]
Special_Characters = ["@",".","...",",",":",";","()","[]","{}","%","%{ %}","!","?","''","","\space","\newline",
                      "< &",".?"]

keywords = set("""and    assert  break class continue
    def    del     elif  else  except
    exec   finally for   from  global
    if     import  in    is    lambda
    not    or      pass  print raise
    return try     while with
    Data  Float Int   Numeric Oxphys
    array close float int     input
    open  range type  write
    len""".split())

funcion_keys = set(""" acos asin atan  cos e
    exp   fabs floor log log10
    pi    sin  sqrt  
    tan""".split())

optable = {
    "!" : "not",
    "~" : "not",
    "~=": "!=",
    "|" : "or",
    "&" : "and",
    "||": "or",
    "&&": "and",
    "^" : "**",
    "**": "**",
    ".^": "**",
    "./": "/",
    ".*": "*",
    ".*=" : "*",
    "./=" : "/",
    }

