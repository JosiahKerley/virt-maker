## Example

  In this example, a base image is imported using virt-builder
using the `centos-7.8` image and is instanced with a `6G` image.

## Building

### First run
```commandline
$ virt-maker build -f examples/10-basic/template.yml
[ FILE ] examples/10-basic/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[FIRSTB] yum update -y
[HOSTNA] 10-basic
[EXPORT] {'path': '10-basic.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   5.0] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  10.9] Clearing Linux swap on /dev/sda3
[  11.5] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  29.4] Copy to destination and make sparse
[  49.9] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/10-basic/template.yml
[ FILE ] examples/10-basic/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[FIRSTB] yum update -y
[HOSTNA] 10-basic
[EXPORT] {'path': '10-basic.qcow2'}
```
