import os
import json
import urllib2



values = {
	"username": "Virt-Maker",
	"text": None,
	"icon_emoji":":construction:",
	"channel": None
	}

def info():
	return('')

def provider(marshal):
	args = marshal['link']['arguments']
	body = marshal['link']['body']
	verbose = marshal['settings']['verbose']

	try:
		values['channel'] = args.split(' ')[0]
		url = 'https://hooks.slack.com/services/' + args.split(' ')[-1]
		values['text'] = body
		data = json.dumps(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		marshal['status'] = True
	except:
		marshal['status'] = False
	return(marshal)
	
