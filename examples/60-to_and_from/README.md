## Example

  Given that there are many shared configuration steps in the creation of
base images, there's a need to break up steps into common discreet 'pre'
and 'post' phases whos build chains should be shared among a number of
common appliance specifications.  The `to` and `from` keys provide a
facility to pull in params, steps, imports, and exports so that a
consitent chain can be maintained without duplicating work.

  Instead of having to build, publish, and subsequently pull a base image
where the build chain is already a known entity, the build chain itself
can be 'pulled' into the spec.

  The `from` key will merge beneath the current template; where
the current template will override any hashes, append and lists before,
and import any undefined values whereas the `to` key will append any lists
as override any hashes or values.

  This is extremely useful in scenarios such as where you have a base template
that has security/monitoring/user/domain/realm/etc/etc/etc configs and you want
to use that certified template as a base for your appliance.

## Building

### First run (after running previous example)
```commandline
$ virt-maker build -f examples/60-to_and_from/template.yml
[ FILE ] examples/60-to_and_from/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[HOSTNA] 60-to_and_from
[   0.0] Examining the guest ...
[   9.0] Setting a random seed
[   9.0] Setting the hostname: 60-to_and_from
[   9.5] Finishing off
[EXPORT] {'path': '60-to_and_from.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.4] Examine source disk
[   4.7] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  12.0] Clearing Linux swap on /dev/sda3
[  12.8] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  33.4] Copy to destination and make sparse
[  57.0] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### First run (without running previous example)
```commandline
$ virt-maker build -f examples/60-to_and_from/template.yml
[ FILE ] examples/60-to_and_from/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[   7.1] Downloading: http://builder.libguestfs.org/centos-7.8.xz
[   8.4] Planning how to build this image
[   8.4] Uncompressing
[  26.1] Converting raw to qcow2
[  34.9] Opening the new disk
[  42.6] Setting a random seed
[  42.6] Setting passwords
virt-builder: Setting random password of root to UJHBftWgoFo9iSqq
[  44.2] SELinux relabelling
[  61.8] Finishing off
                   Output file: /home/josiah/.cache/virt-maker/6c97013f6e2e9725537c13396a691092.qcow2
                   Output size: 6.0G
                 Output format: qcow2
            Total usable space: 5.4G
                    Free space: 4.1G (75%)
[HOSTNA] 60-to_and_from
[   0.0] Examining the guest ...
[   7.6] Setting a random seed
[   7.6] Setting the hostname: 60-to_and_from
[   8.5] Finishing off
[EXPORT] {'path': '60-to_and_from.qcow2'}
[   0.2] Create overlay file in /home/josiah/.cache/virt-maker to protect source disk
[   0.3] Examine source disk
◓ 25% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════⟧ --:--
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  11.0] Fill free space in /dev/sda2 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ --:--
[  16.4] Clearing Linux swap on /dev/sda3
[  17.1] Fill free space in /dev/sda4 with zero
 100% ⟦▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒⟧ 00:00
[  34.8] Copy to destination and make sparse
[  54.9] Sparsify operation completed with no errors.
virt-sparsify: Before deleting the old disk, carefully check that the 
target disk boots and works correctly.
```

### Second run without changes to the template
```commandline
$ virt-maker build -f examples/60-to_and_from/template.yml
[ FILE ] examples/60-to_and_from/template.yml
[IMPORT] {'image': 'centos-7.8', 'size': '6G'}
[HOSTNA] 60-to_and_from
[EXPORT] {'path': '60-to_and_from.qcow2'}
```
