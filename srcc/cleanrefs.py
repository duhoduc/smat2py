# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 13:21:27 2022

@author: Du Ho
"""
import numpy as np
ident = ' '*4
isFix = False
with open('__pyrefs.py','r') as file:
    outs = file.readlines()

comments = ['#','#%%','"""']

def find(array,value, idx0 = 0):
    # create the list of indices, where each array value == value
    # find the array, with 
    if idx0 == 0:
        idxs = np.nonzero(array==value)[0]
        firstcol = np.nonzero(np.diff(idxs)>1)[0][0]
        
    else:
        idxs = np.nonzero(array[idx0:] == value)[0]

idx_c = []
idx_coms = []
idx_mcoms = []

# need to remove \n\n\n
outs_processed = []

for idx, out in enumerate(outs):
    out = out.strip()
    if out.startswith(comments[1]):
        outs_processed.append(out)
        idx_c.append(idx)
        
    elif out.startswith(comments[0]):
        outs_processed.append(out)
        idx_coms.append(idx)
        
    elif out.startswith(comments[2]) and idx not in idx_mcoms: # multiple comment, need to find the last
        idx_mcoms.append(idx)
        idxnew = idx
        print(idxnew)
        idx_mcom = [idxnew]
        while idxnew<len(outs)-1:
            if outs[idxnew].endswith(comments[2]) or outs[idxnew+1].startswith(comments[2]):
                idx_mcom.append(idxnew)
                print(idxnew)
                idxnew = len(outs)
                
            idxnew+=1
    else: # seem to be code
        pass
    if '\tReturns' in out:
        out_ = out.split('\tReturns')
        
        print(out)
#%% test
import re
rest = re.findall(outs[0],'\n')


def replaces(strin, oldvalue, newvalue):
    # replace the strin for 
    pass

for idx in idx_c:
    print(outs[idx])
    
for idx in idx_coms:
    print(outs[idx])
    
    
#%%
import tokenize

with open('__pyrefs.py', 'rb') as f:
    tokens = tokenize.tokenize(f.readline)
    for token in tokens:
        print(token)
#%%
with tokenize.open('__pyrefs.py') as f:
    tokens = tokenize.generate_tokens(f.readline)
    for token in tokens:
        print(token)
        
        
        