import os
import uuid
import shutil
def provider(body,hash,args,verbose,image,settings):

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
		filename = os.path.abspath(filename)
		image.mount(hash)
		shutil.move(filename,'./%s'%(filename.split('/')[-1]))
		cmd = "chroot ./ %s -c '%s %s ; exit'"%(bin,bin,filename)
		retval = os.system(cmd)
		image.unmount(hash)
		return(retval)
	elif args[0] == 'boot':
		if verbose:
			cmd = 'virt-customize --firstboot "%s" -a %s'%(filename,hash)
		else:
			cmd = 'virt-customize -q --firstboot "%s" -a %s >/dev/null 2>&1'%(filename,hash)
		return(os.system(cmd))
	else:
		if verbose:
			cmd = 'virt-customize --run "%s" -a %s'%(filename,hash)
		else:
			cmd = 'virt-customize -q --run "%s" -a %s >/dev/null 2>&1'%(filename,hash)
		return(os.system(cmd))