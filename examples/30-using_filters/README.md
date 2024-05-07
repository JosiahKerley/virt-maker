## Example

  Not only do the templates support parametric keys and values,
but they also support some built in custom filter to provide handy
values in the spec.  In this example a filter will produce a value
that will cause the rolling hash to always update in the spec with
the `random_hostname()` function as well as `random_word()`.
  Some filters can be dynamic and cause the build chain in the spec
to fork leading to a new chain that needs building.

## Building

### First run (after running previous example)
```commandline
$ virt-maker build -f examples/30-using_filters/template.yml
[ FILE ] examples/30-using_filters/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[FIRSTB] yum update -y
[ RUN  ] echo 'eutaxy' > /random_word
[   0.0] Examining the guest ...
[   8.5] Setting a random seed
[   8.5] Running: /home/josiah/.cache/virt-maker/bb24b412b36728e5a41d4eee01eec914
[   9.0] Finishing off
[HOSTNA] houri-puppify
[   0.0] Examining the guest ...
[   7.6] Setting a random seed
[   7.7] Setting the hostname: houri-puppify
[   8.2] Finishing off
[EXPORT] {'path': 'houri-puppify.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   4.5] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[   9.2] Clearing Linux swap on /dev/sda3
[  10.1] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  28.1] Copy to destination and make sparse
[  51.5] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### First run (without running previous example)
```commandline
$ virt-maker build -f examples/30-using_filters/template.yml
[ FILE ] examples/30-using_filters/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[  13.2] Downloading: http://builder.libguestfs.org/centos-7.8.xz
[  14.5] Planning how to build this image
[  14.5] Uncompressing
[  31.8] Converting raw to qcow2
[  40.8] Opening the new disk
[  50.1] Setting a random seed
[  50.2] Setting passwords
virt-builder: Setting random password of root to csG7Ch80WzoYvsGa
[  52.0] SELinux relabelling
[  74.2] Finishing off
                   Output file: /home/josiah/.cache/virt-maker/6c97013f6e2e9725537c13396a691092.qcow2
                   Output size: 6.0G
                 Output format: qcow2
            Total usable space: 5.4G
                    Free space: 4.1G (75%)
[ RUN  ] yum clean all
[   0.0] Examining the guest ...
[   8.4] Setting a random seed
[   8.5] Running: /home/josiah/.cache/virt-maker/05715213dbde55bacc5467a6a04f5da9
[  11.3] Finishing off
[FIRSTB] yum update -y
[   0.0] Examining the guest ...
[   8.3] Setting a random seed
[   8.3] Installing firstboot script: /home/josiah/.cache/virt-maker/da0a8575413b1e414d2c0774e5359bfe
[   9.2] Finishing off
[ RUN  ] echo 'danglingly' > /random_word
[   0.0] Examining the guest ...
[   8.2] Setting a random seed
[   8.3] Running: /home/josiah/.cache/virt-maker/4b7e2486575da52232ae285b9d542e6b
[   8.8] Finishing off
[HOSTNA] forseek-locks
[   0.0] Examining the guest ...
[   8.7] Setting a random seed
[   8.7] Setting the hostname: forseek-locks
[   9.1] Finishing off
[EXPORT] {'path': 'forseek-locks.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
◓ 25% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════⟧ --:--
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  12.5] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  17.2] Clearing Linux swap on /dev/sda3
[  18.0] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  37.2] Copy to destination and make sparse
[  57.8] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/30-using_filters/template.yml
[ FILE ] examples/30-using_filters/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[FIRSTB] yum update -y
[ RUN  ] echo 'crablet' > /random_word
[   0.0] Examining the guest ...
[   8.3] Setting a random seed
[   8.3] Running: /home/josiah/.cache/virt-maker/ec39fea0d9953bad2e3744f45a88b3ec
[   8.9] Finishing off
[HOSTNA] wamefou-quinto
[   0.0] Examining the guest ...
[   7.7] Setting a random seed
[   7.7] Setting the hostname: wamefou-quinto
[   8.2] Finishing off
[EXPORT] {'path': 'wamefou-quinto.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   5.1] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[   9.5] Clearing Linux swap on /dev/sda3
[  10.5] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  29.0] Copy to destination and make sparse
[  48.1] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```
