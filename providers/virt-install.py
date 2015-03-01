import os
cmd = 'virt-install '
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = '%s %s'%(cmd,args)
	else:
		cmd = '%s --quite %s'%(cmd,args)
	return(os.system(cmd))