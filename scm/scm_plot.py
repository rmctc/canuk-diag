''' This is where we read in the scm data and do some plotting. '''

import netCDF4
import standardize
import numpy
import pylab
import warnings


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
        self.runid=[]
        self.filename=[]
        self.label=[]
        self.scmdata=[]

    def add(self, runid, filename, label):
        ''' Add an entry '''
        id='%s--%s' % (runid, filename)
        if id not in self.ids:
            self.ids.append(id)
            self.runid.append(runid)
            self.filename.append(filename)
            self.label.append(label)
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

class ScmPlot(pylab.Axes):
    ''' Class to hold a custom pyplot.
    Currently just inherits from Axes()'''

    def __init__(self, fig, rect, *args, **kwargs):
        pylab.Axes.__init__(self, fig, rect, *args, **kwargs)

        
def plot(scm_data_group, var_list, runids=[], files={}, rectx=None, figx=None,
         ignore_dims=True, plot_config=None):
    ''' Create a plot.
    Standardized names are assumed for the variables.
    If runids is empty, then plot for all runids in scm_data_group.
    If files is empty, then plot for all filenames associated with the runids.
    If ignore_dims is True, then don't plot a variable if it has the same as it's dimensions
    plot_config will be a dictionary of configuration options used to customize 
    non-standard plots, annotating or for rotating axes.
    '''
    # Use all run ids unless specified
    if runids==[]: runids=scm_data_group.runid

    # Find entries for corresponding runids
    ids=[scm_data_group.runid.index(runid) for runid in runids]
    
    # Weed out the filenames that aren't needed
    for i, id_x in enumerate(ids):
        runid=scm_data_group.runid[id_x]
        if runid in files.keys():
            if scm_data_group.filename[id_x] not in files[runid]: 
                del ids[i]
                
 

    for var in var_list:
        if ignore_dims and var in standardize.dim_dicts.keys():
            continue
        if rectx is None:
            rect=[.1,.9,.1,.9]
        else:
            rect=rectx
            
        def plotAllIds():
            for iplot,id_x in enumerate(ids):
                dims=scm_data_group.scmdata[id_x].dimensions[var]
                data=scm_data_group.scmdata[id_x].variables[var]
                units=scm_data_group.scmdata[id_x].units[var]


                rank=len(dims)
                if rank>1:
                    warnings.warn('Still need to implement a method for plotting higher dimensional variables. Skipping variable: %s' % var, UserWarning)
                    return

                # Create a figure if needed
                if iplot==0:
                    if figx is None:
                        figure=pylab.figure()
                    else:
                        figure=figx
                axes=ScmPlot(figure, rect)

                dimvars=[]
                #is dimension variable available
                l_dimvars=True
                for i,dim in enumerate(dims):
                    if dim in scm_data_group.scmdata[id_x].variables.keys():
                        dimvars.append(scm_data_group.scmdata[id_x].variables[dim])
                    else:
                        l_dimvars=False

                if rank==1:
                    if l_dimvars:
                        pylab.plot(dimvars[0],data, label=scm_data_group.label[id_x])
                        pylab.xlabel('%s [%s]' % (dims[0], standardize.dim_dicts[dims[0]]['units']))
                    else:
                        pylab.plot(data)
                    pylab.ylabel('%s [%s]' % (var, units))

            return
        plotAllIds()
        pylab.legend()
        
def read_scm(runids, config, summary, scmdatagroup=None,
             files={}, var_list=[], l_standard=True, model='UM_SCM'):
    ''' Read in the netcdf data for the given runids.  Location of the data
    and it's description should be provided in config and summary.
    If not empty, 'files' contains a dictionary runid:filenames pairs where 
    filenames is a list of filenames to process for a given runid. If empty,
    then all associated files will be processed.
    If not empty, 'var_list' contains a list of variables to process. If empty,
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
        if files=={}: 
            files_list=[x[0] for x in summary.log.entries[runid].outfiles]
        else:
            files_list=files[runid]
            if files_list==[]:
                files_list=[x[0] for x in summary.log.entries[runid].outfiles]
        labels=[x[2] for x in summary.log.entries[runid].outfiles if x[0] in files_list]
                

        for i_f, f in enumerate(files_list):
            filename='%s/%s' % (data_dir, f)
            label=labels[i_f]
            scmdata=scmdatagroup.add(runid, filename, label)

            # Open up the netcdf file
            ncid=netCDF4.Dataset(filename, 'r')
            variables=ncid.variables

            # Which variables should we process (standardized names here)?
            if var_list==[]:
                    variable_list=[standardize.standardize_name(var, model=model) for var in variables.keys()]
            else:
                if l_standard:
                    variable_list=var_list
                else:
                    variable_list=[standardize.standardize_name(var, model=model) for var in var_list]
            
            for var_s in var_list:
                # Here we can translate variable names to a common name
                var=standardize.model_name(var_s, model=model)

                #Store the data (we need to standardize this too)
                var_sq,dim_sq=squeeze(variables[var][:])
                scmdata.variables[var_s]=var_sq
                scmdata.units[var_s]=variables[var].units
                scmdata.dimensions[var_s]=[variables[var].dimensions[d] for d in dim_sq]

            #Close the netcdf file
            ncid.close()
                
            
    return scmdatagroup
