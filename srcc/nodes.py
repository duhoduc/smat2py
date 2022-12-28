# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:24:29 2022

@author: Du Ho
"""
# We distinguish three types of 
class _function():
    def __init__(self):
        # create seeds
        self.name = 'foo'
        self.inputs = ['']
        self.outputs = ['']
        
    def islastnode(self,lastnode = True):
        self.previousNodes = []
        self.nextNodes = []
        
    def isbuiltin(self):
        pass
    
    def inputs(self):
        self.inputs = ['input1', 'input2']
        
    def outputs(self):
        self.outputs = ['output1', 'output2']
    
    def refer2(self):
        self.module = ''
        self.path = 'fft.fft'
        self.name = 'fftshift'
    
    def addtree(self,nextnode, callnode):
        if not hasattr(self,'previousNodes'):
            self.previousNode = callnode
        else:
            self.previousNode.append(callnode)
        
        self.nextnode.addtree([],self)
        
    def to_string(self):
        return self.__repr__
    
    def to_file(self,filename = 'foo.py'):
        with open(filename,'r') as f:
            f.write(self.tp_string())


        

class _variable():
    # A variable name must start with a letter or the underscore character
    # A variable name cannot start with a number
    # A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
    # Variable names are case-sensitive (age, Age and AGE are three different variables)
    def __init__(self):
        self.name = ''
        
class _global(_variable):
    # Variables that are created outside of a function (as in all of the examples above) are known as global variables.
    # Global variables can be used by everyone, both inside of functions and outside.
    def __init__(self):
        super().__init__()
        



class _class():
    # classdef...end — Definition of all class components
    # properties...end — Declaration of property names, specification of property attributes, assignment of default values
    # methods...end — Declaration of method signatures, method attributes, and function code
    # events...end — Declaration of event name and attributes
    # enumeration...end — Declaration of enumeration members and enumeration values for enumeration classes
    def __init__(self):
        self.name = ''
        self.functions = []
        self.staticfunctions = []
        self.properties = []
        
        
class _operator():
    def __init__(self):
        pass


