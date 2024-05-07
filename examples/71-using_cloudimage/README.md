## Example

  In this example, a base image is imported using by downloading a cloud image and handling the initial disk sizing.
This is less reliable and takes more tinkering than using virt-builder, but allows you to use generic cloud images.

## Building

### First run
```commandline
$ virt-maker build -f examples/71-using_cloudimage/template.yml
[ FILE ] examples/71-using_cloudimage/template.yml: Starting                                                                                                                                                   
[IMPORT] examples/71-using_cloudimage/template.yml: {'url': 'https://download.rockylinux.org/pub/rock ... Rocky-9-GenericCloud.latest.x86_64.qcow2', 'resize': {'size': '10G', 'expand': '/dev/sda5'}}
--2024-04-11 00:35:19--  https://download.rockylinux.org/pub/rocky/9/images/x86_64/Rocky-9-GenericCloud.latest.x86_64.qcow2
Resolving download.rockylinux.org (download.rockylinux.org)... 151.101.70.132, 2a04:4e42:10::644
Connecting to download.rockylinux.org (download.rockylinux.org)|151.101.70.132|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1083965440 (1.0G) [application/octet-stream]
Saving to: ‘/root/.cache/virt-maker/9d5c91ecd62a49e10367861e1da8aef4.qcow2_in-progress’

/root/.cache/virt-maker/9d5c91ecd62a49e10367861e1da 100%[==================================================================================================================>]   1.01G  8.04MB/s    in 3m 24s  

2024-04-11 00:38:44 (5.06 MB/s) - ‘/root/.cache/virt-maker/9d5c91ecd62a49e10367861e1da8aef4.qcow2_in-progress’ saved [1083965440/1083965440]

[   0.0] Examining /root/.cache/virt-maker/9d5c91ecd62a49e10367861e1da8aef4.qcow2_in-progress
**********

Summary of changes:

virt-resize: /dev/sda1: This partition will be left alone.

virt-resize: /dev/sda2: This partition will be left alone.

virt-resize: /dev/sda3: This partition will be left alone.

virt-resize: /dev/sda4: This partition will be left alone.

virt-resize: /dev/sda5: This partition will be resized from 8.9G to 8.9G.  
The filesystem xfs on /dev/sda5 will be expanded using the ‘xfs_growfs’ 
method.

**********
[   5.7] Setting up initial partition table on /root/.cache/virt-maker/9d5c91ecd62a49e10367861e1da8aef4.qcow2.raw
[  23.3] Copying /dev/sda1
[  23.5] Copying /dev/sda2
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  26.1] Copying /dev/sda3
[  26.1] Copying /dev/sda4
[  26.1] Copying /dev/sda5
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  36.6] Expanding /dev/sda5 using the ‘xfs_growfs’ method

virt-resize: Resize operation completed with no errors.  Before deleting 
the old disk, carefully check that the resized disk boots and works 
correctly.
[ RUN  ] examples/71-using_cloudimage/template.yml: dnf clean all
[   0.0] Examining the guest ...
[   6.2] Setting a random seed
[   6.2] Setting the machine ID in /etc/machine-id
[   6.2] Running: /root/.cache/virt-maker/dc9cd26d9d1e74a575e0bde69956f23f
[   7.2] Finishing off
[FIRSTB] examples/71-using_cloudimage/template.yml: dnf update -y
[   0.0] Examining the guest ...
[   5.8] Setting a random seed
[   5.8] Installing firstboot script: /root/.cache/virt-maker/504eba249c1c0611dc79b4fe970f53b4
[   5.9] Finishing off
[HOSTNA] examples/71-using_cloudimage/template.yml: 71-using_cloudimage
[   0.0] Examining the guest ...
[   5.8] Setting a random seed
[   5.8] Setting the hostname: 71-using_cloudimage
[   5.9] Finishing off
[EXPORT] examples/71-using_cloudimage/template.yml: {'path': 'images/71-using_cloudimage.qcow2', 'create_dir': False, 'level': 1}
[   0.0] Create overlay file in /root/.cache/virt-maker to protect source disk
[   0.0] Examine source disk
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[   7.3] Fill free space in /dev/sda1 with zero
[   8.2] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  10.6] Fill free space in /dev/sda5 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  45.3] Copy to destination and make sparse
[  58.1] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
[   0.0] Create overlay file in /root/.cache/virt-maker to protect source disk
[   0.0] Examine source disk
[   2.4] Fill free space in /dev/sda1 with zero
[   3.4] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[   6.0] Fill free space in /dev/sda5 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  32.1] Copy to destination and make sparse
[  92.1] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/71-using_cloudimage/template.yml
[ FILE ] examples/71-using_cloudimage/template.yml: Starting
[IMPORT] examples/71-using_cloudimage/template.yml: {'url': 'https://download.rockylinux.org/pub/rock ... Rocky-9-GenericCloud.latest.x86_64.qcow2', 'resize': {'size': '10G', 'expand': '/dev/sda5'}}
[ RUN  ] examples/71-using_cloudimage/template.yml: dnf clean all
[FIRSTB] examples/71-using_cloudimage/template.yml: dnf update -y
[HOSTNA] examples/71-using_cloudimage/template.yml: 71-using_cloudimage
[EXPORT] examples/71-using_cloudimage/template.yml: {'path': 'images/71-using_cloudimage.qcow2', 'create_dir': False, 'level': 1}
```
