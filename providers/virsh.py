import os
def provider(body,hash,args,verbose,image,settings):
	cmd = 'virsh'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s %s >/dev/null 2>&1'%(cmd,args)
	#return(os.system(cmd))
	os.system(cmd)
	return(0)
	