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
  body = marshal['link']['body']
  hash = marshal['link']['last']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']

  if verbose:
    cmd = 'virt-customize --root-password password:%s -a %s'%(args,hash)
  else:
    cmd = 'virt-customize -q --root-password password:%s -a %s >/dev/null 2>&1'%(args,hash)
  if os.system(cmd) == 0:
    marshal['status'] = True
  else:
    marshal['status'] = False
  return(marshal)