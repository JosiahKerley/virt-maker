defaults = {
	"connect":"qemu:///system",
	"virt-type":"kvm",
	"ram":"500",
	"disk":"path=<[args]>,size=10",
	"network":"network=default",
	"graphics":"vnc",
	"os-variant":"generic",
	"wait":"10",
}

import os
def provider(body,hash,args,verbose,image):
	for line in body.split('\n'):
		if '=' in line:
			left = line.split('=')[0]
			right = line.replace(left+'=','')
			defaults[left] = right
	cmdargs = ' '
	for i in defaults:
		cmdargs += ' --%s %s'%(i,defaults[i])
	cmdargs = cmdargs.replace('<[args]>',os.path.abspath(args))
	if verbose:
		cmd = 'virt-install --autostart %s --import --force'%(cmdargs)
	else:
		cmd = 'virt-install --autostart -q %s --import --force'%(cmdargs)
	print cmd
	return(os.system(cmd))