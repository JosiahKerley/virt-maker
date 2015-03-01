import os
def provider(body,hash,args,verbose,image):
	cmd = 'virt-install'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s --quite %s >/dev/null 2>&1'%(cmd,args)
	return(os.system(cmd))