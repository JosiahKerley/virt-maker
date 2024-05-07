## Example

  Given

## Building

### First run (after running previous example)
```commandline
$ virt-maker build -f examples/70-near_world_example/template.yml
[ FILE ] examples/70-near_world_example/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[ RUN  ] yum clean all
[   0.0] Examining the guest ...
[   8.5] Setting a random seed
[   8.6] Running: /home/josiah/.cache/virt-maker/05715213dbde55bacc5467a6a04f5da9
[  11.3] Finishing off
[ RUN  ] yum update -y
[   0.0] Examining the guest ...
[   7.6] Setting a random seed
[   7.6] Running: /home/josiah/.cache/virt-maker/da0a8575413b1e414d2c0774e5359bfe
[ 481.7] Finishing off
[INSTAL] ['epel-release']
[   0.0] Examining the guest ...
[   8.7] Setting a random seed
[   8.8] Installing packages: epel-release
[  17.8] Finishing off
[INSTAL] ['vim', 'nano', 'tmux', 'htop', 'mlocate']
[   0.0] Examining the guest ...
[   7.8] Setting a random seed
[   7.9] Installing packages: vim nano tmux htop mlocate
[  69.6] Finishing off
[FIRSTB] updatedb
[   0.0] Examining the guest ...
[   8.3] Setting a random seed
[   8.3] Installing firstboot script: /home/josiah/.cache/virt-maker/42efcfb4bf5999edc7703d610d0dfed5
[   9.1] Finishing off
[HOSTNA] 70-near_world_example
[   0.0] Examining the guest ...
[   7.8] Setting a random seed
[   7.9] Setting the hostname: 70-near_world_example
[   8.4] Finishing off
[ RUN  ] touch /.autorelabel
[   0.0] Examining the guest ...
[   7.8] Setting a random seed
[   7.8] Running: /home/josiah/.cache/virt-maker/2fe4092fc5f894ea741849803b3fda0a
[   8.4] Finishing off
[FIRSTB] reboot
[   0.0] Examining the guest ...
[   7.6] Setting a random seed
[   7.6] Installing firstboot script: /home/josiah/.cache/virt-maker/c2d3b74a5462797a09d81ab1ec89d8ad
[   8.4] Finishing off
[EXPORT] {'path': '70-near_world_example.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   4.3] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[   8.9] Clearing Linux swap on /dev/sda3
[   9.6] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  28.7] Copy to destination and make sparse
[  54.6] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### First run (without running previous example)
```commandline
$ virt-maker build -f examples/70-near_world_example/template.yml
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/70-near_world_example/template.yml
```
