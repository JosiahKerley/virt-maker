import os
import json
import subprocess


def getBuildchainFromFile(filepath):
  command = '/usr/local/bin/virt-maker --file ' + filepath + ' --dump-blueprint'
  stdout = subprocess.check_output(command, shell=True)
  #print stdout
  return(json.loads(stdout))


def info():
  print('')

def pre(marshal):
  args = marshal['link']['argument']
  body = marshal['link']['body']
  hash = marshal['link']['last']
  verbose = marshal['settings']['verbose']
  settings = marshal['settings']
  newchain = []


  ## Provider safety
  if marshal['link']['provider'] == 'from':

    ## Find reference file and get buildchain
    if os.path.exists(args):
      buildchain = getBuildchainFromFile(args)
    elif os.path.exists('%s/%s' % (settings['catalog'], args)):
      buildchain = getBuildchainFromFile('%s/%s' % (settings['catalog'], args))
    else:
      print('Cannot find "%s" or "%s"' % ('%s/%s' % (settings['catalog'], args), args))
      marshal['status'] = False
      return(marshal)


    ## Create new buildchain
    tmp = {}
    for link in marshal['buildchain']:
      if link == marshal['link']:
        newchain += buildchain
        tmp = link
      else:
        newchain.append(link)
    try: newchain.remove(tmp)
    except:
      if tmp in newchain:
        print '!!!!'
    marshal['buildchain'] = newchain


  ## Done
  return(marshal)


## Passthrough hook
def build(marshal):
  return(marshal)