import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'virt-customize --delete %s'%(args.replace(' ',','))
	else:
		cmd = 'virt-customize -q --delete %s'%(args.replace(' ',','))
	return(os.system(cmd))