#!/usr/bin/python

import os
import time
import json
import uuid
import redis
import shutil
#import bcrypt
import subprocess
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
os.system('clear')


def detached(f):
    def wrapper(*args, **kwargs):
        import os
        if os.fork(): # Parent
            os.wait()
            return
        os.setsid()
        if os.fork():
            os._exit(0)
        f(*args, **kwargs)
        os._exit(0)
    wrapper.__name__ = f.__name__
    wrapper.__dict__ = f.__dict__
    wrapper.__doc__ = f.__doc__
    return wrapper


## Returns structure of path for treeview
def pathTree(path,name,id=0,dotfiles=False):
	id += 1
	if not dotfiles and os.path.basename(path).startswith('.'):
		return(False)
	d = {'value': os.path.basename(path)}
	if path == name:
		d['type'] = "repo"
	else:
		#d['path'] = path.lstrip(name)
		d['path'] = path.replace(name,'').lstrip('/')
		d['repo'] = name.split('/')[-1]
	if os.path.isdir(path):
		if not path == name:
			d['type'] = "folder"
		d['data'] = [pathTree(os.path.join(path,x),name,id) for x in os.listdir(path)]
	else:
		d['type'] = "file"
		d['content'] = "/api/files/%s/content/%s"%(name.split('/')[-1],d['path'])
		d['variables'] = "/api/files/%s/variables/%s"%(name.split('/')[-1],d['path'])
		d['build'] = "/api/files/%s/builds/%s"%(name.split('/')[-1],d['path'])
	return(d)


## Gets list of path files/folders
def listFiles(folder):
	os.chdir(settings['workspace'])
	tree = []
	for root, folders, files in os.walk(folder):
		for filename in folders + files:
			fullpath = os.path.join(root, filename)
			path = os.path.join(root.replace(folder,''), filename).lstrip('/')
			if not os.path.isdir(fullpath): tree.append(path)
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

	def repofiles(self,name,type='tree'):
		if type == 'tree':
			if self.repopath(name):
				return(pathTree(self.repopath(name),self.repopath(name)))
			else:
				return(False)
		elif type == 'list':
			if self.repopath(name):
				return(listFiles(self.repopath(name)))
			else:
				return(False)

	def listrepos(self):
		os.chdir(settings['workspace'])
		repolist = os.listdir('repos')
		return(repolist)


## Handles file operations
class Files:
	repo = Repo()

	def read(self,reponame,filepath):
		os.chdir(settings['workspace'])
		os.chdir(self.repo.gitdir)
		os.chdir(reponame)
		if not os.path.isfile(filepath):
			return(json.dumps({"error":"file does not exist"},indent=2))
		else:
			os.chdir(settings['workspace'])
			os.chdir(self.repo.gitdir)
			os.chdir(reponame)
			with open(filepath,'r') as f: return(f.read())

	def write(self,reponame,filepath,contents):
		os.chdir(settings['workspace'])
		os.chdir(self.repo.gitdir)
		os.chdir(reponame)
		try:
			with open(filepath,'w') as f: f.write(contents)
			return(self.read(reponame, filepath))
		except:
			return(json.dump({"error":"could not write file"},indent=2))

	def delete(self,reponame,filepath):
		if not os.path.isfile(filepath):
			return({"error":"file does not exist"})
		else:
			return({"error":"file not deleted"})
			os.chdir(settings['workspace'])
			os.chdir(self.repo.gitdir)
			os.chdir(reponame)
			os.remove(filepath)
			if os.path.isfile(filepath):
				return({"error":"file not deleted"})
			else:
				return({"success":"file deleted"})

	def variables(self,reponame,filepath,raw=False):
		os.chdir(settings['workspace'])
		os.chdir(self.repo.gitdir)
		os.chdir(reponame)
		print filepath
		if not os.path.isfile(filepath):
			return({"error":"file does not exist"})
		else:
			cmd = 'virt-maker --file %s --show-variables --pretty'%(filepath.replace(' ','\\ '))
			proc = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
			output = json.loads(proc.communicate()[0])
			if not output == {}:
				if not raw:
						container = []
						for i in output:
							container.append({"view":"text","label":i,"value":output[i]})
						output = container
				return(output)
			else:
				return({"error":"cannot parse vmk variables, file may be corrupt"})

		
## Handles Builds
class Builder:
	repo = Repo()
	
	def tag(self,id=''):
		return('vms_builder-%s'%(id))
	
	def build(self,filepath,variables=False,noop=""):
		id = str(uuid.uuid4())
		filepath = ('%s/%s/%s'%(settings['workspace'],self.repo.gitdir,filepath)).replace('//','/')
		if variables:
			vars = ''
			for i in variables:
				vars += '%s=%s '%(i,variables[i])
			vars = vars.rstrip(' ')
			cmd = 'virt-maker --build --file %s --variables %s %s'%(filepath,vars,noop)
		else:
			cmd = 'virt-maker --build --file %s %s'%(filepath,noop)
		cmd = cmd.rstrip(' ')
		self.run(cmd,self.tag(id))
		filepath = filepath.replace('%s/%s'%(settings['workspace'],self.repo.gitdir),'').lstrip('/')
		repo = filepath.split('/')[0]
		filepath = filepath.lstrip('%s/'%(repo))
		content = '/api/files/%s/content/%s'%(repo,filepath)
		response = {
				"_usage":"GET to read stdout, DELETE to kill the process (if running)",
				"repo":repo,
				"filename":filepath.split('/')[-1],
				"filepath":filepath,
				"variables":variables,
				"started":int(time.time()),
				"content":content,
				"stdout":"/api/builds/console/%s"%(id),
				}
		return(response)

	@detached
	def run(self,cmd,id):
		command = cmd.split(' ')
		proc = subprocess.Popen(command, stdout=subprocess.PIPE)
		r.set(self.tag(id),'')
		while proc.poll() is None:
			output = proc.stdout.readline()
			if r.get(self.tag(id)) == False:
				print '!!!!!!!!!!!!!!!!!!!'
				proc.kill()
				newval = '<PROCESS KILLED %s>'%(str(int(time.time())))
			else:
				newval = '%s%s'%(r.get(self.tag(id)),output)
			r.set(self.tag(id),newval)
			#r.expire(self.tag(id),900)

	def console(self,id):
		return(r.get(self.tag(id)))



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
else:
	@app.route('/')
	def noUI():
		return(json.dumps({"error":"oops"}))


## Main API
@app.route('/api', methods=['GET'])
def mainpage():
	os.chdir(settings['workspace'])
	apidoc = {
				"resources":{
								"repos":"/api/repos"
							}
			}
	html = json.dumps(apidoc,indent=2)
	os.chdir(cwd)
	return(html)



##-> Handle Repo Resource <-##


## View all repos
@app.route('/api/repos', methods=['GET'])
def allRepos():
	repo = Repo()
	repos = []
	for i in repo.listrepos():
		repos.append(json.loads(singleRepo(i))[0])
	html = json.dumps(repos,indent=2)
	return(html)




## View single repo
@app.route('/api/repos/<name>', methods=['GET','POST'])
def singleRepo(name):
	os.chdir(settings['workspace'])
	git = Git()
	repo = Repo()
	if True:
		rpath = repo.repopath(name)
		if rpath and os.path.isdir(rpath):
			tree = repo.repofiles(name)
			#tree = {"type": "folder","value": "sdf", "data":[{"value":"file"}]}
			html = json.dumps([tree],indent=2)
		else:
			html = 'repo not installed'
	os.chdir(cwd)
	return(html)



## Add repo page
@app.route('/api/repos/new', methods=['GET','POST'])
def newRepo():
	os.chdir(settings['workspace'])
	defaults = {
				"name":None,
				"url":None,
				"branch":"master",
				"username":None,
				"password":None,
			}
	if request.method == 'POST':
		git = Git()
		repo = Repo()
		input = dict(request.form)
		git.url =      input['url'][0]
		git.name =     input['name'][0]
		git.branch =   input['branch'][0]
		git.username = input['username'][0]
		git.password = input['password'][0]
		git.clone('%s/%s'%('%s/repos'%(settings['workspace']),git.name),True)
		repo.save({"name":git.name,"branch":git.branch,"username":git.username,"password":git.password})
		html = singleRepo(git.name)
		del git
	else:
		html = json.dumps(defaults,indent=2)
	os.chdir(cwd)
	return(html)




##-> Handle File Resource <-##



## View all repos
@app.route('/api/files/<root>', methods=['GET'])
def repoFiles(root):
	repo = Repo()
	files = repo.repofiles(root,'list')
	html = json.dumps(files,indent=2)
	return(html)

## Read/write file contents
@app.route('/api/files/<root>/content/<path:path>', methods=['GET','POST','DELETE'])
def fileContent(root,path):
	repo = Repo()
	files = Files()
	if request.method == 'POST':
		if dict(request.form) == {}:
			data = request.data
		else:
			data = ''
			form = dict(request.form)
			for i in form:
				data += form[i][0]
		html = files.write(root,path,data)
	elif request.method == 'GET':
		html = files.read(root,path)
	elif request.method == 'DELETE':
		html = json.dumps(files.delete(root,path))
	else:
		html = json.dumps({"error":{"supported verbs":['GET','POST','DELETE']}},indent=2)
	return(html)




## Load file input variables
@app.route('/api/files/<root>/variables/<path:path>', methods=['GET'])
def fileInput(root,path):
	repo = Repo()
	files = Files()
	html = json.dumps(files.variables(root,path),indent=2)
	return(html)





## Load file input variables
@app.route('/api/builds', methods=['GET'])
def listBuilds():
	tag = 'vms_builds'
	repo = Repo()
	files = Files()
	builder = Builder()
	html = json.dumps(json.loads(r.get(tag)),indent=2)
	return(html)




## Load file input variables
@app.route('/api/builds/<path:path>', methods=['POST'])
def buildTemplate(path):
	tag = 'vms_builds'
	repo = Repo()
	files = Files()
	builder = Builder()
	form = dict(request.form)
	flatform = {}
	for i in form:
		flatform[i] = form[i][0]
	retval = builder.build(path,flatform)
	if r.get(tag) == None:
		newval = [retval]
	else:
		currentval = json.loads(r.get(tag))
		newval = [retval]
		newval += currentval
	r.set(tag,json.dumps(newval))
	html = json.dumps(retval,indent=2)
	return(html)




@app.route('/api/builds/console/<id>', methods=['GET','DELETE'])
def buildConsole(id):
	builder = Builder()
	if request.method == 'DELETE':
		r.set(builder.tag(id),False,30)
	return(builder.console(builder.tag(id)))













if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080,debug=True)
	#app.run(host='0.0.0.0',port=80)
