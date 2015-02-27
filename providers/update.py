import os
def provider(body,hash,args=False,image):
	cmd = 'virt-sysprep -q --update'
	os.system(cmd)