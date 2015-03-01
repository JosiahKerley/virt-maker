import os
cmd = 'qemu-img '
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = '%s %s'%(cmd,args)
	else:
		cmd = '%s %s >/dev/null'%(cmd,args)
	return(os.system(cmd))