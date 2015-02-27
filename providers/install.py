import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-customize --install %s'%(args.replace(' ',','))
	else:
		cmd = 'virt-customize -q --install %s'%(args.replace(' ',','))
	os.system(cmd)