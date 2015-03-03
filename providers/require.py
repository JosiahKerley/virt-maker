import os
def provider(body,hash,args,verbose,image,settings):
	retval = 0
	lines = body.split('\n')
	for cmd in lines:
		if verbose:
			cmd = '%s %s'%(cmd,args)
			print(cmd)
		else:
			cmd = '%s %s >/dev/null 2>&1'%(cmd,args)
		retval += os.system(cmd)
	return(retval)
	