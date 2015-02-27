import os
def provider(body,hash,args=False,image):
	cmd = 'virt-sysprep -q -a %s'%(hash)
	os.system(cmd)