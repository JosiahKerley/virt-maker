#!/usr/bin/env python
import os
import sys
from setuptools import setup


## Globals
here = os.path.dirname(os.path.realpath(__file__))
install_file = '/usr/local/bin/virt-maker'
install_dirs = [
  '/usr/local/bin',
  '/var/lib/virt-maker',
  '/var/lib/virt-maker/providers',
]




## Main Setup
setup(
  name             = 'virt-maker',
  version          = '0.1.2',
  description      = 'Virtual machine build tool',
  author           = 'Josiah Kerley',
  author_email     = 'josiahkerley@gmail.com',
  url              = 'https://github.com/JosiahKerley/virt-maker',
  install_requires = [
    'argparse',
    'PyYAML',
    'filelock',
    'jinja2',
    'requests',
    'python-swiftclient',
    'python-glanceclient',
    'python-cinderclient',
    'python-novaclient',
    'python-neutronclient'
  ]
)

## Copy
if 'install' in sys.argv:
  for dir in install_dirs:
    if not os.path.isdir(dir):
      os.makedirs(dir)
  with open('%s/virt-maker/__init__.py'%(here),'r') as f:
    file_content = f.read()
  with open(install_file,'w') as f:
    f.write(file_content)
  os.system('chmod +x "%s"'%(install_file))
  for provider in os.listdir(here+'/providers'):
    if provider.endswith('.py'):
      with open(here+'/providers/'+provider,'r') as f:
        with open('/var/lib/virt-maker/providers/'+provider,'w') as c:
          c.write(f.read())
