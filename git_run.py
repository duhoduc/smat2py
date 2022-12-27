# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import numpy as np
import sys
import json

#%%

import subprocess
import os
import time
import subprocess
class git():
    @staticmethod
    def toJson(currObj,filename = 'things.json',ident = 4,overwrite = True):
        #toJson covert to json string and write to a file
        path2repo = os.path.dirname(os.path.abspath(__file__))
        path2json = os.path.join(path2repo, filename)
        if os.path.isfile(path2json) and not overwrite:
            isWrite = False
        else:
            isWrite = True
        if isWrite:
            jsonstr = json.dumps(currObj, indent=ident)
            # Writing to sample.json
            with open(path2json, "w") as jsonfile:
                jsonfile.write(jsonstr)
                
    @staticmethod
    def fromJson(filename = 'things.json'):
        path2repo = os.path.dirname(os.path.abspath(__file__))
        path2json = os.path.join(path2repo, filename)
        with open(path2json,'r') as json_file:
            things = json.load(json_file)
        return things
    
    @staticmethod
    def getlist(path2repo,debug=False):
        if os.path.isfile(path2repo):
            print(f'warning: {path2repo} is a file')
            currFiles = path2repo.split('\\')[-1]
            currName = currFiles.split('.')[0]
            return currName, currFiles
        elif os.path.isdir(path2repo):
            # get the current folder
            currFolder = path2repo.split('\\')[-1]
            currObj = dict()
            # get the listdir
            things  = os.listdir(path2repo)
            for thing in things:
                if not thing.startswith('.git'): # ignore .git
                    # get the obsolute path 
                    path2thing = os.path.join(path2repo,thing)
                    if debug:
                        print(path2thing)
                    # two case, folder and file
                    if os.path.isfile(path2thing):
                        # thing is file, separate by '.' and add to struct seed
                        currObj[thing.split('.')[0]] = thing
                        
                    elif os.path.isdir(path2thing):
                        if debug:
                            print(path2thing)
                        folderName, folderObj = git.getlist(path2thing)
                        currObj[folderName] = folderObj
                        # setattr(currObj,folderName, folderObj)
                    else:
                        pass
            return currFolder, currObj
        else:
            raise ValueError(f'{path2repo} is not valid path.')
    
    @staticmethod
    def gitActions(path2repo, command = 'init',url = None, commitMess = 'init commit', branch='main',filename = '.'):
        # single command
        if url is None:
            url = 'git@github.com:duhoduc/smat2py.git'
        commands = ['init','status','clone','add','commit','remote_add','branch','checkout','push','pull',
                    'merge','delete','help']
        cmd = ['git']
        if command in commands or not os.path.isdir(path2repo):
            if command == 'init':
                #Create an empty Git repository or reinitialize an existing one
                cmd.extend([command,path2repo])
                out,error = git.gitRun(cmd, path2repo)
            
            elif command == 'status':
                cmd.append('status')
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'clone':
                #Clone a repository into a new directory
                cmd.extend(['clone',url])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'add':
                #Add file contents to the index
                if filename == '.': # add all files
                    print('Warning: added all files to commit')
                    cmd.extend([command,'.'])
                    out,error = git.gitRun(cmd, path2repo)
                else:
                    cmd.extend([command,filename])
                    out,error = git.gitRun(cmd, path2repo)

            elif command == 'commit':
                cmd.extend([command,'-m',commitMess])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'remote_add':
                cmd.extend(['remote','add','origin',url])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'push':
                cmd.extend(['push','origin',branch])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'branch':
                #List, create, or delete branches
                if branch == '':
                    cmd.extend([command])
                else:
                    cmd.extend([command,branch])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'checkout':
                cmd.extend([command,branch])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'pull':
                cmd.extend([command,'origin',branch])
                out,error = git.gitRun(cmd, path2repo)
            
            elif command == 'merge':
                git.gitActions(path2repo,'checkout',branch = 'main')
                cmd.extend(['merge',branch])
                out,error = git.gitRun(cmd, path2repo)
                
            elif command == 'delete':
                #delete local branch
                if branch == 'main':
                    print(f'Wwarning: main will not be deleted')
                else:
                    print(f'Wwarning: {branch} is going to be deleted')
                    cmd.extend(['branch','--delete',branch])
                    out,error = git.gitRun(cmd, path2repo)
                    #delete remote branch
                    cmd.extend(['push','origin','--delete',branch])
                    out,error = git.gitRun(cmd, path2repo)
            elif command == 'help':
                cmd.extend([command,'-a'])
                out,error = git.gitRun(cmd, path2repo)
            return out.decode(),error.decode()
        
        else:
            print(f'{command} is not valid')
        
    @staticmethod
    def gitRun(cmd, path2repo = None):
        if path2repo is None or not os.path.isdir(path2repo):
            # not valid path, getcwd()
            path2repo = os.getcwd()
        pipe = subprocess.Popen(cmd, shell=True, cwd=path2repo,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
        out, error = pipe.communicate()
        pipe.wait()
        return out,error

#%%
pp = "C:\\Users\\Du Ho\\OneDrive - Qamcom Research & Technology AB\\ICX KaSS\\smat2py"
pp2 = "C:\\ICX\\uute\\uutModule"


currFolder, currObj = git.getlist(pp)
git.toJson(currObj)
currObj2 = git.fromJson()
currFolder2, currObj2 = git.getlist(pp2)



#%%
path2repo = "C:\\Users\\Du Ho\\OneDrive - Qamcom Research & Technology AB\\ICX KaSS\\smat2py"
url = "git@github.com:duhoduc/smat2py.git"


#%% test clone
url_clone = 'git@github.com:duhoduc/smop.git'
path2main_repo = os.path.dirname(path2repo)
out,error = git.gitActions(path2main_repo,command = 'clone',url = url_clone)
print(out,error)

#%% init

out,error = git.gitActions(path2repo,command = 'init')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'add')
print(out,error)
#%%


out,error = git.gitActions(path2repo,command = 'commit',commitMess = 'new delete git_run.py')

print(out,error)
#%%
out,error = git.gitActions(path2repo,command = 'branch',branch='main')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'branch',branch='test')
print(out,error)

#%% get list branch
out,error = git.gitActions(path2repo,command = 'branch',branch='')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'checkout',branch='main')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'checkout',branch='test')
print(out,error)

#%% recover delete files
# git checkout HEAD . in main branch

#%%
out,error = git.gitActions(path2repo,command = 'remote_add',url = url)
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'push',branch_name = 'test')
print(out,error)


#%%
out,error = git.gitActions(path2repo,command = 'branch_test')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'checkout',branch_name='main')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'checkout',branch_name='test')
print(out,error)

#%% recover delete files
# git checkout HEAD . in main branch

#%%
out,error = git.gitActions(path2repo,command = 'remote_add',url = url)
print(out,error)

#%%
#%%
out,error = git.gitActions(path2repo,command = 'push',branch = 'main')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'push',branch = 'test')
print(out,error)

#%%
out,error = git.gitActions(path2repo,command = 'pull',branch = 'main')
print(out,error)
# gitCommit(uploaddate, repoDir)
# gitPush(repoDir)

#%% merge two branch
out,error = git.gitActions(path2repo,command = 'merge',branch = 'test')
print(out,error)
 # after fixing merge conflict, we just have to push origin main


#%%
out,error = git.gitActions(path2repo,command = 'status')
print(out,error)

#%% help
out,error = git.gitActions(path2repo,command = 'help')
print(out,error)

#%% delete
out,error = git.gitActions(path2repo,command = 'delete',branch = 'test')
print(out,error)



