## Example

  Like the previous example, this image is building a very basic image.
However, the template this time is using parameters that can be both defined
in the file as well as set or shadowed in the command line.

## Building

### First run (after running previous example)
```commandline
$ virt-maker build -f examples/20-using_params/template.yml
[ FILE ] examples/20-using_params/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[FIRSTB] yum update -y
[HOSTNA] 20-using_params
[EXPORT] {'path': '20-using_params.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   4.7] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[   8.9] Clearing Linux swap on /dev/sda3
[   9.5] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  26.6] Copy to destination and make sparse
[  45.8] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### First run (without running previous example)
```commandline
$ virt-maker build -f examples/20-using_params/template.yml
[ FILE ] examples/20-using_params/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[  11.2] Downloading: http://builder.libguestfs.org/centos-7.8.xz
[  12.7] Planning how to build this image
[  12.7] Uncompressing
[  28.3] Converting raw to qcow2
[  35.5] Opening the new disk
[  44.6] Setting a random seed
[  44.6] Setting passwords
virt-builder: Setting random password of root to XdDbFRJLourEd616
[  46.3] SELinux relabelling
[  64.8] Finishing off
                   Output file: /home/josiah/.cache/virt-maker/6c97013f6e2e9725537c13396a691092.qcow2
                   Output size: 6.0G
                 Output format: qcow2
            Total usable space: 5.4G
                    Free space: 4.1G (75%)
[ RUN  ] yum clean all
[   0.0] Examining the guest ...
[   8.1] Setting a random seed
[   8.1] Running: /home/josiah/.cache/virt-maker/05715213dbde55bacc5467a6a04f5da9
[  11.5] Finishing off
[FIRSTB] yum update -y
[   0.0] Examining the guest ...
[   7.6] Setting a random seed
[   7.6] Installing firstboot script: /home/josiah/.cache/virt-maker/da0a8575413b1e414d2c0774e5359bfe
[   8.3] Finishing off
[HOSTNA] 20-using_params
[   0.0] Examining the guest ...
[   7.5] Setting a random seed
[   7.5] Setting the hostname: 20-using_params
[   8.0] Finishing off
[EXPORT] {'path': '20-using_params.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.3] Examine source disk
◓ 25% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════⟧ --:--
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  11.3] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  16.3] Clearing Linux swap on /dev/sda3
[  18.0] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  41.3] Copy to destination and make sparse
[  61.1] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/20-using_params/template.yml
[ FILE ] examples/20-using_params/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[FIRSTB] yum update -y
[HOSTNA] 20-using_params
[EXPORT] {'path': '20-using_params.qcow2'}
```
