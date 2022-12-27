# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import numpy as np
import sys
import json
import git
from git.repo import Repo

pp = "C:\\Users\\Du Ho\\OneDrive - Qamcom Research & Technology AB\\ICX KaSS\\smat2py"
pp2 = "C:\\ICX\\uute\\uutModule"
#%=>startwith

#%<=endwith

def toJson(currObj,filename = 'things.json',ident = 4,overwrite = True):
    #toJson covert to json string and write to a file
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(path_to_folder, filename)
    if os.path.isfile(path_to_json) and not overwrite:
        isWrite = False
    else:
        isWrite = True
    if isWrite:
        jsonstr = json.dumps(currObj, indent=ident)
        # Writing to sample.json
        with open(path_to_json, "w") as jsonfile:
            jsonfile.write(jsonstr)
        
def fromJson(filename = 'things.json'):
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(path_to_folder, filename)
    with open(path_to_json,'r') as json_file:
        things = json.load(json_file)
    return things

def getlist(path_to):
    if os.path.isfile(path_to):
        print(f'warning: {path_to} is a file')
        currFiles = path_to.split('\\')[-1]
        currName = currFiles.split('.')[0]
        return currName, currFiles
    else:
        # get the current folder
        currFolder = path_to.split('\\')[-1]
        currObj = dict()
        # get the listdir
        things  = os.listdir(path_to)
        for thing in things:
            if not thing.startswith('.git'): # ignore .git
                # get the obsolute path 
                path_to_thing = os.path.join(path_to,thing)
                print(path_to_thing)
                # two case, folder and file
                if os.path.isfile(path_to_thing):
                    # thing is file, separate by '.' and add to struct seed
                    currObj[thing.split('.')[0]] = thing
                    
                elif os.path.isdir(path_to_thing):
                    
                    print(path_to_thing)
                    folderName, folderObj = getlist(path_to_thing)
                    currObj[folderName] = folderObj
                    # setattr(currObj,folderName, folderObj)
                else:
                    pass
        #
        return currFolder, currObj


currFolder, currObj = getlist(pp)
toJson(currObj)
currObj2 = fromJson()



# to automate git, we need to find the file, write the file list in the end of this file/json file

#%% Now we do git clone
# rorepo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with
repo = Repo(os.getcwd())
assert not repo.bare

#%%
rw_dir = os.getcwd()
bare_repo = Repo.init(os.path.join(rw_dir, "bare-repo"), bare=True)

#%%
cloned_repo = repo.clone(os.path.join(rw_dir, "smop"))

#%%
repository = Repo.init(pp)
repository.remotes.origin.set_url('git@github.com:duhoduc/smat2py.git')
repository.untracked_files
repository.is_dirty(untracked_files=True) # This returns true in this case
repository.index.add(['.'])
commit = repository.index.commit("This is our first commit")
repository.git.push('--set-upstream', 'origin', 'main')

#%%

import subprocess

import time
import subprocess
def gitActions(path2repo, url = None, command = 'init', commitMess = '"init commit"',branch_name = 'main'):
    if url is None:
        url = 'git@github.com:duhoduc/smat2py.git'
        
    commands = ['init','clone','add','commit','push','pull','remote_add', 'branch_main','branch_test',
                'checkout']
    cmd = ['git']
    if command in commands:
        if command == 'init':
            # Check if repoDir is dir
            if os.path.isdir(path2repo):
                cmd.append('init')
                cmd.append(path2repo)
                out,error = gitRun(cmd, path2repo)
            else:
                print('{path2repo} is not valid repo.')
        elif command == 'add':
            cmd.extend(['add','.'])
            # cmd.append('add')
            # cmd.append('.')
            out,error = gitRun(cmd, path2repo)
        elif command == 'commit':
            #git commit -m "init commit"
            cmd.extend(['commit','-m',commitMess])
            # cmd.append('commit')
            # cmd.append('-m')
            # cmd.append(commitMess)
            out,error = gitRun(cmd, path2repo)
            
        elif command == 'remote_add':
            cmd.extend(['remote','add','origin',url])
            # cmd.append('remote')
            # cmd.append('add')
            # cmd.append('origin')
            # cmd.append(url)
            out,error = gitRun(cmd, path2repo)
            
        elif command == 'push':
            cmd.extend(['push','origin',branch_name])
            # cmd.append('push')
            # cmd.append('-u')
            # cmd.append('origin')
            # cmd.append('main')
            # cmd.append(url)
            out,error = gitRun(cmd, path2repo)
            
        elif command == 'branch_main':
            cmd.extend(['branch','main'])
            out,error = gitRun(cmd, path2repo)
            
        elif command == 'branch_test':
            cmd.extend(['branch','test'])
            out,error = gitRun(cmd, path2repo)
            
        elif command == 'checkout':
            cmd.extend(['checkout',branch_name])
            out,error = gitRun(cmd, path2repo)
            
        elif command == 'clone':
            cmd.extend(['clone',url])
            out,error = gitRun(cmd, path2repo)
        elif command == 'pull':
            cmd.extend(['pull','origin',branch_name])
            out,error = gitRun(cmd, path2repo)
        return out,error
    else:
        print(f'{command} is not valid')

def gitCommit(commitMessage, repoDir):
    cmd = ['git','commit','-m', commitMessage]
    out,error = gitRun(cmd,repoDir)
    return out,error



def gitPush(repoDir):
    cmd = ['git','push']
    out,error = gitRun(cmd,repoDir)
    return out,error

def gitRun(cmd, path2repo):
    pipe = subprocess.Popen(cmd, shell=True, cwd=path2repo,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
    out, error = pipe.communicate()
    pipe.wait()
    return out,error


#%%
url='git@github.com:duhoduc/smop.git' # your git repository , windows your need to use double backslash for right directory.
gitActions(os.getcwd(),url )

#%%
path2repo = "C:\\Users\\Du Ho\\OneDrive - Qamcom Research & Technology AB\\ICX KaSS\\smat2py"
url = "git@github.com:duhoduc/smat2py.git"

#%% 
import os
path2main_repo = os.path.dirname(path2repo)
out,error = gitActions(path2main_repo,command = 'clone')
print(out,error)

#%% init

out,error = gitActions(path2repo,command = 'init')
print(out,error)

#%%
out,error = gitActions(path2repo,command = 'add')
print(out,error)
#%%

out,error = gitActions(path2repo,command = 'commit',commitMess = 'new gitrun')
print(out,error)
#%%
out,error = gitActions(path2repo,command = 'branch_main')
print(out,error)

#%%
out,error = gitActions(path2repo,command = 'branch_test')
print(out,error)

#%%
out,error = gitActions(path2repo,command = 'checkout',branch_name='main')
print(out,error)

#%%
out,error = gitActions(path2repo,command = 'checkout',branch_name='test')
print(out,error)

#%% recover delete files
# git checkout HEAD . in main branch

#%%
out,error = gitActions(path2repo,command = 'remote_add',url = url)
print(out,error)

#%%
out,error = gitActions(path2repo,command = 'push',branch_name = 'test')
print(out,error)

#%%
out,error = gitActions(path2repo,command = 'pull',branch_name = 'main')
print(out,error)
# gitCommit(uploaddate, repoDir)
# gitPush(repoDir)










