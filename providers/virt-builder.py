import os
def build(marshal):
  args = marshal['link']['argument']
  body = marshal['link']['body']
  hash = marshal['link']['hash']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']
  ofile = '%s.img'%(args)
  ofile = ofile.replace(' ','')
  if not os.path.isfile(ofile) or settings['nodelta']:
    cmd = 'virt-builder'
    if verbose:
      cmd = '%s %s' % (cmd, args)
      print(cmd)
    else:
      cmd = '%s --quite %s >/dev/null 2>&1' % (cmd, args)
    if os.system(cmd) == 0:
      marshal['status'] = True
    else:
      print('Virt-Builder Failed!')
      marshal['status'] = False
  else:
    print('skipping...')
    marshal['status'] = 'Skip'
  return(marshal)