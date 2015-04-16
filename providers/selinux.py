import os
def info():
	return('')

def pre(marshal):
	command = 'virt-customize'
	from distutils.spawn import find_executable
	if not find_executable(command):
		print("Cannot find file '%s'"%(command))
		marshal['status'] = False
	return(marshal)

def provider(marshal):
	args = marshal['link']['arguments']
	body = marshal['link']['body']
	verbose = marshal['settings']['verbose']

	sed = "sed -i '/^SELINUX=.*/s/^SELINUX=.*/SELINUX=%s/g' /etc/selinux/config"
	if   'disabl' in args.lower(): command = sed%('disabled')
	elif 'enforc' in args.lower(): command = sed%('enforcing')
	elif 'permis' in args.lower(): command = sed%('permissive')
	elif 'label' in args.lower(): command = 'touch /.autorelabel'
	else: return('Unknown argument')
	if verbose:
		cmd = 'virt-customize --run-command "%s" -a %s'%(command,hash)
	else:
		cmd = 'virt-customize -q --run-command "%s" -a %s >/dev/null 2>&1'%(command,hash)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)