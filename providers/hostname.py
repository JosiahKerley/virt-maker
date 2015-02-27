import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-sysprep --hostname %s --operations hostname -a %s'%(args,hash)
	else:
		cmd = 'virt-sysprep -q --hostname %s --operations hostname -a %s'%(args,hash)
	os.system(cmd)