import os
def provider(body,hash,args,verbose,image,settings):
	if verbose:
		cmd = 'virt-sysprep -a %s'%(hash)
	else:
		cmd = 'virt-sysprep -q -a %s >/dev/null 2>&1'%(hash)
	return(os.system(cmd))