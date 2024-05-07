## Example

  As you export an image from the build chain often it is need
to run a script before or after the export process.  Using `pre_script`
and `post_script` keys in the export stanza you can run script local
to the build machine to facilitate actions such as pre-provisioning
storage space or ad-hoc uploading images after an export completes.

## Building

### First run (after running previous example)
```commandline
$ virt-maker build -f examples/40-export_scripts/template.yml
[ FILE ] examples/40-export_scripts/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[EXPORT] {'path': '40-export_scripts.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.3] Examine source disk
[   5.6] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  10.6] Clearing Linux swap on /dev/sda3
[  11.4] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  34.7] Copy to destination and make sparse
[  58.6] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### First run (without running previous example)
```commandline
$ virt-maker build -f examples/40-export_scripts/template.yml
[ FILE ] examples/40-export_scripts/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[EXPORT] {'path': '40-export_scripts.qcow2'}
(venv) [josiah@thinkpad-carbonx1 virt-maker]$ rm -rf ~/.cache/virt-maker/
(venv) [josiah@thinkpad-carbonx1 virt-maker]$ virt-maker build -f examples/40-export_scripts/template.yml
[ FILE ] examples/40-export_scripts/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[   8.8] Downloading: http://builder.libguestfs.org/centos-7.8.xz
[  10.2] Planning how to build this image
[  10.2] Uncompressing
[  28.3] Converting raw to qcow2
[  35.9] Opening the new disk
[  45.0] Setting a random seed
[  45.0] Setting passwords
virt-builder: Setting random password of root to QJFfQEz2ygjMuHMb
[  47.0] SELinux relabelling
[  69.1] Finishing off
                   Output file: /home/josiah/.cache/virt-maker/6c97013f6e2e9725537c13396a691092.qcow2
                   Output size: 6.0G
                 Output format: qcow2
            Total usable space: 5.4G
                    Free space: 4.1G (75%)
[EXPORT] {'path': '40-export_scripts.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
◓ 25% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════⟧ --:--
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  14.1] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  19.3] Clearing Linux swap on /dev/sda3
[  20.1] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  38.5] Copy to destination and make sparse
[  63.6] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/40-export_scripts/template.yml
[ FILE ] examples/40-export_scripts/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[EXPORT] {'path': '40-export_scripts.qcow2'}
```
