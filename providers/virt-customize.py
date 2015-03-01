import os
def provider(body,hash,args,verbose,image):
	cmd = 'virt-customize'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s --quite %s'%(cmd,args)
	return(os.system(cmd))