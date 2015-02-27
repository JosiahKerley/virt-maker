import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-customize --hostname %s -a %s'%(args,hash)
	else:
		cmd = 'virt-customize -q --hostname %s -a %s'%(args,hash)
	return(os.system(cmd))