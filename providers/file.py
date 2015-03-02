import os
import uuid
def provider(body,hash,args,verbose,image):

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
	return(os.system(cmd))	