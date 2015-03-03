import os
def provider(body,hash,args,verbose,image,settings):
	virtmakercache = '/var/lib/virt-maker/cache'
	if os.path.isfile(args):
		pass
	elif os.path.isfile('%s/%s'%(virtmakercache,args)):
		args = '%s/%s'%(virtmakercache,args)
	else:
		return('Cannot find "%s"'%(args))
	if verbose:
		cmd = 'qemu-img convert -O qcow2 %s %s'%(args,hash)
		print(cmd)
	else:
		cmd = 'qemu-img convert -O qcow2 %s %s >/dev/null 2>&1'%(args,hash)
	return(os.system(cmd))