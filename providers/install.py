import os
import re
def info():
  print('')

def pre(marshal):
  command = 'virt-customize'
  from distutils.spawn import find_executable
  if not find_executable(command):
    print("Cannot find file '%s'"%(command))
    marshal['status'] = False
  return(marshal)

def build(marshal):
  args = ((marshal['link']['argument']).replace(' ',',')).replace(',,',',')
  body = marshal['link']['body']
  hash = marshal['link']['last']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']

  if '--nochroot' in args:
    args = args.replace('--nochroot','')
    cmd = '%s'%(args)
  else:
    if verbose:
      cmd = 'virt-customize --install "%s" -a %s'%(args,hash)
    else:
      cmd = 'virt-customize -q --install "%s" -a %s >/dev/null 2>&1'%(args,hash)

  if os.system(cmd) == 0:
    marshal['status'] = True
  else:
    marshal['status'] = False
  return(marshal)
