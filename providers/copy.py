import os
import uuid
def info():
	return('Copies file into snapshot')
def provider(marshal):
	args = marshal['link']['arguments']
	verbose = marshal['settings']['verbose']

	## Parse args
	if args == "":
		args = False
	else:
		args = args.split(' ')
	src = args[0]
	try: dest = args[1]
	except: dest = src
	if dest == "": dest = src
	dir = os.path.dirname(dest)
	if verbose:
		cmd = 'virt-customize --mkdir "%s" --upload "%s":"%s" -a %s'%(dir,src,dest,hash)
		print cmd
	else:
		cmd = 'virt-customize -q --mkdir "%s" --upload "%s":"%s" -a %s >/dev/null 2>&1'%(dir,src,dest,hash)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)