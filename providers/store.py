import os
def provider(body,hash,args,verbose,image,settings):
	args = ('%s/%s'%(settings['imgcache'],args.split('/')[-1])).replace('//','/')
	retval = False
	if args == "": args = False
	if args and not args == 'export':
		if verbose:
			cmd = 'qemu-img convert -f qcow2 -O qcow2 %s "%s"'%(hash,args)
			print(cmd)
		else:
			cmd = 'qemu-img convert -p -f qcow2 -O qcow2 %s "%s" >/dev/null 2>&1'%(hash,args)
	return(os.system(cmd))