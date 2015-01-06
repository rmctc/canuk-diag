#!/usr/bin/env python
from scm import um_scm
from scm import scm_plot
from scm import standardize
import pylab

um_scm.initialize()

summary=um_scm.summary
config=um_scm.config

print(summary.log)
   

#Let's try plotting everythin that's there!
runids=um_scm.summary.log.entries.keys()
var_list=standardize.standardize_names(['tot_precip', 'wstar', 'qcl', 'time'], model='UM_SCM')
scm_data_group=scm_plot.read_scm(runids, config, summary, var_list=var_list)

# Now let's plot something
scm_plot.plot(scm_data_group, var_list)

pylab.show()
