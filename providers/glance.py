'''
Usage:
@glance imagename http://glance.example.com
'''

import os
import json
def info():
	return('')
def provider(marshal):
	args = marshal['link']['arguments']
	body = marshal['link']['body']
	verbose = marshal['settings']['verbose']
	name = args.split(' ')[0]
	url = args.split(' ')[1]
	imagesurl = (('%s/%s'%(url,v1/images)).replace('//','/')).replace(':/','://')
	imagemsg = getjson(imagesurl)
	imagedata = False
	for image in imagemsg['images']:
		if image['name'] == name:
			imagedata = image
			break
	if os.system(cmd) == 0:
		marshal['status'] = True
	else:
		marshal['status'] = False
	return(marshal)