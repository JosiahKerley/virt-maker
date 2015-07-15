import os
import uuid
import shutil

def info():
	print('')

def pre(marshal):
	command = 'virt-customize'
	from distutils.spawn import find_executable
	if not find_executable(command):
		print("Cannot find file '%s'"%(command))
		marshal['status'] = False
	return(marshal)

def build(marshal):
	args = marshal['link']['argument']
	body = marshal['link']['body']
	hash = marshal['link']['last']
	verbose = marshal['settings']['verbose']
	settings = marshal['settings']


	## Create the temp script
	filename = '.virt-maker_shell-%s.sh'%str(uuid.uuid4())
	with open(filename,'w') as f: f.write(body)

	## Parse args
	if args == "":
		args = False
	else:
		args = args.split(' ')
	if args[0] == 'boot':
		if verbose:
			cmd = 'virt-customize --firstboot "%s" -a %s'%(filename,hash)
		else:
			cmd = 'virt-customize -q --firstboot "%s" -a %s >/dev/null 2>&1'%(filename,hash)
	else:
		if verbose:
			cmd = 'virt-customize --run "%s" -a %s'%(filename,hash)
		else:
			cmd = 'virt-customize -q --run "%s" -a %s >/dev/null 2>&1'%(filename,hash)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)