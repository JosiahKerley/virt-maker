import os
def provider(image,body,hash,args=False):
	cmd = 'virt-sysprep -q --hostname %s --operations hostname -a %s'%(args,hash)
	os.system(cmd)