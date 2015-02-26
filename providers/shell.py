import os
import uuid
def provider(body,hash,args=False):
	if args == "": args = False
	if args and not args == 'shell':
		bin = args
	else:
		bin = '/bin/bash'
	filename = '.virt-maker_shell-%s.sh'%str(uuid.uuid4())
	with open(filename,'w') as f: f.write(body)
	cmd = "chroot ./ %s -c '%s %s ; exit'"%(bin,bin,filename)
	#print cmd
	os.system(cmd)