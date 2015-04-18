import os
import uuid
def info():
	print('')
def build(marshal):
	args = marshal['link']['argument']
	body = marshal['link']['body']
	hash = marshal['link']['last']
	verbose = marshal['settings']['verbose']
	settings = marshal['settings']

	## Create the temp script
	filename = '.virt-maker_file-%s.tmp'%str(uuid.uuid4())
	with open(filename,'w') as f: f.write(body)

	## Parse args
	if verbose:
		cmd = 'virsh net-destroy %s; virsh net-define %s; virsh net-autostart %s; virsh net-start %s'%(args,args,filename,args)
		print cmd
	else:
		cmd = 'virsh net-destroy %s >/dev/null 2>&1; virsh net-define %s >/dev/null 2>&1; virsh net-autostart %s >/dev/null 2>&1; virsh net-start %s >/dev/null 2>&1'%(args,filename,args)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)