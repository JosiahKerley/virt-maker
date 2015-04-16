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
	if os.path.isfile(args):
		pass
	elif os.path.isfile('%s/%s'%(settings['imgcache'],args)):
		args = '%s/%s'%(settings['imgcache'],args)
	else:
		return('Cannot find "%s"'%(args))
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