''' A few functions which help to standardize variable names and unit conventions.'''

dictionaries={
    'UM_SCM':
        {
        # NB Entries should be unique!
        'tot_precip':'total_precip',
        }
    }

global reverse_dict
reverse_dict={}

for key_x,dict_x in dictionaries.items():
    reverse_dict[key_x]={}
    for k,v in dictionaries[key_x].items():
        reverse_dict[key_x][v]=k
        
def standardize_name(var, model='UM_SCM'):
    ''' Return the standardize variable name '''
    if var in dictionaries[model].keys():
        # An update exists
        var_s=dictionaries[model][var]
    else:
        # Leave it as it was
        var_s=var
    return var_s

def model_name(var_s, model='UM_SCM'):
    ''' Return the model specific name '''
    if var_s in dictionaries[model].values():
        # An update exists
        var=reverse_dict[model][var_s]
    else:
        # Leave it as it was
        var=var_s
    return var
    
    
def standardize_names(var_list, model='UM_SCM'):
    var_list_s=[]
    for var in var_list:
        var_list_s.append(standardize_name(var, model))
    return var_list_s
