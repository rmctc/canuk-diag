
import netCDF4
import standardize
import numpy

class ScmData(object):
    ''' Object to hold SCM data.  Later on we might want to generalize this
    to cope with the same variable naming and unit convention used by the 
    Canadian model.'''
    
    def __init__(self):
        ''' At the moment this is just a dictionary pointing to the data '''
        self.variables={}
        self.units={}
        self.dimensions={}
        

class ScmDataGroup():
    ''' A collection of scmdata objects '''
    def __init__(self):
        self.ids=[]
        self.scmdata=[]

    def add(self, id):
        ''' Add an entry '''
        if id not in self.ids:
            self.ids.append(id)
            self.scmdata.append(ScmData())
        return self.scmdata[self.ids.index(id)]
        

def squeeze(array):
    ''' Squeeze out the single dimension entries from array.  Also return
    the index of dimension which aren't squeezed.'''

    shape=array.shape
    dim_sq=[]
    for i, ld in enumerate(shape):
        if ld!=1:dim_sq.append(i)
    return numpy.squeeze(array), dim_sq

def read_scm(runids, config, summary, scmdatagroup=None,
             files=None, var_list=None, l_standard=True,):
    ''' Read in the netcdf data for the given runids.  Location of the data
    and it's description should be provided in config and summary.
    If not None, 'files' contains a dictionary runid:filenames pairs where 
    filenames is a list of filenames to process for a given runid. If None,
    then all associated files will be processed.
    If not None, 'var_list' contains a list of variables to process. If None,
    then all variables will be processed. 
    If l_standard is True, then variable names are the standardized names.
    If l_standard is False, then variables are SCM specific names.
    '''

    # Create a data handler if it's not already defined
    if scmdatagroup is None:
        scmdatagroup=ScmDataGroup()

    for runid in runids:
        data_dir='%s/%s' % (config.scm_data_root, runid)

        # Which files should we process for this runid?
        if files is None: 
            files_list=[x[0] for x in summary.log.entries[runid].outfiles]
        else:
            files_list=files[runid]
            if files_list is None:
                files_list=[x[0] for x in summary.log.entries[runid].outfiles]
        for f in files_list:
            filename='%s/%s' % (data_dir, f)

            id='%s--%s' % (runid, filename)
            scmdata=scmdatagroup.add(id)

            # Open up the netcdf file
            ncid=netCDF4.Dataset(filename, 'r')
            variables=ncid.variables

            # Which variables should we process (standardized names here)?
            if var_list is None:
                    variable_list=[standardize.standardize_name(var, model='UM_SCM') for var in variables.keys()]
            else:
                if l_standard:
                    variable_list=var_list
                else:
                    variable_list=[standardize.standardize_name(var, model='UM_SCM') for var in var_list]
            
            for var_s in var_list:
                # Here we can translate variable names to a common name
                var=standardize.model_name(var_s, model='UM_SCM')

                #Store the data (we need to standardize this too)
                var_sq,dim_sq=squeeze(variables[var][:])
                scmdata.variables[var]=var_sq
                scmdata.units[var]=variables[var].units
                scmdata.dimensions[var]=[variables[var].dimensions[d] for d in dim_sq]

            #Close the netcdf file
            ncid.close()
                
            
    return scmdatagroup
