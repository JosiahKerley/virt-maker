import os
import shutil

def build(marshal):
  args = marshal['link']['argument']
  body = marshal['link']['body']
  hash = marshal['link']['last']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']
  blueprintfile = marshal['blueprint']['path']

    
  if os.path.exists(blueprintfile):
    shutil.copy2(blueprintfile,settings['catalog'])
    marshal['status'] = True
    return(marshal)
  else:
    print('Cannot find "%s"' % (blueprintfile))
    marshal['status'] = False
    return(marshal)