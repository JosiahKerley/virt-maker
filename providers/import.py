import os
def provider(body,hash,args,verbose,image):
	if verbose:
		cmd = 'qemu-img convert -O qcow2 %s %s'%(args,hash)
		print(cmd)
	else:
		cmd = 'qemu-img convert -O qcow2 %s %s >/dev/null'%(args,hash)
	return(os.system(cmd))