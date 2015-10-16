import os
import urllib2
def info():
  print('')
def build(marshal):
  args = marshal['link']['argument']
  body = marshal['link']['body']
  hash = marshal['link']['last']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']
  if 1:
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
        if verbose: print('\tDownloading "%s"' % (args))
        CHUNK = 64 * 1024
        with open(filename, 'wb') as fp:
          while True:
            chunk = req.read(CHUNK)
            if not chunk: break
            fp.write(chunk)
        if verbose:
          print('\t"%s" complete' % (filename))
          marshal['status'] = True
    except:
      print('\tCannot download "%s"' % (args))
      marshal['status'] = False
  return(marshal)