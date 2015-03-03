import os
def provider(body,hash,args,verbose,image,settings):
	if verbose:
		cmd = 'virt-customize --update -a %s'%(hash)
	else:
		cmd = 'virt-customize -q --update -a %s >/dev/null 2>&1'%(hash)
	return(os.system(cmd))