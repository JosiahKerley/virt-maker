import os
def info():
	return('')
def provider(marshal):
	args = marshal['link']['arguments']
	body = marshal['link']['body']
	verbose = marshal['settings']['verbose']

	retval = 0
	lines = body.split('\n')
	for cmd in lines:
		if verbose:
			cmd = '%s'%(cmd)
			print(cmd)
		else:
			cmd = '%s >/dev/null 2>&1'%(cmd)
		retval += os.system(cmd)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)