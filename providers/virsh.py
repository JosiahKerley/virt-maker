import os
def provider(body,hash,args,verbose,image):
	cmd = 'virsh'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s %s >/dev/null'%(cmd,args)
	#return(os.system(cmd))
	os.system(cmd)
	return(0)
	