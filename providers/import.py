import os
def info():
  print('Import/convert images for use in the buildchain')
def pre(marshal):
  command = 'qemu-img'
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
  if os.path.isfile(args):
    pass
  elif os.path.isfile('%s/%s'%(settings['store'],args)):
    args = '%s/%s'%(settings['store'],args)
  else:
    print('Cannot find "%s"'%(args))
  if verbose:
    cmd = 'qemu-img convert -O qcow2 %s %s'%(args,hash)
    print(cmd)
  else:
    cmd = 'qemu-img convert -O qcow2 %s %s >/dev/null 2>&1'%(args,hash)
  if os.system(cmd) == 0:
    marshal['status'] = True
  else:
    marshal['status'] = False
  return(marshal)