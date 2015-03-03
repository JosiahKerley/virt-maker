import os
import urllib2
def provider(body,hash,args,verbose,image,settings):
	try:
		filename = args.split('/')[-1]
		f = urllib2.urlopen(args)
		remotesize = f.headers["Content-Length"]
		if os.path.isfile(filename) and not os.path.getsize(filename) == remotesize:
			if verbose: print('\tDownloading "%s"'%(args))
			CHUNK = 16 * 1024
			with open(filename, 'wb') as fp:
				while True:
					chunk = req.read(CHUNK)
					if not chunk: break
					fp.write(chunk)
			if verbose: print('\t"%s" complete'%(filename))
		return(0)
	except:
		return('\tCannot downloading "%s"'%(args))