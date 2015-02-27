import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-sysprep --install %s'%(args.replace(' ',','))
	else:
		cmd = 'virt-sysprep -q --install %s'%(args.replace(' ',','))
	os.system(cmd)