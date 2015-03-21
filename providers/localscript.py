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
	if args[0] == 'bash' or args == False:
		executor = "bash"
	else:
		executor = args[0]
	if verbose:
		cmd = '%s "%s"'%(executor,filename)
	else:
		cmd = '%s "%s"'%(executor,filename)
	return(os.system(cmd))
