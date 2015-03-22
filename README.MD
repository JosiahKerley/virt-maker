Note:
=====
Be advised, this is still pretty early.  I'm still hammering out details with the DSL and provider modules (as well as things like whether or not I want to incorporate jinja2)

Command Line:
=============

usage: virt-maker.py [-h] [--file [VMKFILEPATH [VMKFILEPATH ...]]] [--build]
                     [--noop] [--variables [OVERRIDEVARS [OVERRIDEVARS ...]]]
                     [--show-variables] [--show-template]
                     [--input-format INPUT_FORMAT] [--pretty] [--version]

Libvirt based VM builder

optional arguments:
  -h, --help            show this help message and exit
  --file [VMKFILEPATH [VMKFILEPATH ...]], -f [VMKFILEPATH [VMKFILEPATH ...]]
                        VMK build template file
  --build, -b           Build file
  --noop, -n            Displays provider output only
  --variables [OVERRIDEVARS [OVERRIDEVARS ...]]
                        Override input variables on build
  --show-variables      Shows the input variables for a given *.vmk file
  --show-template       Shows the input template for a given *.vmk file
  --input-format INPUT_FORMAT
                        Set the input format (JSON|Key). Default KEY
  --pretty, -p          Displays output in easily readable format
  --version             show program's version number and exit
