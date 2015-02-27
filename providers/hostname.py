import os
def provider(body,hash,args=False,image):
	cmd = 'virt-sysprep -q --hostname %s --operations hostname -a %s'%(args,hash)
	os.system(cmd)