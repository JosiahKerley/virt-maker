import os
def info():
	return('')
def pre(marshal):
	command = 'qemu-img'
	from distutils.spawn import find_executable
	if not find_executable(command):
		print("Cannot find file '%s'"%(command))
		marshal['status'] = False
	return(marshal)
def provider(marshal):
	args = marshal['link']['arguments']
	body = marshal['link']['body']
	verbose = marshal['settings']['verbose']

	cmd = 'qemu-img'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s %s >/dev/null 2>&1'%(cmd,args)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)