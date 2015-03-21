import os
import json
import reques
import urllib2



values = {
	"username": "Virt-Maker",
	"text": None,
	"construction": ":ghost:",
	"channel": None
	}


def provider(body,hash,args,verbose,image,settings):
	values['channel'] = args.split(' ')[0]
	url = 'https://hooks.slack.com/services/' + args.split(' ')[-1]
	values['text'] = body
	data = json.dumps(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	return(True)
	
	
