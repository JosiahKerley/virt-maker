#!/usr/bin/python

import os
import sys
import imp
import json
import shutil
import urllib2
import hashlib
import cPickle as pickle


## Settings
v = True
varlib = '/var/lib/virt-maker'
cachedir = '%s/cache'%(varlib)


## Prep dirs
dirs = [varlib,cachedir]
for dir in dirs:
	if not os.path.isdir(dir): os.makedirs(dir)

## Prints verbose statements
def verbose(text,label='INFO'):
	print('\t%s: %s'%(label,text))

## Parses DSL
def dsl2dict(text):
	providerchar = '@'
	text = '\n'+text
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
	
	def start(self):
		#self.chain = [self.backingimage]
		self.chain = []
		self.buildchain = '%s/%s'%(os.getcwd(),self.buildchain)

	def snapshot(self,link):
		try:
			imagefile = self.chain[-1]
		except:
			imagefile = self.backingimage
		## snapshot command here
		with open(link,'w') as f: f.write('')
		cmd = 'qemu-img create -f qcow2 -b %s %s'%(imagefile,link)
		#print cmd
		os.system(cmd)

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
		cmd = 'guestmount -a %s -m /dev/sda1 --rw %s/'%(imagefile,mountdir)
		print cmd
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
		#print cmd
		os.system(cmd)
		if os.path.isdir(mountdir): shutil.rmtree(mountdir)



## Get vmk contents
try:
	with open(sys.argv[-1],'r') as f: filetext = f.read()
except:
	print('Cannot open *.vmk file')
	sys.exit(False)


## Main
image = Image()
image.buildchain = '.%s.%s'%(sys.argv[-1],image.buildchain)
cwd = os.getcwd()
chain = []
cache = True
ready = False
steps = 0
lasthash = None
for section in dsl2dict(filetext):
	steps += 1
	#print json.dumps(section,indent=2)
	providerdir = '%s/providers'%(varlib)
	providerscript = '%s/%s.py'%(providerdir,section['provider'])


	## Handles the providers
	print '[STEP] %s/%s %s - %s'%(steps,len(dsl2dict(filetext)),section['provider'],section['hash'])
	if section['provider'] == "image":
		if section['argument'].startswith("http://") or section['argument'].startswith("https://"):
			filename = section['argument'].split('/')[-1]
			dest = '%s/%s'%(cachedir,filename)
			tmp = dest+'.downloading'
			if not os.path.isfile(dest):
				fetch(section['argument'],tmp)
				os.rename(tmp,dest)
			else:
				verbose('Using cached','Download')
			section['argument'] = dest
		cachfile = '%s/%s'%(cachedir,section['argument'])
		if os.path.isfile(cachfile):
			section['argument'] = cachfile
		imagepath = os.path.abspath(section['argument']).replace('\\','/')
		#print imagepath
		image.backingimage = imagepath.split('/')[-1]
		sectiondir = '/'.join(imagepath.split('/')[:-1])
		os.chdir(sectiondir)
		image.setup()
		chain = image.chain
		chain.reverse()
		image.start()
		ready = True
		image.snapshot(section['hash'])
		link = chain.pop()
	elif ready:
		try: link = chain.pop()
		except: link = None
		if link == section['hash'] and cache and os.path.isfile(section['hash']):
			#print('Using cached %s'%(section['hash']))
			pass
		else:
			cache = False
			if not os.path.isfile(providerscript):
				print '\nCannot find "%s"'%(providerscript)
			else:
				#print '\nLoading "%s"'%(providerscript)
				module = imp.load_source(section['provider'], providerscript)
				retval = module.provider(section['body'],lasthash,section['argument'],v,image)
				if not retval: sys.exit(1)
				image.snapshot(section['hash'])
	image.chainlink(section['hash'])
	lasthash = section['hash']


## Finish
os.chdir(cwd)















