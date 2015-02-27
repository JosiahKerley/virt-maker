import os
def provider(image,body,hash,args=False):
	cmd = 'virt-sysprep -q --install %s'%(args.replace(' ',','))
	os.system(cmd)