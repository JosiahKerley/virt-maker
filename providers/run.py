import os
def provider(body,hash,args,verbose,image,settings):
	if verbose:
		cmd = 'virt-customize --run-command "%s" -a %s'%(args,hash)
	else:
		cmd = 'virt-customize -q --run-command "%s" -a %s >/dev/null 2>&1'%(args,hash)
	return(os.system(cmd))