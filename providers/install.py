import os
def provider(body,hash,args=False,image):
	cmd = 'virt-sysprep -q --install %s'%(args.replace(' ',','))
	os.system(cmd)