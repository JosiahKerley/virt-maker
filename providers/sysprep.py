import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-sysprep -a %s'%(hash)
	else:
		cmd = 'virt-sysprep -q -a %s'%(hash)
	return(os.system(cmd))