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
	verbose = marshal['settings']['verbose']

	if verbose:
		cmd = 'virt-customize --update -a %s'%(hash)
	else:
		cmd = 'virt-customize -q --update -a %s >/dev/null 2>&1'%(hash)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)