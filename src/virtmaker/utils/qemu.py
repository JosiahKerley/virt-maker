#!/usr/bin/env python3
# (c) 2015-2025, Josiah Kerley <josiahkerley@gmail.com>
#
# This file is part of Virt Maker.
#
# Virt Maker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Virt Maker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Virt Maker.  If not, see <http://www.gnu.org/licenses/>.


from virtmaker.utils.cmd import runCmdCaptureOutput, runCmd


def qemu_img_list_snapshots(disk_image_filepath: str) -> list:
    cmd = f"qemu-img snapshot '{disk_image_filepath}' -l"
    retval, stdout, stderr = runCmdCaptureOutput(cmd)
    snapshots = []
    for line in stdout.splitlines()[2:]:
        snapshots.append(str(line.split()[1].decode()))
    return snapshots

def qemu_img_create_snapshot(disk_image_filepath: str, name: str) -> bool:
    cmd = f'qemu-img snapshot {disk_image_filepath} -c "{name}"'
    return runCmd(cmd)

def qemu_img_revert_snapshot(disk_image_filepath: str, name: str) -> bool:
    cmd = f'qemu-img snapshot {disk_image_filepath} -a "{name}"'
    return runCmd(cmd)

def qemu_img_delete_snapshot(disk_image_filepath: str, name: str) -> bool:
    cmd = f'qemu-img snapshot {disk_image_filepath} -d "{name}"'
    return runCmd(cmd)
