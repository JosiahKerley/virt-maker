import os
def provider(body,hash,args,verbose,image,settings):
	sed = "sed -i '/^SELINUX=.*/s/^SELINUX=.*/SELINUX=%s/g' /etc/selinux/config"
	if   'disabl' in args.lower(): command = sed%('disabled')
	elif 'enforc' in args.lower(): command = sed%('enforcing')
	elif 'permis' in args.lower(): command = sed%('permissive')
	else: return('Unknown argument')
	if verbose:
		cmd = 'virt-customize --run-command "%s" -a %s'%(command,hash)
	else:
		cmd = 'virt-customize -q --run-command "%s" -a %s >/dev/null 2>&1'%(command,hash)
	return(os.system(cmd))