import os
def provider(image,body,hash,args=False):
	cmd = 'virt-sysprep -q --update'
	os.system(cmd)