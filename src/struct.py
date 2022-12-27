import numpy as np
import scipy.io as spio
import json
import sys, os
import copy
# sys.path.append('..\..')

# - using dict, the built-in dictionary type in Python, which is actually
#  a key-value array of items;
# - using an empty class or a temporary class, and then adding required fields to it;
# - using a hard-coded class, with all required fields and methods;
# - and using collections.namedtuple class, which is a tuple with keys for each 
#   item, and that is an immutable type.

# MATLAB convert struct to dict, we want to use class instead dict for parameters
# we coould define the class for init parameter, but we can also read from mat file or json file
def jsonPars(filename='jsonPars.json',load=False):
    '''
    read the parameter struct, including also matrix of struct from matlab

    Parameters
    ----------
    filetype : TYPE, optional
        DESCRIPTION. The default is 'mat'.
    fileName : TYPE, optional
        DESCRIPTION. The default is 'allPars.mat'.

    Returns
    -------
    None.

    '''
    if load:
        try:
            with open(filename) as json_file:
                dictPars = json.load(json_file)
        except:
            sys.exit(f'file {filename} is not available')
    else:
        dictPars = {}
                
    return struct(dictPars)
    


class matlabRepr():
    def __init__(self):
        pass
    # TODO overwrite __repr__ for seeing only the attributes name:value
    def _isMatlabRepr(self):
        return True
    
    def whatclass(self):
        return self.__class__.__name__
    
    def fieldnames(self):
        '''
        Get all fieldnames of this class
        '''
        #return list(self.__dict__.keys())#
        #return [key for key in self.__dict__.keys()]
        # Dictionary Keys to List using Unpacking with * 
        return [*self.__dict__]
    
    def methods(self):
        #methods get string of methods, similar to matlab
        fldNames = self.fieldnames()
        allDir = self.__dir__()
        strOut = ''
        strOut += (f'Methods for class {self.__class__.__name__}:\n')
        for eleDir in allDir:
            if eleDir not in fldNames:
               strOut+=(f' {eleDir} \n')
        print(strOut)
    
    def properties(self):
        return self.fieldnames()
    
    @staticmethod
    def is_staticmethod(cls, m):
        return isinstance(cls.__dict__.get(m), staticmethod)
        
    def isfield(self,field):
        '''
        Determine if input is structure array field
        '''
        fields = self.fieldnames()
        if field in fields:
            return True
        else:
            return False
        
    def setfield(self,field,value):
        if self.isfield(field):
            setattr(self,field,value)
            return True
        else:
            return False
            
            
    def getfield(self,field):
        '''
        Field of structure array
        '''
        if self.isfield(field):
            return getattr(self,field)
        else:
            print(f'{field} is not a field of this class')
            
    def __repr__(self):
        '''
        represent the class, using fieldnames for debugging

        Returns
        -------
        None.

        '''
        fldNames = self.fieldnames()
        if len(fldNames) == 0:
            strOut = 'class with no fields'
        else:
            # get the longest fldNamemax fldNames_len
            len_max = max([len(fldName) for fldName in fldNames])
            strOut = ''
            for fldName in fldNames:
                fldElem = self.getfield(fldName)
                # Combine fldName and fldElem
                strSpace = ' '*(len_max+4-len(fldName))
                if isinstance(fldElem,(list,struct)):
                    try: # Check if struct
                        if fldElem.isstruct():
                            strOut+=(f'{strSpace} {fldName}: [{len(fldElem)}x1 struct]\n')
                    except: # should be a list
                        if len(fldElem)==0:
                            strOut+=(f'{strSpace} {fldName}: []\n')
                        else:
                            try:
                                if fldElem[0].isstruct():
                                    strOut+=(f'{strSpace} {fldName}: [{len(fldElem)}x1 struct]\n')
                            except:
                                strType = fldElem[0].__class__.__name__
                                strOut+=(f'{strSpace} {fldName}: [{len(fldElem)}x1 {strType}]\n')
                else:
                    if fldElem is None:
                        strOut+=(f'{strSpace} {fldName}: []\n')
                    else:
                        if isinstance(fldElem,np.ndarray):
                            strOut+=(f'{strSpace} {fldName}: [{fldElem.shape} ndarray]\n')
                        else:
                            # Handle if instance as attribute of instance
                            try:
                                if fldElem._isMatlabRepr():
                                    fldElem_str = f'[1x1 {fldElem.__class__.__name__}]'
                            except:
                                fldElem_str = fldElem.__repr__()
                            strOut+=(f'{strSpace} {fldName}: {fldElem_str}\n')
                            
        return strOut #f'{self.fieldnames()}'
    
    
class struct(matlabRepr):
    '''
    dataclasses is alternative, python does not support struct as matlab, we could define a class for struct
    '''
    def __init__(self,dict_value=None,filename='allPars.mat',load=False,debug=False):
        '''
        recursive generate a class to represent similarly to struct
        Parameters
        ----------
        filename : MATfile, optional
            DESCRIPTION. The default is 'allPars.mat'.
        dict_value : recursive dict, optional
            DESCRIPTION. The default is {}.
        load : BOOLEAN, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        '''
        super().__init__()
        # load parameters stored in mat file to a dict
        # print(filename)
        if dict_value is None:
            dict_value = {}
        if load:
            try:
                if '.mat' in filename:
                    dict_value = self.__loadMatFile(filename)
                elif '.json' in filename:
                    dict_value = self.__loadJsonFile(filename)
            except:
                print(f'file {filename} is not available')
                
        # Convert a dict to class properties
        for key,values in dict_value.items():
            if isinstance(values,(list,tuple)):
                # list and tuble need a loop
                setattr(self,key,[struct(value) if isinstance(value,dict) else value for value in values])
            else:
                # Dict call 1 more otherwise take values
                if isinstance(values,dict):
                    setattr(self,key,struct(values))
                else:
                    if debug:
                        print(f'{key} has type as {type(values)}: {isinstance(values,np.ndarray)}')
                    if isinstance(values,(int,float,complex)):
                        if values == int(values):
                            setattr(self,key,int(values))
                        else:
                            setattr(self,key,values)
                    else:
                        setattr(self,key,values)
                # setattr(self,key,struct(values) if isinstance(values,dict) else values)
                
    def __loadJsonFile(self,filename):
        with open(filename) as json_file:
            dictPars = json.load(json_file)
        return dictPars

    def __loadMatFile(self,filename):
        '''
        this function should be called instead of direct spio.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects
        '''
        # print(' in loadMatFile mat')
        data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
        return self.__check_keys(data)

    def __check_keys(self,data):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in data:
            if isinstance(data[key], spio.matlab.mio5_params.mat_struct):
                data[key] = self.__todict(data[key])
            elif isinstance(data[key], (np.ndarray,list,tuple)): # this is ndarray of struct
                data[key] = self.__tolist(data[key])
        return data

    def __todict(self, matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        parDicts = {}
        for key in matobj._fieldnames:
            value = matobj.__dict__[key]
            if isinstance(value, np.ndarray):
                # value is np.ndarray, we need to loop
                valueOut = self.__tolist(value)
                # check if valueOut is not empty list of number
                if valueOut and isinstance(valueOut[0],(int,float,complex)):
                    # We want to convert all arrays into ndarray
                    valueOut = np.array(valueOut)
                parDicts[key] = valueOut
            elif isinstance(value, spio.matlab.mio5_params.mat_struct):
                # value is a scalar dict, recursive 1 more
                parDicts[key] = self.__todict(value)
            else:
                # data is a scalar value, take it
                parDicts[key] = (value)
        return parDicts

    def __tolist(self,ndarray_dicts):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''
        elem_list = []

        for sub_elem in ndarray_dicts:
            if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                elem_list.append(self.__todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(self.__tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list
    
    def todict(self):
        out = {}
        fldNames = self.fieldnames()
        if len(fldNames) == 0:
            print('Warning: struct with no fields')
        else:
            for fldname in fldNames:
                ele = getattr(self,fldname)
                if isinstance(ele,struct):
                    ele_dict = ele.todict()
                    out[fldname] = ele_dict
                elif isinstance(ele,np.ndarray):
                    out[fldname] = ele.tolist()
                elif isinstance(ele,list):
                    elelist = []
                    for elei in ele:
                        if isinstance(elei, struct):
                            elelist.append(elei.todict())
                        else:
                            elelist.append(elei)
                    out[fldname] = elelist
                else:
                    out[fldname] = ele
        return out

    def toJson(self,filename = 'struct.json',ident = 4):
        #toJson covert to json string and write to a file
        jsonstr = json.dumps(self.todict(), indent=ident)
        # Writing to sample.json
        with open(filename, "w") as jsonfile:
            jsonfile.write(jsonstr)


    def __len__(self):
        if len(self.fieldnames())==0:
            return 0
        else:
            return 1
    
    def isstruct(self):
        # Determine if input is structure array
        return True
    
    def deepcopy(self):
        return copy.deepcopy(self)
    
    #TODO: should we implement some methods of MATLAB struct for this class
    # ctranspose   ismatrix     isvector     struct2cell  
    # display      isrow        permute      transpose    
    # iscolumn     isscalar     reshape 
    
    # struct	Structure array
    # fieldnames	Field names of structure, or public fields of Java or Microsoft COM object
    # getfield	Field of structure array
    # isfield	Determine if input is structure array field
    # isstruct	Determine if input is structure array
    # orderfields	Order fields of structure array
    # rmfield	Remove fields from structure
    # setfield	Assign value to structure array field
    # arrayfun	Apply function to each element of array
    # structfun	Apply function to each field of scalar structure
    # table2struct	Convert table to structure array
    # struct2table	Convert structure array to table
    # cell2struct	Convert cell array to structure array
    # struct2cell	Convert structure to cell array
    
def updateStruct(sOrg=None, sUpd=None, acceptNewFields=False):
    '''
    QRT lab, using in updating parameters based on ie., json file
    '''
    # sOrg contains all fields of sUpd, meaning sUpd is subset of sOrg
    if sOrg is None: # None
        return struct()
    else:
        sNew = sOrg
        
    if sUpd is None or not isinstance(sUpd,struct):
        return sNew

    
    strFields = sUpd.fieldnames()

    for idxFld in range(len(strFields)):
        fldName = strFields[idxFld]
        
        if not sOrg.isfield(fldName) and not acceptNewFields:
            sys.exit(f'{fldName} is not a field in the original struct')
        elif not sOrg.isfield(fldName) and acceptNewFields:
            setattr(sNew,fldName, getattr(sUpd,fldName))
        else: # same fieldname and accept, same fieldname and not accept
            if isinstance(getattr(sOrg,fldName),(struct,list)):
                # Get element for fieldname
                sOrgEle = getattr(sOrg, fldName)
                sUdpEle = getattr(sUpd, fldName)
                if isinstance(sOrgEle,struct) and not isinstance(sUdpEle,struct):
                    sys.exit(f'{fldName} is a substruct in the original struct but not in the update struct.')
                if isinstance(sOrgEle,list) and not isinstance(sUdpEle,list):
                    sys.exit(f'{fldName} is an array in the original struct but not in the update struct.')
                if len(sUdpEle) < len(sOrgEle):
                    sys.exit(f'{fldName} has more elements in the update struct than in the original struct. This is currently not supported.')
                
                for idxElem in range(len(sUdpEle)):
                    if isinstance(sOrgEle,list):
                        orgFldElem = sOrgEle[idxElem]
                        updFldElem = sUdpEle[idxElem]
                    else:
                        orgFldElem = sOrgEle
                        updFldElem = sUdpEle
                    if isinstance(orgFldElem,list) or isinstance(updFldElem,list):
                        if not (isinstance(orgFldElem,list) and isinstance(updFldElem,list)):
                            if isinstance(orgFldElem,list):
                                sys.exit(f'{fldName} is a cell in the original struct but not in the update struct.')
                            
                            if isinstance(updFldElem,list):
                                sys.exit(f'{fldName} is a cell in the update struct but not in the original struct.')
                        
                        
                        flgCellElem = True
                        orgFldElem = orgFldElem[0]
                        updFldElem = updFldElem[0]
                    else:
                        flgCellElem = False
                
                    if len(updFldElem)==0:
                        # This will happen when the update struct has a field that
                        # is an array of structs that dont populate all the
                        # elements
                        continue
                    newFldElem = updateStruct(orgFldElem,updFldElem,acceptNewFields)
                    if flgCellElem:
                        setattr(sNew,fldName, newFldElem)#[idxElem]
            else:
                setattr(sNew,fldName, getattr(sUpd,fldName))
        
    return sNew
if __name__ == '__main__':
    
    
    # aas = struct(filename = 'aasSignal1.mat',load=True)
    # sp = jsonPars('..\Matlab\sp.json',load = True)
    # spUpd = jsonPars('..\Matlab\spUpd.json',load = True)
    
    # spNew = updateStruct(sp,spUpd)
    
    filePath = (os.path.abspath(__file__))
    
    uutPar = dict()
    uutPar['fs_Hz'] = 100
    y = dict()
    y['a'] = 1
    y['b'] = 2
    uutPar['vel'] = [0,1,2,3,4,5,6,7,8,9]
    uutPar['y'] = y
    uutPar['tx'] = [dict([('fs',100),('Bw',10)])]
    uutPar['rx'] = dict([('fs_rx',100),('Bw_rx',10)])
    
    uutParUpd = dict()
    uutParUpd['tx'] = [dict([('fs',10.1)])]
    uutParUpd['fs_Hz'] = 200
    uutParUpd['rx'] = dict([('fs_rx',500),('Bw_rx',10)])
    
    uutParOrg = struct(uutPar)
    uutParUpd = struct(uutParUpd)

    uutParNew = updateStruct(uutParOrg,uutParUpd,False)
    uutParOrg = struct(uutPar)

