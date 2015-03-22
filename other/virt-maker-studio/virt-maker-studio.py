#!/usr/bin/python

import os
import json
import redis
import time
import shutil
#import bcrypt
from gitexpect import Git
from urlparse import urlparse
from flask import Flask, request, render_template, render_template_string, redirect

r = redis.Redis()

## Settings
settings = {
	'fingerprint':'virt-maker-studio:',
	'workspace':'/var/lib/virt-maker/studio',
}


## Startup
offloadUI = True
cwd = os.getcwd()
htmldir = '%s/%s'%(os.getcwd(),'html')
if not os.path.isdir(settings['workspace']): os.makedirs(settings['workspace'])
os.system('ls')




## Returns structure of path for treeview
def pathTree(path,id=0):
	os.chdir(settings['workspace'])
	id += 1
        d = {'value': os.path.basename(path)}
        d['path'] = path
	d['id'] = id
        if os.path.isdir(path):
                d['type'] = "folder"
                d['data'] = [pathTree(os.path.join(path,x),id) for x in os.listdir(path)]
        else:
                d['type'] = "file"
	os.chdir(cwd)
        return(d)


## Gets list of path files/folders
def listfiles(folder):
	os.chdir(settings['workspace'])
	tree = []
	for root, folders, files in os.walk(folder):
		for filename in folders + files:
			#yield os.path.join(root, filename)
			tree.append(os.path.join(root, filename))
	os.chdir(cwd)
	return(tree)






## handles repo indexing
class Repo:
	creddir = 'repo-credentials'
	gitdir = 'repos'
	def __init__(self):
		os.chdir(settings['workspace'])
		if not os.path.isdir(self.creddir): os.makedirs(self.creddir)
		if not os.path.isdir('%s/%s'%(settings['workspace'],self.gitdir)): os.makedirs('%s/%s'%(settings['workspace'],self.gitdir))
		os.chdir(cwd)


	def save(self,repo):
		os.chdir(settings['workspace'])
		with open('%s/%s.repo'%(self.creddir,repo['name']),'w') as f: f.write(json.dumps(repo,indent=2))
		os.chdir(cwd)


	def repopath(self,name):
		os.chdir(settings['workspace'])
		full = '%s/%s/%s'%(settings['workspace'],self.gitdir,name)
		if not os.path.isdir(full): return(False)
		os.chdir(cwd)
		return(full)

	def repofiles(self,name):
		os.chdir(settings['workspace'])
		os.chdir(cwd)
		if self.repopath(name):
			return(pathTree(self.repopath(name)))
		else:
			return(False)





##-> MAIN APP <-##
app = Flask(__name__, static_url_path=htmldir)
#app = Flask(__name__)



## Serve the main UI
if not offloadUI:
	uiroute = '/ui'
	codebaseroute = '/codebase'
	@app.route('/')
	def redirectToMain():
		return(redirect(uiroute, code=302))
	@app.route(uiroute)
	def serveUI():
		html = r.get('mainui')
		if html == None:
			with open('html/index.html', 'r') as f: html = f.read()
			r.set('mainui',html)
			r.expire('mainui',10)
		return(html)
	@app.route('/<path:path>')
	def serveCodebase(path=False):
		reqfile = 'codebase/%s'%(path)
		print reqfile
		return(app.send_static_file(path))



## Main API
@app.route('/api', methods=['GET'])
def mainpage():
	os.chdir(settings['workspace'])
	id = '%s*'%(settings['fingerprint'])
	items = r.keys(id)
	items = list(filter(None, items))
	new = []
	for i in items:
		items = list(set(json.loads(r.get(i))))
		if len(items) > 1:
			new.append(i.replace(settings['fingerprint'],''))
		else:
			r.delete(i)
	items = new
	os.chdir(cwd)
	return(html)



## Add repo page
@app.route('/api/repos/new', methods=['GET','POST'])
def newpage():
	os.chdir(settings['workspace'])
	id = '%srepos*'%(settings['fingerprint'])
	css = render_template_string(defaultcss,fontstyle=fonts[fontselected]['fontstyle'])
	if request.method == 'POST':
		git = Git()
		repo = Repo()
		input = dict(request.form)
		#print request.form
		#print json.dumps(input,indent=2)
		git.url =      input['url'][0]
		git.name =     input['name'][0]
		git.branch =   input['branch'][0]
		git.username = input['username'][0]
		git.password = input['password'][0]
		git.clone('%s/%s'%(repo.gitdir,git.name),True)
		repo.save({"name":git.name,"branch":git.branch,"username":git.username,"password":git.password})
		del git
		html = 'done'
	else:
		items = r.keys(id)
		items = list(filter(None, items))
		new = []
		for i in items:
			items = list(set(json.loads(r.get(i))))
			if len(items) > 1:
				new.append(i.replace(settings['fingerprint'],''))
			else:
				r.delete(i)
		items = new
	os.chdir(cwd)
	return(html)



## View single repo
@app.route('/api/repos/<name>', methods=['GET','POST'])
def singlerepo(name):
	os.chdir(settings['workspace'])
	git = Git()
	repo = Repo()
	id = '%srepos*'%(settings['fingerprint'])
	css = render_template_string(defaultcss,fontstyle=fonts[fontselected]['fontstyle'])
	if True:
		rpath = repo.repopath(name)
		if rpath and os.path.isdir(rpath):
			tree = repo.repofiles(name)
			tree = {"type": "folder","value": "sdf", "data":[{"value":"file"}]}
			html = json.dumps([tree],indent=2)
		else:
			html = 'repo not installed'
	os.chdir(cwd)
	return(html)





#@app.route('/repos/new', methods=['GET','POST'])

















if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080,debug=True)
	#app.run(host='0.0.0.0',port=80)
