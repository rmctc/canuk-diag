class SCMinfo(object):
    '''class containing the descriptive information for an SCM run'''
    pass

class SCMjoblist():
    ''' Class containing a list of SCM info entities '''

    def __init__(self):
        self.entries={}

    def add(self, runid, details, umversion, outfiles=None):
        self.entries[runid]=scminfo=SCMinfo()
        scminfo.runid=runid
        scminfo.details=details
        scminfo.umversion=umversion
        scminfo.exptid=runid[0:4]
        scminfo.jobid=runid[4]
        if outfiles is not None:
            scminfo.outfiles=[]
            for filename, details, shortdetails in outfiles:
                scminfo.outfiles.append([filename, details, shortdetails])
                
    def __repr__(self):
        x=['Summary of SCM runs available',
           '-----------------------------',]
        for k,v in self.entries.items():
            x.extend(['runid: %s' % k,
                      '\tdetails: \t%s' % v.details,
                      '\tum version: \t%s' % v.umversion,
                      '\toutput files: \t%s ' % '\n\t\t\t'.join([' : '.join(f) for f in v.outfiles])
                      ])
        return '\n'.join(x)
