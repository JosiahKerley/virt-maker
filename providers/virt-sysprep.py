import os
def provider(body,hash,args,verbose,image):
	cmd = 'virt-sysprep'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s --quite %s >/dev/null'%(cmd,args)
	return(os.system(cmd))