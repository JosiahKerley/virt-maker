import os
import json
import redis
import time
import shutil
#import bcrypt
from gitexpect import Git
from urlparse import urlparse
from flask import Flask, request, render_template, render_template_string

r = redis.Redis()

## Settings
settings = {
	'fingerprint':'virt-maker-studio:',
	'workspace':'/var/lib/virt-maker/studio',
}


## Startup
if not os.path.isdir(settings['workspace']): os.makedirs(settings['workspace'])
os.chdir(settings['workspace'])
os.system('ls')




## Returns structure of path for treeview
def pathTree(path,id=0):
	id += 1
        d = {'value': os.path.basename(path)}
        d['path'] = path
	d['id'] = id
        if os.path.isdir(path):
                d['type'] = "folder"
                d['data'] = [pathTree(os.path.join(path,x),id) for x in os.listdir(path)]
        else:
                d['type'] = "file"
        return(d)


## Gets list of path files/folders
def listfiles(folder):
	tree = []
	for root, folders, files in os.walk(folder):
		for filename in folders + files:
			#yield os.path.join(root, filename)
			tree.append(os.path.join(root, filename))
	return(tree)






## handles repo indexing
class Repo:
	creddir = 'repo-credentials'
	gitdir = 'repos'
	def __init__(self):
		if not os.path.isdir(self.creddir): os.makedirs(self.creddir)
		if not os.path.isdir('%s/%s'%(settings['workspace'],self.gitdir)): os.makedirs('%s/%s'%(settings['workspace'],self.gitdir))

	def save(self,repo):
		with open('%s/%s.repo'%(self.creddir,repo['name']),'w') as f: f.write(json.dumps(repo,indent=2))

	def repopath(self,name):
		full = '%s/%s/%s'%(settings['workspace'],self.gitdir,name)
		if not os.path.isdir(full): return(False)
		return(full)

	def repofiles(self,name):
		if self.repopath(name):
			return(pathTree(self.repopath(name)))
		else:
			return(False)





##-> MAIN APP <-##
app = Flask(__name__, static_url_path='html')



## Serve static files
@app.route('/')
def index():
    return(send_from_directory('html', 'index.html'))



## Serve static files
@app.route('/<path>')
def staticFiles(path):
    return(send_from_directory('html', path))



## Main page
@app.route('/api', methods=['GET'])
def mainpage():
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
	return(html)



## Add repo page
@app.route('/api/repos/new', methods=['GET','POST'])
def newpage():
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
	return(html)



## View single repo
@app.route('/api/repos/<name>', methods=['GET','POST'])
def singlerepo(name):
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
	return(html)





#@app.route('/repos/new', methods=['GET','POST'])

















if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
