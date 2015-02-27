import os
def provider(body,hash,args,verbose,image):
        retval = False
        if args == "": args = False
        if args and not args == 'export':
                current = os.getcwd()
                os.chdir('..')
                lastsnap = (current.split('/')[-1]).replace('_mount','')
                cmd = 'qemu-img convert -f qcow2 -O qcow2 %s "%s"'%(lastsnap,args)
                retval = os.system(cmd)
                os.chdir(current)
        return(retval)