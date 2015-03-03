import os
def provider(body,hash,args,verbose,image,settings):
	cmd = 'qemu-img'
	if verbose:
		cmd = '%s %s'%(cmd,args)
		print(cmd)
	else:
		cmd = '%s %s >/dev/null 2>&1'%(cmd,args)
	return(os.system(cmd))