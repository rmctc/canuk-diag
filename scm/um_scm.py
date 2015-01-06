#!/usr/bin/env python

import os.path
import imp
import pylab


global config, summary
config=None
summary=None

_default_config='%s/%s/default_config.py' %  (os.path.dirname(__file__),'config')
_user_config='%s/%s/user_config.py' % (os.path.dirname(__file__),'config')

class Summary():
    ''' An object for summarizing what's available. '''

    def __init__(self, config):
        self.config=config

    def update_scm_jobs(self):
        self.scm_jobs=os.listdir(self.config.scm_data_root)
    
    def update_scm_log(self): 
        log=self.config.scm_log
        if os.path.isfile(log):
            log_module=imp.load_source('log_module', log)
            self.log=log_module.log
        else:
            raise NameError('''SCM log module not found''')
        
            
def initialize():

    global config, summary

    # Load in the configutation file 
    # (allows code to run without the use config
    # which may have sensitive data in it)
    if os.path.isfile(_user_config):
        config=imp.load_source('config', _user_config)
    else:
        config=imp.load_source('config', _default_config)
        print(config.summary)
        raise SystemExit

    # Load in the summary data
    summary=Summary(config)

    # Update with list of available jobs
    summary.update_scm_jobs()

    # Load in the scm log data
    summary.update_scm_log()

if __name__=='__main__':
    
    initialize()

    print(summary.log)
   
    import scm_plot
    import standardize

    #Let's try plotting everythin that's there!
    runids=summary.log.entries.keys()
    var_list=standardize.standardize_names(['tot_precip', 'wstar', 'qcl', 'time'], model='UM_SCM')
    scm_data_group=scm_plot.read_scm(runids, config, summary, var_list=var_list)

    # Now let's plot something
    scm_plot.plot(scm_data_group, var_list)

    pylab.show()
