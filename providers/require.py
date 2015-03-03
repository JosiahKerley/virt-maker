import os
def provider(body,hash,args,verbose,image,settings):
	retval = 0
	lines = body.split('\n')
	for cmd in lines:
		if verbose:
			cmd = '%s'%(cmd)
			print(cmd)
		else:
			cmd = '%s >/dev/null 2>&1'%(cmd)
		retval += os.system(cmd)
	return(retval)
	