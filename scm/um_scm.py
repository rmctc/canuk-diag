#!/usr/bin/env python


import os.path
import imp

_default_config='%s/default_config.py' % './config'
_user_config='%s/user_config.py' % './config'


def main():
    
    global config

    if os.path.isfile(_user_config):
        config=imp.load_source('config', _user_config)
    else:
        config=imp.load_source('config', _default_config)
if __name__=='__main__':
    
    main()
    print(config.summary)
