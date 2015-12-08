#!/usr/bin/python

## Import libraries
import os
import sys
import imp
import json
import time
import yaml
import shutil
import jinja2
import urllib2
import inspect
import hashlib
import argparse
import filelock
import cPickle as pickle
from distutils.spawn import find_executable


## Settings
settings = {
  'verbose':True,
  'varlib':'/var/lib/virt-maker',
  'catalog':'/var/lib/virt-maker/catalog',
  'store':'/var/lib/virt-maker/store',
  'cache':'/var/lib/virt-maker/cache',
  'providerdir':'/var/lib/virt-maker/providers',
  'trycmd':True,
  'safedelta':True
}


## Marshal object
marshal = {
      "link":{},
      "image":None,
      "status":True,
      "messages":[],
      "settings":settings,
      "buildchain":[],
      "commands":[],  ## For futures use, all commands are appended to this allowing a shell script to be generated
}


## Globals
locks = {}



## File locking
class Flock:

  ## Imports
  import os
  import time
  import uuid
  import hashlib
  import threading
  from cPickle import loads as load_
  from cPickle import dumps as dump_


  ## Globals
  locks       = {}
  threads     = {}
  evaluations = 5
  eval_delay  = 1
  lock_poll   = 0.1
  lock_life   = None


  ## Methods

  def __init__(self,lockroot='/tmp'):
    """ Constructor """
    self.lockroot = lockroot
    self.id = str(self.uuid.uuid4())


  def load(self,filepath):
    """ Load method """
    if self.os.path.isfile(filepath):
      with open(filepath,'r') as f:
        return(self.load_(f.read()))
    return(False)


  def dump(self,data,filepath):
    """ Load method """
    with open(filepath,'w') as f:
      return(f.write(self.dump_(data)))


  def get_lock_file(self,filepath):
    """ Gets a lockfile path for a given file path """
    filepath = self.os.path.abspath(filepath)
    filehash = str(self.hashlib.md5(filepath).hexdigest())
    lockfile_path = self.os.path.join(self.lockroot,'.'+filehash+'.lock')
    return(lockfile_path)


  def is_locked(self,filepath):
    """ Returns whether or not the given file is locked """
    lockfile = self.get_lock_file(filepath)
    self.time.sleep(self.eval_delay)
    if self.os.path.isfile(lockfile):
      lock = self.load(lockfile)
      time = lock['timestamp']
      locked = False
      for i in range(1,self.evaluations):
        self.time.sleep(self.eval_delay)
        lock = self.load(lockfile)
        try:
          if not time == lock['timestamp']:
            locked = True
        except:
          locked = True
      return(locked)
    else:
      return(False)


  def heartbeat(self,filepath):
    """ Maintains a lock """
    start = self.time.time()
    while self.locks[filepath]:
      lock = {}
      lock['id'] = self.id
      lock['filepath'] = filepath
      lock['timestamp'] = self.time.time()
      self.dump(lock,self.get_lock_file(filepath))
      if not self.lock_life == None:
        if (self.lock_life - start) <= 0:
          self.locks['filepath'] = False
      self.time.sleep(self.lock_poll)
      if self.load(self.get_lock_file(filepath)) == False or not self.os.path.exists(self.get_lock_file(filepath)):
        break


  def lock(self,filepath):
    """ Lock a given file """
    filepath = self.os.path.abspath(filepath)
    if not self.is_locked(filepath):
      #get_lock_file(filepath)
      self.locks[filepath] = True
      self.threads[filepath] = self.threading.Thread(target=self.heartbeat,args=(filepath,))
      (self.threads[filepath]).start()
      return(True)
    else:
      return(False)
    
  def unlock(self,filepath):
    filepath = self.os.path.abspath(filepath)
    self.locks[filepath] = False
    if self.os.path.isfile(self.get_lock_file(filepath)):
      self.os.remove(self.get_lock_file(filepath))

  def unlock_all(self):
    for i in self.locks:
      self.unlock(i)


## Start locks
flock = Flock()



## Prep dirs
dirs = [settings['varlib'], settings['store'], settings['catalog'], settings['cache']]
for dir in dirs:
  if not os.path.isdir(dir): os.makedirs(dir)

## Prints verbose statements
def verbose(text, label='INFO'):
  print('\t%s: %s' % (label, text))


## Exit cleanup
def cleanup():
  flock.unlock_all()

## Parses DSL Variables
def dsl2opt(text, providerchar='@'):
  options = {}
  text = '\n' + text
  text = text.replace('\n%s' % (providerchar), '\n\n%s' % (providerchar))
  headertext = text.split('\n%s' % (providerchar))[0]
  for i in headertext.split('\n'):
    if '=' in i:
      key = i.split('=')[0]
      val = '='.join(i.split('=')[1:])
      options[key] = val
  return(options)


## Parses DSL Statements
def dsl2dict(text, options=False, mutatestr='<[%s]>', providerchar='@'):
  text = '\n\n' + text
  text = text.replace('\n%s' % (providerchar), '\n\n%s' % (providerchar))
  text = providerchar.join(text.split('\n' + providerchar)[1:])
  if options:
    for i in options:
      key = mutatestr % (i.split('=')[0])
      val = options[i]
      text = text.replace(key, val)
  sectionsraw = text.split('\n%s' % (providerchar))
  sections = []
  lasthash = 'start'
  lastprovider = None
  for s in sectionsraw:
    head = s.split('\n')[0]
    body = ('\n'.join(s.split('\n')[1:-1])).replace('\\%s' % (providerchar), '%s' % (providerchar))
    if not s.startswith('#'):
      sections.append(
        {
          "provider":head.split(' ')[0],
          "argument":head.replace('%s ' % (head.split(' ')[0]), ''),
          "body":body.split('\n#%s' % (providerchar))[0],
        }
      )
      if sections[-1]['provider'] == '':
        sections[-1]['provider'] = lastprovider
      lastprovider = sections[-1]['provider']
      sections[-1]['hash'] = hashlib.md5(lasthash + json.dumps(sections[-1])).hexdigest()
      lasthash = sections[-1]['hash']
  return(sections)


## Parses YAML Statements
def yml2dict(text):
  data_raw = yaml.load(text)
  env = jinja2.Environment()
  namespace = {}
  parameters = {}
  definitionOrig = yaml.load(text)
  lastEval = 'start'
  definition = definitionOrig
  while not json.dumps(definition) == lastEval:
    lastEval = json.dumps(definition)
    definition = load(env.from_string(dump(definitionOrig)).render(definition))
  count_steps = len(definition['steps'])
  steps_messy = definition['steps']

  steps = []
  for step in steps_messy:
    corrected = {'provider':step.keys()[0]}
    if not type(step.keys()[0]) == type({}):
      corrected['argument'] = step[step.keys()[0]]
      corrected['body'] = ''
    else:
      corrected['argument'] = step['args']
      corrected['body'] = step['body']
    steps.append(corrected)

  c = 0
  lastprovider = ''
  sections = steps
  while c <= len(sections):
    if sections[-1]['provider'] == '':
      sections[-1]['provider'] = lastprovider
    lastprovider = sections[-1]['provider']
    sections[-1]['hash'] = hashlib.md5(lasthash + json.dumps(sections[-1])).hexdigest()
    lasthash = sections[-1]['hash']
    c += 1

  return(sections)


## Adds previous hashes to links
def filterPrevHash(buildchain):
  new = []
  last = None
  for link in buildchain:
    link['last'] = last
    last = link['hash']
    new.append(link)
  buildchain = new
  return(buildchain)


## Searches a provider module for a given hook
def hasHook(filepath, hookname):
  module = imp.load_source(hookname, filepath)
  members = inspect.getmembers(module)
  for i in members:
    if i[0] == hookname:
      return(True)
  return(False)


## Download files from url
def fetch(url, dest):
  verbose("Fetching '%s'" % (url), 'Download')
  req = urllib2.urlopen(url)
  CHUNK = 16 * 1024
  count = 0
  total = int(req.headers["Content-Length"])
  lastmsg = None
  with open(dest, 'wb') as fp:
    while True:
      percent = int(float(count / total) * 100)
      chunk = req.read(CHUNK)
      count += CHUNK
      if not chunk: break
      if not (count % (CHUNK * 32)):
        if not lastmsg == str(percent):
          verbose('%s' % (str(percent)), 'Download')
          lastmsg = str(percent)
      fp.write(chunk)
  verbose('Done', 'Download')


## Handle the image
class Image:

  def snapshot(self, last, next):
    os.chdir(settings['cache'])
    cmd = 'qemu-img create -f qcow2 -b %s %s >/dev/null 2>&1' % (last, next)
    if settings['verbose'] > 1:
      cmd = 'qemu-img create -f qcow2 -b %s %s' % (last, next)
      print(cmd)
    if not os.system(cmd) == 0:
      os.remove(next)

  def mount(self, link):
    imagefile = link
    while flock.is_locked(imagefile):
      print('[ Lock ] File {} locked, waiting'.format(imagefile))
      time.sleep(10)
    if not flock.lock(imagefile):
      print('[ Lock ] Cannot acquire {}'.format(imagefile))
      sys.exit(1)
    else:
      print('[ Lock ] Acquired {}'.format(imagefile))
    mountdir = '%s_mount' % (imagefile)
    if not os.path.isdir(mountdir):
      try: os.makedirs(mountdir)
      except: pass
    cmd = 'guestmount -a %s --rw %s/ -i >/dev/null 2>&1' % (imagefile, mountdir)
    if settings['verbose'] > 1:
      cmd = 'guestmount -a %s --rw %s/ -i' % (imagefile, mountdir)
      print(cmd)
    try: os.system(cmd)
    except:
      os.chdir(mountdir)
      self.unmount(link)
      os.system(cmd)
    os.system('ls')
    os.system('pwd')
    os.chdir(mountdir)
    flock.unlock(imagefile)


  def unmount(self, link):
    os.chdir('..')
    imagefile = link
    mountdir = '%s_mount' % (imagefile)
    cmd = 'guestunmount %s/ >/dev/null 2>&1' % (mountdir)
    if settings['verbose'] > 1:
      cmd = 'guestunmount %s/' % (mountdir)
      print(cmd)
    os.system(cmd)
    if os.path.isdir(mountdir): shutil.rmtree(mountdir)


## Pre processor
def pre(marshal):
  orig = marshal
  chain = marshal['buildchain']
  for link in chain:
    marshal['link'] = link
    providerfile = '%s/%s.py' % (settings['providerdir'], link['provider'])
    if os.path.isfile(providerfile):
      if hasHook(providerfile, 'pre'):
        module = imp.load_source('pre', providerfile)
        marshal = module.pre(marshal)
        del module
      if not marshal['status']:
        print('Error!')
        sys.exit(1)
  return(marshal)


## YAML based Blueprints


## Build VBP file
def build(marshal):


  ## Setup main
  '/'.join(sys.argv[-1].split('/')[:-1])
  vbpdir = os.path.abspath('/'.join(sys.argv[-1].split('/')[:-1])).replace('\\', '/')
  #workingdir = (vbpdir + '/.virt-maker')
  workingdir = settings['cache']
  image = Image()
  cwd = os.getcwd()
  chain = []
  steps = 0
  delta = True


  ## Prepare the marshal object
  marshal['image'] = image

  ## Setup workspace
  if not os.path.isdir(workingdir):
    os.makedirs(workingdir)
  os.chdir(workingdir)
  providerdir = '%s/providers' % (settings['varlib'])

  ## Execute sections
  for link in filterPrevHash(marshal['buildchain']):
    skip = False
    os.chdir(workingdir)
    marshal['link'] = link
    steps += 1
    providerscript = '%s/%s.py' % (providerdir, link['provider'])

    ## Handles the providers
    print('[ STEP ] %s/%s %s:\t%s' % (steps, len(marshal['buildchain']), link['provider'], link['argument']))

    if os.path.isfile(link['hash']) and not settings['nodelta']:
      skip = True
    if skip and delta:
      pass
    else:
      while flock.is_locked(link['hash']) == True:
        print('[ LOCK ] File {} locked, waiting'.format(link['hash']))
        time.sleep(10)
      if not flock.lock(link['hash']):
        print('[ LOCK ] Cannot acquire {}'.format(link['hash']))
        cleanup()
        sys.exit(1)
      if settings['safedelta']:delta = False
      if not os.path.isfile(providerscript):
        if not find_executable(link['provider']) == None and settings['trycmd']:  ## Handles arbitrary commands
          if settings['verbose']:
            cmd = '%s %s' % (link['provider'], link['argument'])
            print(cmd)
          else:
            cmd = '%s %s >/dev/null 2>&1' % (link['provider'], link['argument'])
          retval = os.system(cmd)
          if not retval == 0:
            print retval
            print('ERROR!')
            sys.exit(1)
        else:
          print 'Cannot find provider script "%s"' % (providerscript)
          exit(1)
      else:
        os.chdir(workingdir)
        if hasHook(providerscript, 'build'):
          module = imp.load_source(link['provider'], providerscript)
          retval = 0
          if not settings['noop']:
            marshal = module.build(marshal)
            del module
          if not marshal['status']:
            print('ERROR!')
            cleanup()
            sys.exit(1)
      try: image.snapshot(link['last'], link['hash'])
      except: pass
      flock.unlock(link['hash'])
  print('[FINISH] Execution time: %s'%(str(time.time() - starttime)))

  ## Finish,
  os.chdir(cwd)
  cleanup()
  return(marshal)


## Post processor - currently just using the preproc until changes are needed.
def post(marshal):
  for link in marshal['buildchain']:
    marshal['link'] = link
    try:
      module = imp.load_source(link['provider'], '%s/providers/%s.py' % (settings['varlib'], link['provider']))
      marshal = module.post(marshal)
    except:
      pass
    if not marshal['status']:
      print('Error!')
      sys.exit(1)
  return(marshal)



## Fully resolves input
def resolveYAMLJinja(text):
  start = text
  test = ''
  data = {}
  c = 0
  while not start == test:
    c += 1
    data = yaml.load(start)
    test = jinja2.Environment().from_string(start).render(data)
    if c >= 255: break
  return(test)



## Jinja handler
def handle_jinja(text):
  """ Handles parsing the Jinja DSL """
  template = '\n@'+text.split('\n@',1)[-1] ## Breaks out the YAML from the DSL
  text = text.replace(template,'')         ##
  text = resolveYAMLJinja(text)  ## Jumps the YAML's internal jinja-ness
  if '-s' in sys.argv: print text # Need to integrate into argparse
  buff = ''                                     ## Stream loads the YAML
  for line in text.split('\n'):                 ##
    if not line.startswith('#'):                ##
      try:                                      ##
        buff += line+'\n'                       ##
        yaml.load(buff)                         ##
      except:                                   ##
        buff = '\n'.join(buff.split('\n')[:-2]) ##
        break                                   ##
  dsl = jinja2.Environment().from_string(template).render(yaml.load(buff)) ## Render the DSL
  return(dsl)



## Arguments
parser = argparse.ArgumentParser(description='Libvirt based VM builder')
parser.add_argument('--file', '-f', action="store", dest="vbpfilepath", default=False, help='DSL based blueprint file', nargs='*')
parser.add_argument('--yaml', '-y', action="store", dest="ymlfilepath", default=False, help='YAML based blueprint file', nargs='*')
parser.add_argument('--jinja', '-j', action="store_true", dest="jinja", default=False, help='Jinja enhanced blueprint parser')
parser.add_argument('--build', '-b', action="store_true", dest="build", default=False, help='Build blueprint')
parser.add_argument('--catalog', '-c', action="store_true", dest="catalog", default=False, help='Catalog blueprint')
parser.add_argument('--noop', '-n', action="store_true", dest="noop", default=False, help='Displays provider output only')
parser.add_argument('--list-store', '--list', '-l', action="store_true", dest="list", default=False, help='List stored images')
parser.add_argument('--list-providers', '--providers', action="store_true", dest="providers", default=False, help='List providers')
parser.add_argument('--variables', '-v', action="store", dest='overridevars', default=False, help='Override input variables on build', nargs='*')
parser.add_argument('--show-variables', '-s', action="store_true", dest='show_variables', default=False, help='Shows the input variables for a given *.vbp file')
parser.add_argument('--dump-blueprint', '-d', action="store_true", dest='show_blueprint', default=False, help='Shows the input blueprint for a given *.vbp file')
# arser.add_argument('--output-format','-o',           action="store",      dest='output_format',  default='JSON', help='Set the output format (JSON|Key).  Default JSON')
parser.add_argument('--input-format', '-i', action="store", dest='input_format', default='KEY', help='Set the input format (JSON|Key).  Default KEY')
parser.add_argument('--pretty', '-p', action="store_true", dest='pretty', default=False, help='Displays output in easily readable format')
parser.add_argument('--no-cache', action="store_true", dest='nodelta', default=False, help='Build blueprint without using cache')
parser.add_argument('--flush-cache', action="store_true", dest='flushcache', default=False, help='Remove all snapshots from cache')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
results = parser.parse_args()


## Execute
starttime = time.time()













if results.vbpfilepath:
  settings['noop'] = results.noop
  settings['nodelta'] = results.nodelta
  marshal['settings'] = settings
  for vbp in results.vbpfilepath:
    marshal['blueprint'] = {}
    marshal['blueprint']['path'] = os.path.abspath(vbp)
    with open(vbp, 'r') as f: filetext = f.read()
    if results.jinja:
      filetext = handle_jinja(filetext)
    options = dsl2opt(filetext)
    if results.overridevars:
      for i in results.overridevars:
        if results.input_format.lower() == 'key':
          options = dict(options.items() + dsl2opt(i).items())
        elif results.input_format.lower() == 'json':
          options = dict(options.items() + json.loads(i).items())
    buildchain = dsl2dict(filetext, options)
    marshal['buildchain'] = filterPrevHash(buildchain)
    marshal = pre(marshal)
    if results.catalog:
      dest = vbp.split('/')[-1]
      dest = '%s/%s'%(settings['catalog'] ,dest)
      shutil.copy2(vbp,dest)
    if results.show_variables:
      if results.pretty:
        print(json.dumps(options, indent=2))
      else:
        print(json.dumps(options))
    if results.show_blueprint:
      if results.pretty:
        print(json.dumps(buildchain, indent=2))
      else:
        print(json.dumps(buildchain))
    if results.build:
      marshal = build(marshal)
    marshal = post(marshal)



elif results.ymlfilepath:
  settings['noop'] = results.noop
  settings['nodelta'] = results.nodelta
  marshal['settings'] = settings
  for yml in results.ymlfilepath:
    marshal['blueprint'] = {}
    marshal['blueprint']['path'] = os.path.abspath(vbp)
    with open(yml, 'r') as f: filetext = f.read()
    buildchain = yml2dict(filetext)
    marshal['buildchain'] = filterPrevHash(buildchain)
    marshal = pre(marshal)
    if results.catalog:
      dest = vbp.split('/')[-1]
      dest = '%s/%s'%(settings['catalog'] ,dest)
      shutil.copy2(vbp,dest)
    if results.show_variables:
      if results.pretty:
       	print(json.dumps(options, indent=2))
      else:
        print(json.dumps(options))
    if results.show_blueprint:
      if results.pretty:
        print(json.dumps(buildchain, indent=2))
      else:
        print(json.dumps(buildchain))
    if results.build:
      marshal = build(marshal)
    marshal = post(marshal)



elif results.list:
  # files = [f for f in os.listdir(settings['store']) if os.path.isfile(f)] ## Maybe...
  files = os.listdir(settings['store'])
  if results.pretty:
    pass
  else:
    for i in files:
      print i
elif results.providers:
  files = os.listdir('%s/providers' % (settings['varlib']))
  if results.pretty:
    pass
  else:
    for i in files:
      print i
elif results.flushcache:
  cmd = 'find "%s/" -type f -exec rm -rf {} \; ;'%(settings['cache'])
  os.system(cmd)
else:
  raise('No input file specified')
  cleanup()
  sys.exit(1)
cleanup()
