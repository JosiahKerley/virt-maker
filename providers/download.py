import os
import urllib2
def provider(body,hash,args,verbose,image,settings):
        try:
                download = True
                filename = args.split('/')[-1]
                req = urllib2.urlopen(args)
                remotesize = int(req.headers["Content-Length"])
                if os.path.isfile(filename):
                        download = False
                        if not os.path.getsize(filename) == remotesize:
                                download = True
                if download:
                        if verbose: print('\tDownloading "%s"'%(args))
                        CHUNK = 64 * 1024
                        with open(filename, 'wb') as fp:
                                while True:
                                        chunk = req.read(CHUNK)
                                        if not chunk: break
                                        fp.write(chunk)
                        if verbose: print('\t"%s" complete'%(filename))
                return(0)
        except: return('\tCannot download "%s"'%(args))
