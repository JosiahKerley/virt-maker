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
	'imgcache':'/var/lib/virt-maker/store'
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
			val = '='.join(i.split('=')[1:])
			options[key] = val
	return(options)


## Parses DSL Statements
def dsl2dict(text,options=False,mutatestr='<[%s]>', providerchar='@'):
	text = text.replace('\n%s'%(providerchar),'\n\n%s'%(providerchar))
	text = providerchar.join(text.split(providerchar)[1:])
	if options:
		for i in options:
			key = mutatestr%(i.split('=')[0])
			val = options[i]
			text = text.replace(key,val)
	sectionsraw = text.split('\n%s'%(providerchar))
	print json.dumps(sectionsraw,indent=2)
	sections = []
	lasthash = 'start'
	lastprovider = None
	for s in sectionsraw:
		head = s.split('\n')[0]
		body = ('\n'.join(s.split('\n')[1:-1])).replace('\\%s'%(providerchar),'%s'%(providerchar))
		#if not s.startswith('#') and not (body.split('\n#%s'%(providerchar))[0]).startswith('#@'):
		if not s.startswith('#'):
			sections.append(
				{
					"provider":head.split(' ')[0],
					"argument":head.replace('%s '%(head.split(' ')[0]),''),
					"body":body.split('\n#%s'%(providerchar))[0],
				}
			)
			if sections[-1]['provider'] == '':
				sections[-1]['provider'] = lastprovider
			lastprovider = sections[-1]['provider']
			sections[-1]['hash'] = hashlib.md5(lasthash+json.dumps(sections[-1])).hexdigest()
			lasthash = sections[-1]['hash']
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
	buildchain = 'buildchain'

	def setup(self):
		if os.path.isfile(self.buildchain):
			try:
				with open(self.buildchain,'r') as f: self.chain = pickle.loads(f.read())
			except:
				os.remove(self.buildchain)

	def snapshot(self,last,next):
		cmd = 'qemu-img create -f qcow2 -b %s %s >/dev/null 2>&1'%(last,next)
		if not os.system(cmd) == 0: os.remove(next)

	def mount(self,link):
		imagefile = link
		mountdir = '%s_mount'%(imagefile)
		if not os.path.isdir(mountdir): os.makedirs(mountdir)
		cmd = 'guestmount -a %s -m /dev/sda1 --rw %s/ >/dev/null 2>&1'%(imagefile,mountdir)
		os.system(cmd)
		os.chdir(mountdir)

	def unmount(self,link):
		os.chdir('..')
		imagefile = link
		mountdir = '%s_mount'%(imagefile)
		## unmount command
		cmd = 'guestunmount %s/'%(mountdir)
		cmd = 'umount %s/'%(mountdir)
		os.system(cmd)
		if os.path.isdir(mountdir): shutil.rmtree(mountdir)




## Build VBP file
def build(blueprint,noop=False,nocache=True):

	## Main
	'/'.join(sys.argv[-1].split('/')[:-1])
	vbpdir = os.path.abspath('/'.join(sys.argv[-1].split('/')[:-1])).replace('\\','/')
	workingdir = (vbpdir+'/.virt-maker')
	image = Image()
	cwd = os.getcwd()
	chain = []
	steps = 0
	lasthash = None

	## Setup workspace
	if not os.path.isdir(workingdir):
		os.makedirs(workingdir)
	os.chdir(workingdir)
	providerdir = '%s/providers'%(settings['varlib'])

	## Execute sections
	for section in blueprint:
		steps += 1
		providerscript = '%s/%s.py'%(providerdir,section['provider'])

		## Handles the providers
		print('[ STEP ] %s/%s %s:\t%s'%(steps,len(dsl2dict(filetext)),section['provider'],section['argument']))
		if os.path.isfile(section['hash']) and not nocache:
			pass
		else:
			if not os.path.isfile(providerscript):
				if not find_executable(section['provider']) == None:  ## Handles arbitrary commands
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
				os.chdir(workingdir)
				module = imp.load_source(section['provider'], providerscript)
				retval = 0
				if not noop: retval = module.provider(section['body'],lasthash,section['argument'],settings['verbose'],image,settings)
				if not retval == 0:
					print retval
					print('ERROR!')
					sys.exit(1)
				try: image.snapshot(lasthash,section['hash'])
				except: pass
		if not noop: lasthash = section['hash']

	## Finish
	os.chdir(cwd)





## Arguments
parser = argparse.ArgumentParser(description='Libvirt based VM builder')
parser.add_argument('--file','-f',                    action="store",      dest="vbpfilepath",    default=False,  help='Blueprint file',                    nargs='*')
parser.add_argument('--build','-b',                   action="store_true", dest="build",          default=False,  help='Build blueprint')
parser.add_argument('--noop','-n',                    action="store_true", dest="noop",           default=False,  help='Displays provider output only')
parser.add_argument('--list-store','--list','-l',     action="store_true", dest="list",           default=False,  help='List stored images')
parser.add_argument('--list-providers','--providers', action="store_true", dest="providers",      default=False,  help='List providers')
parser.add_argument('--variables','-v',               action="store",      dest='overridevars',   default=False,  help='Override input variables on build', nargs='*')
parser.add_argument('--show-variables','-s',          action="store_true", dest='show_variables', default=False,  help='Shows the input variables for a given *.vbp file')
parser.add_argument('--dump-blueprint','-d',          action="store_true", dest='show_blueprint', default=False,  help='Shows the input blueprint for a given *.vbp file')
#arser.add_argument('--output-format','-o',           action="store",      dest='output_format',  default='JSON', help='Set the output format (JSON|Key).  Default JSON')
parser.add_argument('--input-format','-i',            action="store",      dest='input_format',   default='KEY',  help='Set the input format (JSON|Key).  Default KEY')
parser.add_argument('--pretty','-p',                  action="store_true", dest='pretty',         default=False,  help='Displays output in easily readable format')
parser.add_argument('--no-delta',                     action="store_true", dest='nodelta',        default=False,  help='Build blueprint without using deltas')
parser.add_argument('--version',                      action='version',    version='%(prog)s 1.0')
results = parser.parse_args()


## Execute
if results.vbpfilepath:
	for vbp in results.vbpfilepath:
		with open(vbp,'r') as f: filetext = f.read()
		options = dsl2opt(filetext)
		if results.overridevars:
			for i in results.overridevars:
				if results.input_format.lower() == 'key':
					options = dict(options.items()+dsl2opt(i).items())
				elif results.input_format.lower() == 'json':
					options = dict(options.items()+json.loads(i).items())
		blueprint = dsl2dict(filetext,options)
		if results.show_variables:
			if results.pretty:
				print(json.dumps(options,indent=2))
			else:
				print(json.dumps(options))
		if results.show_blueprint:
			if results.pretty:
				print(json.dumps(blueprint,indent=2))
			else:
				print(json.dumps(blueprint))
		if results.build: build(blueprint,results.noop,results.nodelta)
elif results.list:
	#files = [f for f in os.listdir(settings['imgcache']) if os.path.isfile(f)] ## Maybe...
	files = os.listdir(settings['imgcache'])
	if results.pretty:
		pass
	else:
		for i in files:
			print i
elif results.providers:
	files = os.listdir('%s/providers'%(settings['varlib']))
	if results.pretty:
		pass
	else:
		for i in files:
			print i
else:
	raise('No input file specified')
	sys.exit(1)
