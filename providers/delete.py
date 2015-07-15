import os
def info():
	print('Deletes file/folder')
def pre(marshal):
	command = marshal['link']['provider']
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
		cmd = 'virt-customize --delete %s'%(args.replace(' ',','))
	else:
		cmd = 'virt-customize -q --delete %s >/dev/null 2>&1'%(args.replace(' ',','))
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)