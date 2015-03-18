#!/usr/bin/python

import os
import sys
import imp
import json
import shutil
import urllib2
import hashlib
import argparse
import cPickle as pickle
from distutils.spawn import find_executable


## Settings
settings = {
	'verbose':True,
	'varlib':'/var/lib/virt-maker',
	'imgcache':'/var/lib/virt-maker/cache'
}


## Prep dirs
dirs = [settings['varlib'],settings['imgcache']]
for dir in dirs:
	if not os.path.isdir(dir): os.makedirs(dir)

## Prints verbose statements
def verbose(text,label='INFO'):
	print('\t%s: %s'%(label,text))


## Parses DSL Variables
def dsl2opt(text,providerchar='@'):
	options = {}
	text = '\n'+text
	text = text.replace('\n%s'%(providerchar),'\n\n%s'%(providerchar))
	headertext = text.split('%s'%(providerchar))[0]
	for i in headertext.split('\n'):
		if '=' in i:
			key = i.split('=')[0]
			val = i.split('=')[1]
			options[key] = val
	return(options)


## Parses DSL Statements
def dsl2dict(text,options=False,mutatestr='<[%s]>', providerchar='@'):
	if options:
		for i in options:
			key = mutatestr%(i.split('=')[0])
			val = options[i]
			text = text.replace(key,val)
	sectionsraw = text.split('\n%s'%(providerchar))
	sections = []
	for s in sectionsraw:
		head = s.split('\n')[0]
		body = ('\n'.join(s.split('\n')[1:-1])).replace('\\%s'%(providerchar),'%s'%(providerchar))
		sections.append(
			{
				"provider":head.split(' ')[0],
				"argument":head.replace('%s '%(head.split(' ')[0]),''),
				"body":body.split('\n#%s'%(providerchar))[0],
				"hash":(hashlib.md5(s)).hexdigest(),
			}
		)
	sections.remove(sections[0]) ## Remove blank entry
	return(sections)


## Download files from url
def fetch(url,dest):
	verbose("Fetching '%s'"%(url),'Download')
	req = urllib2.urlopen(url)
	CHUNK = 16 * 1024
	count = 0
	total = int(req.headers["Content-Length"])
	lastmsg = None
	with open(dest, 'wb') as fp:
		while True:
			percent = int(float(count/total)*100)
			chunk = req.read(CHUNK)
			count += CHUNK
			if not chunk: break
			if not (count%(CHUNK*32)):
				if not lastmsg == str(percent):
					verbose('%s'%(str(percent)),'Download')
					lastmsg = str(percent)
			fp.write(chunk)
	verbose('Done','Download')

## Handle the image
class Image:
	backingimage = False
	lastimg = False
	chain = [None]
	buildchain = 'buildchain'

	def setup(self):
		if os.path.isfile(self.buildchain):
			try:
				with open(self.buildchain,'r') as f: self.chain = pickle.loads(f.read())
			except:
				os.remove(self.buildchain)

	def snapshot(self,link):
		try:
			imagefile = self.chain[-1]
		except:
			imagefile = self.backingimage
		## snapshot command here
		with open(link,'w') as f: f.write('')
		cmd = 'qemu-img create -f qcow2 -b %s %s >/dev/null 2>&1'%(imagefile,link)
		if not os.system(cmd) == 0: os.remove(link)

	def chainlink(self,link):
		self.chain.append(link)
		with open(self.buildchain,'w') as f: f.write(pickle.dumps(self.chain))

	def mount(self,link):
		try:
			imagefile = self.chain[-1]
		except:
			imagefile = self.backingimage
		mountdir = '%s_mount'%(imagefile)
		if not os.path.isdir(mountdir): os.makedirs(mountdir)
		cmd = 'guestmount -a %s -m /dev/sda1 --rw %s/ >/dev/null 2>&1'%(imagefile,mountdir)
		os.system(cmd)
		os.chdir(mountdir)

	def unmount(self,link):
		os.chdir('..')
		try:
			imagefile = self.chain[-1]
		except:
			imagefile = self.backingimage
		mountdir = '%s_mount'%(imagefile)
		## unmount command
		cmd = 'guestunmount %s/'%(mountdir)
		cmd = 'umount %s/'%(mountdir)
		os.system(cmd)
		if os.path.isdir(mountdir): shutil.rmtree(mountdir)




## Build VMK file
def build(template):

	## Main
	'/'.join(sys.argv[-1].split('/')[:-1])
	vmkdir = os.path.abspath('/'.join(sys.argv[-1].split('/')[:-1])).replace('\\','/')
	workingdir = (vmkdir+'/.virt-maker')
	image = Image()
	cwd = os.getcwd()
	chain = []
	cache = True
	steps = 0
	lasthash = None

	## Setup workspace
	if not os.path.isdir(workingdir):
		os.makedirs(workingdir)
	os.chdir(workingdir)
	image.setup()
	chain = json.loads(json.dumps(image.chain))
	chain.reverse()
	link = chain.pop()
	providerdir = '%s/providers'%(settings['varlib'])

	## Execute sections
	for section in template:
		steps += 1
		providerscript = '%s/%s.py'%(providerdir,section['provider'])

		## Handles the providers
		print('[ STEP ] %s/%s %s:\t%s'%(steps,len(dsl2dict(filetext)),section['provider'],section['argument']))
		try: link = chain.pop()
		except: link = None
		if link == section['hash'] and cache:
			pass
		else:
			cache = False
			if not os.path.isfile(providerscript):
				if not find_executable(section['provider']) == None:	## Handles arbitrary commands
					if settings['verbose']:
						cmd = '%s %s'%(section['provider'],section['argument'])
						print(cmd)
					else:
						cmd = '%s %s >/dev/null 2>&1'%(section['provider'],section['argument'])
					retval = os.system(cmd)
					if not retval == 0:
						print retval
						print('ERROR!')
						sys.exit(1)
				else:
					print 'Cannot find provider script "%s"'%(providerscript)
					exit(1)
			else:
				module = imp.load_source(section['provider'], providerscript)
				retval = module.provider(section['body'],lasthash,section['argument'],settings['verbose'],image,settings)
				if not retval == 0:
					print retval
					print('ERROR!')
					sys.exit(1)
				try: image.snapshot(section['hash'])
				except: print("\tProvider '%s' does not use snapshots."%(section['provider']))
		image.chainlink(section['hash'])
		lasthash = section['hash']

	## Finish
	os.chdir(cwd)





## Arguments
parser = argparse.ArgumentParser(description='Libvirt based VM builder')
parser.add_argument('--file','-f',      action="store",      dest="vmkfilepath",    default=False,  help='VMK build template file',           nargs='*')
parser.add_argument('--build','-b',     action="store_true", dest="build",          default=False,  help='VMK build template file')
parser.add_argument('--variables',      action="store",      dest='overridevars',   default=False,  help='Override input variables on build', nargs='*')
parser.add_argument('--show-variables', action="store_true", dest='show_variables', default=False,  help='Shows the input variables for a given *.vmk file')
parser.add_argument('--show-template',  action="store_true", dest='show_template',  default=False,  help='Shows the input template for a given *.vmk file')
#arser.add_argument('--output-format',  action="store",      dest='output_format',  default='JSON', help='Set the output format (JSON|Key).  Default JSON')
parser.add_argument('--input-format',   action="store",      dest='input_format',   default='KEY',  help='Set the input format (JSON|Key).  Default KEY')
parser.add_argument('--pretty','-p',    action="store_true", dest='pretty',         default=False,  help='Displays output in easily readable format')
parser.add_argument('--version',        action='version',    version='%(prog)s 1.0')
results = parser.parse_args()


## Execute
if results.vmkfilepath:
	for vmk in results.vmkfilepath:
		with open(vmk,'r') as f: filetext = f.read()
		options = dsl2opt(filetext)
		if results.overridevars:
			for i in results.overridevars:
				if results.input_format.lower() == 'key':
					options = dict(options.items()+dsl2opt(i).items())
				elif results.input_format.lower() == 'json':
					options = dict(options.items()+json.loads(i).items())
		template = dsl2dict(filetext,options)
		if results.show_variables:
			if results.pretty:
				print(json.dumps(options,indent=2))
			else:
				print(json.dumps(options))
		if results.show_template:
			if results.pretty:
				print(json.dumps(template,indent=2))
			else:
				print(json.dumps(template))
		if results.build: build(template)
else:
	raise('No input file specified')
	sys.exit(1)

'''
## Get vmk contents
try:
	
	build(filetext)
except:
	print('Cannot open *.vmk file')
	sys.exit(False)
'''


























