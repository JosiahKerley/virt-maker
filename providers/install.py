import os
def pre(marshal):
	command = 'virt-customize'
	from distutils.spawn import find_executable
	if not find_executable(command):
		print("Cannot find file '%s'"%(command))
		marshal['status'] = False
	return(marshal)
def provider(marshal):
	if verbose:
		cmd = 'virt-customize --install %s'%(args.replace(' ',','))
	else:
		cmd = 'virt-customize -q --install %s >/dev/null 2>&1'%(args.replace(' ',','))
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)