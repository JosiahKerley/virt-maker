import os
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
  args = marshal['link']['argument']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']

  if verbose:
    cmd = 'virt-customize --update -a %s'%(hash)
  else:
    cmd = 'virt-customize -q --update -a %s >/dev/null 2>&1'%(hash)
  if os.system(cmd) == 0:
    marshal['status'] = True
  else:
    marshal['status'] = False
  return(marshal)