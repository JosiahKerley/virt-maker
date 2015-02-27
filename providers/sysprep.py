import os
def provider(image,body,hash,args=False):
	cmd = 'virt-sysprep -q -a %s'%(hash)
	os.system(cmd)