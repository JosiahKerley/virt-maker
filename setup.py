#!/usr/bin/env python
import os
import sys
from distutils.core import setup

## Globals
here = os.path.dirname(os.path.realpath(__file__))
install_file = '/usr/local/bin/virt-maker'
install_dirs = [
  '/usr/local/bin',
  '/var/lib/virt-maker',
  '/var/lib/virt-maker/providers',
]

setup(name='Virt-Maker',
  version='0.2',
  description='Libvirt based VM builder',
  author='Josiah Kerley',
  author_email='josiahkerley@gmail.com',
  url='https://github.com/JosiahKerley/virt-maker',
  require=['argparse','pyyaml','filelock'],
)


## Copy
if 'install' in sys.argv:
  for dir in install_dirs:
    if not os.path.isdir(dir):
      os.makedirs(dir)
  with open('%s/virt-maker.py'%(here),'r') as f:
    file_content = f.read()
  with open(install_file,'w') as f:
    f.write(file_content)
  os.system('chmod +x "%s"'%(install_file))
  for provider in os.listdir(here+'/providers'):
    if provider.endswith('.py'):
      with open(here+'/providers/'+provider,'r') as f:
        with open('/var/lib/virt-maker/providers/'+provider,'w') as c:
          c.write(f.read())