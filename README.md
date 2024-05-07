<p align="center">
  <img src=".media/splash.png" alt="A penguin holding a blacksmith hammer in a metalworking shop banging on an anvil.  The penguin is building metal boxes.  There are many metal boxes stacked in the background.">
</p>

Abstract:
=========

  Virt Maker is a command line tool for automating the creation
of disk images heavily centered around libguestfs and quick turnaround.

  It utilizes a straight-forward template system to define a specification
for how an image needs to be built and uses snapshotting and rolling hashes
to fast-forward over known good completed steps.

  The thesis of this project is to provide a tool that can support 
rapid appliance image creation for virtualization environments
where the boot volume is considered ephemeral and can be replaced quickly.

  Template files will generate specs that define where an initial image
comes from, what offline (or online in certain scenarios) steps need to
run in order to configure the image, and once complete; how to store
the resulting image.


Demo:
=====

## Building a new template with no previous cache:
```commandline
$ virt-maker build -f examples/10-basic/template.yml
```
<p align="center">
  <img src=".media/first-run-ff.cast.gif" alt="Demo building a template">
</p>

## Running again with the same template:
Since the template has already been built, the second run will be instant.
This is because all the steps have been cached and the final image is already complete.
```commandline
[ FILE ] examples/10-basic/template.yml: Starting
[IMPORT] examples/10-basic/template.yml: {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] examples/10-basic/template.yml: yum clean all
[FIRSTB] examples/10-basic/template.yml: yum update -y
[HOSTNA] examples/10-basic/template.yml: 10-basic
[EXPORT] examples/10-basic/template.yml: {'path': 'images/10-basic.qcow2'}
```

Command Line Usage:
===================

## Overview
```
usage: virt-maker [-h] [-v] [-V] {build,cache,runners} ...

positional arguments:
  {build,cache,runners}
                        Actions

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -V, --version         Show virt-maker version
```

## Template Building
```
usage: virt-maker build [-h] -f BUILD_FILES [BUILD_FILES ...] [-p BUILD_PARAMS [BUILD_PARAMS ...]] [-F] [-X]

optional arguments:
  -h, --help            show this help message and exit
  -f BUILD_FILES [BUILD_FILES ...], --file BUILD_FILES [BUILD_FILES ...]
                        Path to template file(s)
  -p BUILD_PARAMS [BUILD_PARAMS ...], --param BUILD_PARAMS [BUILD_PARAMS ...]
                        Set or override template parameter
  -F, --force           Force build from scratch
  -X, --force-export    Force export to re-run
```

## Cache Management
```
usage: virt-maker cache [-h] [-H] {clean,usage}

positional arguments:
  {clean,usage}

options:
  -h, --help            show this help message and exit
  -H, --human-readable  Output as human-readable values
```

## Runner Information
```
usage: virt-maker runners [-h] {steps,importers,exporters}

positional arguments:
  {steps,importers,exporters}
                        Show the types of runners

optional arguments:
  -h, --help            show this help message and exit
```

Templates
=========

Virt Maker uses a YAML file to define a template generating a build spec that consists of input parameters
and the build specification template itself.  The `params` section is used to define the input parameters
and the `spec` section is used to define the build steps.

## Basic template format
```yaml
params:
  foo: bar
spec:
  import:
    some-import-runner:
      runner:
      args:
  steps:
    - some-step-runner:
        runner:
        args:
    - another-step-runner:
        more:
        args:
  export:
    some-export-runner:
      some-arg: '{{ foo }}'
```

## Examples
See the [Examples](examples/) directory.


Installing
==========

## Prerequisites command line tools/packages
* scp
* virt-customize
* qemu-system-x86_64 or /usr/libexec/qemu-kvm
* virt-sysprep
* wget
* virt-resize
* truncate
* virt-builder
* cp or pv
* mv
* virt-sparsify
* words
* tesseract

### Optional
* libguestfs-xfs
* libguestfs-zfs
* libguestfs-ufs
* libguestfs-rsync
* libguestfs-winsupport
* virt-win-reg
* virt-v2v
* xz
* gzip
* lz4c

## Installing with pip
```commandline
pip install .
```

## Preparing a build host

### EL Based

#### Basic Rocky Linux 9 Example
```commandline
dnf install -y python-pip epel-release
pip install .
export LIBGUESTFS_BACKEND=direct
dnf install -y words qemu-kvm guestfs-tools wget xz lz4 pv tesseract
```

#### Test to see if it works
```commandline
virt-maker build -f examples/10-basic/template.yml
```
