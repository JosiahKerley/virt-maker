import os
def info():
	print('')
def pre(marshal):
	command = 'virt-sysprep'
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
		cmd = 'virt-sysprep -a %s'%(hash)
	else:
		cmd = 'virt-sysprep -q -a %s >/dev/null 2>&1'%(hash)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)