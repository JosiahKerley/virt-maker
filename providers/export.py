import os
def provider(body,hash,args,verbose,image):
        retval = False
        if args == "": args = False
        if args and not args == 'export':
				if verbose:
					cmd = 'qemu-img convert -p -f qcow2 -O qcow2 %s "%s"'%(hash,args)
				else:
					cmd = 'qemu-img convert -f qcow2 -O qcow2 %s "%s"'%(hash,args)
                return(os.system(cmd))