import os
import uuid
def provider(body,hash,args,verbose,image):

	## Create the temp script
	filename = '.virt-maker_shell-%s.sh'%str(uuid.uuid4())
	with open(filename,'w') as f: f.write(body)

	## Parse args
	if args == "":
		args = False
	else:
		args = args.split(' ')
	if args[0] == 'chroot':
		try: bin = args[1]
		except: bin = '/bin/bash'
		image.mount(hash)
		cmd = "chroot ./ %s -c '%s %s ; exit'"%(bin,bin,filename)
		os.system(cmd)
		image.unmount(hash)
	elif args[0] == 'boot':
		if verbose:
			cmd = 'virt-sysprep --firstboot "%s" --operations script -a %s'%(filename,hash)
		else:
			cmd = 'virt-sysprep -q --firstboot "%s" --operations script -a %s'%(filename,hash)
		os.system(cmd)
	else:
		if verbose:
			cmd = 'virt-sysprep --run "%s" --operations firstboot -a %s'%(filename,hash)
		else:
			cmd = 'virt-sysprep -q --run "%s" --operations firstboot -a %s'%(filename,hash)
		os.system(cmd)

	