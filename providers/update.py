import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-sysprep --update'
	else:
		cmd = 'virt-sysprep -q --update'
	os.system(cmd)