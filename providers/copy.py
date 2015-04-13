import os
import uuid
def provider(body,hash,args,verbose,image,settings):

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
	return(os.system(cmd))