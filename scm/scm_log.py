from scm import scm_lists
        
log=scm_lists.SCMjoblist()

# This is where we add the entries...
# Format is...
# log.add(<runid>, <run description>, <UM version>,
#         [<filename1>, <descriptions of filename1>, <label for filename1>, 
#         <filename2>, <descriptions of filename2>, <label for filename2>,  
#         ])
# Then list here is to support multiple files for a given run, e.g. for testing 
# different vertical resolutions etc. but with same basic executable.

log.add('dlwca', 'Initial standard run from Adrian', '8.2',
        [('constrain_GA4ish_TnucM18conv.nc', 'Initial setup from Adrian', 'Default'),
         ]
        )

log.add('dlwcb', 'As dlwca, but with BL dependent Tnuc', '8.4',
        [('constrain_GA4ish_KprofCu2test.nc', 'As dlwca, but with BL dependent Tnuc', 'Tnuc_BL'),
         ]
        )
