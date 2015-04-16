import os
def info():
	return('Deletes file/folder')
def pre(marshal):
	command = marshal['link']['provider']
	from distutils.spawn import find_executable
	if not find_executable(command):
		print("Cannot find file '%s'"%(command))
		marshal['status'] = False
	return(marshal)
def provider(marshal):
	args = marshal['link']['arguments']
	verbose = marshal['settings']['verbose']
	if verbose:
		cmd = 'virt-customize --delete %s'%(args.replace(' ',','))
	else:
		cmd = 'virt-customize -q --delete %s >/dev/null 2>&1'%(args.replace(' ',','))
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)