import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-sysprep --update -a %s'%(hash)
	else:
		cmd = 'virt-sysprep -q --update -a %s'%(hash)
	os.system(cmd)