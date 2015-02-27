import os
import uuid
def provider(body,hash,args,verbose,image):

	## Create the temp script
	filename = '.virt-maker_file-%s.sh'%str(uuid.uuid4())
	with open(filename,'w') as f: f.write(body)

	## Parse args
	if args == "":
		args = False
	else:
		args = args.split(' ')
	dest = args[0]
	if verbose:
		cmd = 'virt-customize    --copy-in "%s:%s" -a %s'%(filename,dest,hash)
	else:
		cmd = 'virt-customize -q --copy-in "%s:%s" -a %s'%(filename,dest,hash)
	return(os.system(cmd))	