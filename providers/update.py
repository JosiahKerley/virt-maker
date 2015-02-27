import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-customize --update -a %s'%(hash)
	else:
		cmd = 'virt-customize -q --update -a %s'%(hash)
	os.system(cmd)