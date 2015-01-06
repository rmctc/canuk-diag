summary='''
This is the default configuration file.  
Please edit this file and save it as a user configuration file 
named user_config.py.  Also edit this summary.
NB The user config should not be uploaded to the repository.
'''
# Your user id
user_name=''
# Your home directory
home_directory='/home/spongebob'
# Your top level project directory
proj_dir='%s/proj' % home_directory
# Your top level scm output directory
scm_data_root='/home/spongebob/scm_data'
# Default experiment id
scm_exptid='xxxx'
# Default job id
scm_jobid='a'
# Plot output directory
plot_dir='%s/plots' % home_directory
# SCM log (a dictionary providing details of each scm run)
scm_log='%s/logfile.py' % proj_dir

