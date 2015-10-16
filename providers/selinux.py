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

  sed = "sed -i '/^SELINUX=.*/s/^SELINUX=.*/SELINUX=%s/g' /etc/selinux/config"
  if   'disabl' in args.lower(): command = sed%('disabled')
  elif 'enforc' in args.lower(): command = sed%('enforcing')
  elif 'permis' in args.lower(): command = sed%('permissive')
  elif 'label' in args.lower(): command = 'touch /.autorelabel'
  else: print('Unknown argument')
  if verbose:
    cmd = 'virt-customize --run-command "%s" -a %s'%(command,hash)
    print(cmd)
  else:
    cmd = 'virt-customize -q --run-command "%s" -a %s >/dev/null 2>&1'%(command,hash)
  if os.system(cmd) == 0:
    marshal['status'] = True
  else:
    marshal['status'] = False
  return(marshal)