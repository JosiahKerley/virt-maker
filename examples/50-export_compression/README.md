## Example

  Using exporters that support compression, completed appliance images
can be compressed as a step during the build of the spec.

## Building

### First run (after running previous example)
```commandline
$ virt-maker build -f examples/50-export_compression/template.yml
[ FILE ] examples/50-export_compression/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[EXPORT] {'path': '50-export_compression.qcow2.lz', 'compress': 'lz4', 'level': '1'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   5.9] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  12.4] Clearing Linux swap on /dev/sda3
[  13.1] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  33.3] Copy to destination and make sparse
[  56.3] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
1.23GiB 0:00:08 [ 147MiB/s] [========================================================================================================================================>] 100%      
```

### First run (without running previous example)
```commandline
$ virt-maker build -f examples/50-export_compression/template.yml
[ FILE ] examples/50-export_compression/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[  11.7] Downloading: http://builder.libguestfs.org/centos-7.8.xz
[  13.3] Planning how to build this image
[  13.3] Uncompressing
[  31.5] Converting raw to qcow2
[  42.9] Opening the new disk
[  50.2] Setting a random seed
[  50.3] Setting passwords
virt-builder: Setting random password of root to nNCW9I141mqD4oXL
[  52.1] SELinux relabelling
[  74.1] Finishing off
                   Output file: /home/josiah/.cache/virt-maker/6c97013f6e2e9725537c13396a691092.qcow2
                   Output size: 6.0G
                 Output format: qcow2
            Total usable space: 5.4G
                    Free space: 4.1G (75%)
[EXPORT] {'path': '50-export_compression.qcow2.lz', 'compress': 'lz4', 'level': '1'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
◓ 25% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════⟧ --:--
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  12.9] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  18.0] Clearing Linux swap on /dev/sda3
[  18.7] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  38.0] Copy to destination and make sparse
[  61.6] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
1.23GiB 0:00:08 [ 144MiB/s] [========================================================================================================================================>] 100%
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/50-export_compression/template.yml
[ FILE ] examples/50-export_compression/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[EXPORT] {'path': '50-export_compression.qcow2.lz', 'compress': 'lz4', 'level': '1'}
```
