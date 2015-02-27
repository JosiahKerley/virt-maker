import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-customize --hostname %s --operations hostname -a %s'%(args,hash)
	else:
		cmd = 'virt-customize -q --hostname %s --operations hostname -a %s'%(args,hash)
	os.system(cmd)