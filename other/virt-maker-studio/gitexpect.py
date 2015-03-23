#!/usr/bin/python

import os
import time
import shutil
import getpass
import pexpect

class Git:

	url = None
	name = None
	email = None
	branch = None
	username = None
	password = None


	def __init__(self):
		os.system('unset SSH_ASKPASS')


	def preflight(self):
		if self.url == None:
			return({'error':'no url set'})
		if self.branch == None:
			return({'error':'no branch set'})
		if self.username == None:
			return({'error':'no username set'})
		if self.password == None:
			return({'error':'no password set'})
		else:
			return(False)



	def clone(self,directory,overwrite=False):
		retval = False
		cwd = os.getcwd()
		if not os.path.isdir(directory): os.makedirs(directory)
		if self.preflight():
			return(self.preflight())
		if not os.listdir(directory) == []:
			if overwrite:
				shutil.rmtree(directory)
			else:
				return({'error':'%s is not empty'}%(directory))
		if not os.path.isdir(directory): os.makedirs(directory)
		os.chdir(directory)
		print '!!!!'
		os.system('pwd')
		cmd = 'git clone %s -b %s .'%(self.url,self.branch)
		print(cmd)
		exp = pexpect.spawn(cmd)
		try:
			exp.expect('Username.*', timeout=5)
			exp.sendline(self.username)
		except:
			pass
		exp.expect('Password*')
		exp.sendline(self.password)
		exp.expect(pexpect.EOF)
		if os.path.isdir('.git'): retval = True
		os.chdir(cwd)
		return(retval)



	def pull(self,directory):
		retval = False
		cwd = os.getcwd()
		if self.preflight():
			return(self.preflight())
		if not os.path.isdir(directory):
			return(retval)
		os.chdir(directory)
		cmd = 'git pull'
		print (cmd)
		exp = pexpect.spawn(cmd)
		try:
			exp.expect('Username.*', timeout=5)
			exp.sendline(self.username)
		except:
			pass
		exp.expect('Password.*')
		exp.sendline(self.password)
		exp.expect(pexpect.EOF)
		retval = True
		os.chdir(cwd)
		return(retval)



	def commit(self,directory,message=str(time.time())):
		retval = False
		cwd = os.getcwd()
		if self.preflight():
			return(self.preflight())
		if not os.path.isdir(directory):
			return(retval)
		os.chdir(directory)
		cmd = 'git commit -m "%s"'%(message)
		print (cmd)
		exp = pexpect.spawn(cmd)
		exp.expect(pexpect.EOF)
		retval = True
		os.chdir(cwd)
		return(retval)



	def add(self,directory,opt='-A'):
		retval = False
		cwd = os.getcwd()
		if self.preflight():
			return(self.preflight())
		if not os.path.isdir(directory):
			return(retval)
		os.chdir(directory)
		cmd = 'git add %s'%(opt)
		print (cmd)
		exp = pexpect.spawn(cmd)
		exp.expect(pexpect.EOF)
		retval = True
		os.chdir(cwd)
		return(retval)


	def push(self,directory):
		retval = False
		cwd = os.getcwd()
		if self.preflight():
			return(self.preflight())
		if not os.path.isdir(directory):
			return(retval)
		os.chdir(directory)
		cmd = 'git push'
		print (cmd)
		exp = pexpect.spawn(cmd)
		try:
			exp.expect('Username.*', timeout=5)
			exp.sendline(self.username)
		except:
			pass
		exp.expect('Password.*')
		exp.sendline(self.password)
		exp.expect(pexpect.EOF)
		retval = True
		os.chdir(cwd)
		return(retval)



	def remoteChanged(self,directory):
		retval = False
		cwd = os.getcwd()
		if self.preflight():
			return(self.preflight())
		if not os.path.isdir(directory): os.makedirs(directory)
		os.chdir(directory)
		cmd = 'git rev-parse @{u}'
		exp = pexpect.spawn(cmd)
		try:
			exp.expect('Username.*', timeout=5)
			exp.sendline(self.username)
		except:
			pass
		exp.expect('Password.*')
		exp.sendline(self.password)
		exp.expect('.*')
		remote = exp.before
		exp.expect(pexpect.EOF)
		cmd = 'git rev-parse @'
		exp = pexpect.spawn(cmd)
		exp.expect('.*')
		local = exp.before
		exp.expect(pexpect.EOF)
		os.chdir(cwd)
		if not local == remote:
			retval = True
		return(retval)



	def setup(self,directory):
		retval = False
		cwd = os.getcwd()
		os.chdir(directory)
		cmd = 'git config user.name "%s"'%(self.name)
		print (cmd)
		exp = pexpect.spawn(cmd)
		exp.expect(pexpect.EOF)
		cmd = 'git config user.email "%s"'%(self.email)
		print (cmd)
		exp = pexpect.spawn(cmd)
		exp.expect(pexpect.EOF)
		retval = True
		os.chdir(cwd)
		return(retval)


# git ls-remote origin