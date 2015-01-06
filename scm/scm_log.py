from scm import scm_lists
        
log=scm_lists.SCMjoblist()

# This is where we add the entries...
log.add('dlwca', 'Initial standard run from Adrian', '8.2',
        [('constrain_GA4ish_TnucM18conv.nc', 'Initial setup from Adrian', 'Default'),
         ]
        )

log.add('dlwcb', 'As dlwca, but with BL dependent Tnuc', '8.4',
        [('constrain_GA4ish_KprofCu2test.nc', 'As dlwca, but with BL dependent Tnuc', 'Tnuc_BL'),
         ]
        )
