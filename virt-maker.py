#!/usr/bin/python

import os
import imp
import json
import shutil
import hashlib
import cPickle as pickle



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


## For test
with open('test.vmk','r') as f: filetext = f.read()


## Main
image = Image()
cwd = os.getcwd()
chain = []
cache = True
ready = False
steps = 0
for section in dsl2dict(filetext):
	steps += 1
	#print json.dumps(section,indent=2)
	providerdir = '../providers'
	providerscript = '%s/%s.py'%(providerdir,section['provider'])


	## Handles the providers
	print '[STEP] %s/%s %s - %s'%(steps,len(dsl2dict(filetext)),section['provider'],section['hash'])
	if section['provider'] == "image":
		imagepath = os.path.abspath(section['argument']).replace('\\','/')
		#print imagepath
		image.backingimage = imagepath.split('/')[-1]
		os.chdir('/'.join(imagepath.split('/')[:-1]))
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
				image.mount(section['hash'])
				retval = module.provider(section['body'],section['hash'],section['argument'])
				image.unmount(section['hash'])
				image.snapshot(section['hash'])
	image.chainlink(section['hash'])


## Finish
os.chdir(cwd)















