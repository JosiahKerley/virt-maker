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

## HTML and CSS

fonts = [
	{"fontstyle":"font-family: 'Amatic SC', cursive;","link":"<link href='http://fonts.googleapis.com/css?family=Amatic+SC' rel='stylesheet' type='text/css'>"},
	{"fontstyle":"font-family: 'Indie Flower', cursive;","link":"<link href='http://fonts.googleapis.com/css?family=Indie+Flower' rel='stylesheet' type='text/css'>"},
]
fontselected = 1

defaultcss = '''
			html * {
				{{ fontstyle }}
				font-size: 25px;
				text-decoration: none;
			}
			#list {
				width: 60%;
				margin-left: auto;
				margin-right: auto;
				margin-top: 5%;
			}
			#item_ {
				border:3px solid #999;
				padding:1em;
				-moz-border-radius:8px;
				-webkit-border-radius:8px;
				-opera-border-radius:8px;
				-khtml-border-radius:8px;
				border-radius:8px;
				margin-top: 20px;
				width: 100%;
			}
			#item {
				width: 100%;
				padding-bottom: 50px;
			}
			input[type=checkbox] {
				opacity: 0;
				float: left;
			}
			input[type=checkbox] + label {
				//background:url('https://cdn1.iconfinder.com/data/icons/mimiGlyphs/16/check_mark.png') no-repeat;
				height: 16px;
				width: 16px;
				display:inline-block;
				padding: 10px;
			}
			input[type=checkbox]:checked + label {
				background:url('http://i.stack.imgur.com/oZocc.png') no-repeat;
				height: 16px;
				width: 16px;
				display:inline-block;
				padding: 10px;
				cursor: pointer;
			}
			input_ {
				border: 5px solid white; 
				-webkit-box-shadow: 
					inset 0 0 8px  rgba(0,0,0,0.1),0 0 16px rgba(0,0,0,0.1); 
				-moz-box-shadow: 
					inset 0 0 8px  rgba(0,0,0,0.1),0 0 16px rgba(0,0,0,0.1); 
				box-shadow: 
					inset 0 0 8px  rgba(0,0,0,0.1),0 0 16px rgba(0,0,0,0.1); 
					padding: 15px;
					background: rgba(255,255,255,0.5);
					margin: 0 0 10px 0;
			}
			#newitem {
				margin-top: 20px;
				width: 100%;
			}
			#update {
				margin-top: 20px;
				width: 100%;
			}
'''


newrepomarkup = '''
<!DOCTYPE html>
<html>
	<head>
		{{ link }}
		<style>
			{{ css }}
		</style>
	</head>
	<body>
		<div id="header"></div>
		<div id="list">
			<form method="post">
				<table>
					<tr><td><label for="name">Name:         </td><td> <input name="name"     id="name"     type="text" required />                </td></label></tr>
					<tr><td><label for="url">URL:           </td><td> <input name="url"      id="url"      type="text" required />                </td></label></tr>
					<tr><td><label for="branch">Branch:     </td><td> <input name="branch"   id="branch"   type="text" value="master" required /> </td></label></tr>
					<tr><td><label for="username">Username: </td><td> <input name="username" id="username" type="text" required />                </td></label></tr>
					<tr><td><label for="password">Password: </td><td> <input name="password" id="password" type="password" required />            </td></label></tr>
				</table>
				<input id="add" type="submit" value="Add" />
			</form>
		</div>
		<div id="add"></div>
		<div id="footer"></div>
	</body>
</html>
'''


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
app = Flask(__name__)


## Main page
@app.route('/', methods=['GET'])
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
	css = render_template_string(defaultcss,fontstyle=fonts[fontselected]['fontstyle'])
	html = render_template_string(mainboardmarkup,items=items,link=fonts[fontselected]['link'],css=css)
	return(html)


## Add repo page
@app.route('/repos/new', methods=['GET','POST'])
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
		html = render_template_string(newrepomarkup,items=items,link=fonts[fontselected]['link'],css=css)
	return(html)



## View single repo
@app.route('/repos/<name>', methods=['GET','POST'])
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
