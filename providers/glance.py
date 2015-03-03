'''
Usage:
@glance imagename http://glance.example.com
'''

import os
import json
def provider(body,hash,args,verbose,image,settings):
	name = args.split(' ')[0]
	url = args.split(' ')[1]
	imagesurl = (('%s/%s'%(url,v1/images)).replace('//','/')).replace(':/','://')
	imagemsg = getjson(imagesurl)
	imagedata = False
	for image in imagemsg['images']:
		if image['name'] == name:
			imagedata = image
			break
	