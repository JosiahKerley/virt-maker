defaults = {
	"connect":"qemu:///system",
	#"virt-type":"kvm",
	"ram":"500",
	"disk":"path=<[args]>,size=10",
	"network":"network=default",
	"graphics":"vnc",
	#"os-variant":"generic",
	"wait":"0",
}
import os
def info():
	print('')
def pre(marshal):
	command = 'virt-install'
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
	name = args.split('/')[-1]
	name = name.replace(' ','_')
	for line in body.split('\n'):
		if '=' in line:
			left = line.split('=')[0]
			right = '='.join(line.split('=')[1:])
			defaults[left] = right
	if not 'name' in defaults: defaults['name'] = name
	cmdargs = ' '
	for i in defaults:
		cmdargs += ' --%s %s'%(i,defaults[i])
	
	if not os.path.isfile(args):
		storefile = '%s/%s'%(settings['imgcache'],args)
		storefile = storefile.replace('//','/')
		if os.path.isfile(storefile):
			args = storefile
		else:
			print('No image file found.')
	imgfile = os.path.abspath(args)
	cmdargs = cmdargs.replace('<[args]>',imgfile)
	os.system('virsh destroy %s'%(defaults['name']))
	os.system('virsh undefine %s'%(defaults['name']))
	if verbose:
		cmd = 'virt-install --autostart %s --import --force'%(cmdargs)
		print cmd
	else:
		cmd = 'virt-install --autostart -q %s --import --force >/dev/null 2>&1'%(cmdargs)
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)