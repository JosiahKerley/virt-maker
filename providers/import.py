import os
def provider(body,hash,args,verbose,image,settings):
	if os.path.isfile(args):
		pass
	elif os.path.isfile('%s/%s'%(settings['imgcache'],args)):
		args = '%s/%s'%(settings['imgcache'],args)
	else:
		return('Cannot find "%s"'%(args))
	if verbose:
		cmd = 'qemu-img convert -O qcow2 %s %s'%(args,hash)
		print(cmd)
	else:
		cmd = 'qemu-img convert -O qcow2 %s %s >/dev/null 2>&1'%(args,hash)
	return(os.system(cmd))