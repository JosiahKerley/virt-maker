import os
import uuid
def info():
	return('')
def pre(marshal):
	command = 'virt-customize'
	from distutils.spawn import find_executable
	if not find_executable(command):
		print("Cannot find file '%s'"%(command))
		marshal['status'] = False
	return(marshal)
def provider(marshal):
	args = marshal['link']['arguments']
	body = marshal['link']['body']
	verbose = marshal['settings']['verbose']

	## Create the temp script
	filename = '.virt-maker_file-%s.tmp'%str(uuid.uuid4())
	with open(filename,'w') as f: f.write(body)

	## Parse args
	if args == "":
		args = False
	else:
		args = args.split(' ')
	dest = args[0]
	dir = os.path.dirname(dest)
	if verbose:
		cmd = 'virt-customize --mkdir "%s" --upload "%s":"%s" -a %s'%(dir,filename,dest,hash)
		print cmd
	else:
		cmd = 'virt-customize -q --mkdir "%s" --upload "%s":"%s" -a %s >/dev/null 2>&1'%(dir,filename,dest,hash)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)