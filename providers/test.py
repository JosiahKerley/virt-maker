import os
def info():
  print('')
def build(marshal):
  args = marshal['link']['argument']
  body = marshal['link']['body']
  hash = marshal['link']['last']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']

  retval = 0
  lines = body.split('\n')
  for cmd in lines:
    if verbose:
      cmd = '%s'%(cmd)
      print(cmd)
    else:
      cmd = '%s >/dev/null 2>&1'%(cmd)
    retval += os.system(cmd)
  if os.system(cmd) == 0:
    marshal['status'] = True
  else:
    marshal['status'] = False
  return(marshal)