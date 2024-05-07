#!/usr/bin/env python3
# (c) 2015-2024, Josiah Kerley <josiahkerley@gmail.com>
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

import os
import sys
import time
import subprocess
from vncdotool import api
from virtmaker.utils.cli import ShellPrinter
from virtmaker.utils.vnc import VNC

from subprocess import Popen, PIPE
from datetime import datetime, timedelta
import threading
import psutil


def runCmd(cmd: str) -> bool:
    with ShellPrinter(tag="cmd", verbosity=1, tag_color='white') as print:
        print(cmd)
        if os.system(cmd) == 0:
            return True
        return False


def list_bound_ports():
    return [conn.laddr.port for conn in psutil.net_connections()]

def find_free_port(start, end):
    for port in range(start, end):
        if port not in list_bound_ports():
            return port

## TODO:  Clean this mess up
def runQemuCmdVncKeystrokes(cmd: str, keystrokes: str, delay_time: float = 40, key_delay_time: float = 0.1,
                            timeout: int = 3600) -> bool:

    def thread_target(process, timeout):
        start_time = datetime.now()
        while True:
            if datetime.now() - start_time > timedelta(seconds=timeout):
                print(f"Timeout reached, killing qemu")
                process.kill()
                break
            output = process.stderr.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                print("QEMU stderr output: " + output.strip())

    if not delay_time:
        delay_time = 40
    else:
        delay_time = float(delay_time)
    if not key_delay_time:
        key_delay_time = 0.1
    else:
        key_delay_time = float(key_delay_time)
    if not timeout:
        timeout = 3600
    else:
        timeout = int(timeout)

    vnc_port = find_free_port(5900, 5910)
    if not vnc_port:
        print("Failed to find a free port")
        sys.exit(1)
    print(f"Running VNC on port {vnc_port}")
    print(f"Connect remotely with an ssh tunnel: `ssh -L 1{vnc_port}:localhost:{vnc_port} user@host` "
          f"and then connect with a VNC client: `vncviewer localhost:1{vnc_port}`")
    print(f"Connect locally with a VNC client: localhost:{vnc_port}")
    cmd = f"{cmd} -vnc :{vnc_port-5900}"
    print(f"Running command: {cmd}")
    qemu_process = Popen(cmd, shell=True, stderr=PIPE)
    stderr_thread = threading.Thread(target=thread_target, args=(qemu_process, timeout,))
    stderr_thread.daemon = True
    stderr_thread.start()

    print(f"Waiting {delay_time} seconds for the VM to start")
    time.sleep(float(delay_time))
    if keystrokes:
        with VNC(api.connect(f"localhost:{vnc_port - 5900}:{vnc_port}")) as vnc:
            for keystroke_type in keystrokes:
                if 'blind' in keystroke_type.keys():
                    vnc.send_blind_keystrokes(keystrokes=keystroke_type['blind'], key_delay_time=key_delay_time)
                elif 'ocr' in keystroke_type.keys():
                    vnc.send_ocr_keystrokes(expectations=keystroke_type['ocr'], key_delay_time=key_delay_time)

    print(f"Waiting {timeout} seconds for QEMU to poweroff")
    start_time = datetime.now()
    stderr_thread.join(timeout)
    exec_time = datetime.now() - start_time
    if exec_time > timedelta(seconds=timeout):
        print(f"QEMU took too long, killing after {exec_time}")
        return False
    thread_exit_code = qemu_process.poll()
    if not thread_exit_code == 0:
        print(f"QEMU failed with exit code {thread_exit_code}")
        return False
    return True

def runCmdCaptureOutput(cmd: str) -> (bool, str, str):
    with ShellPrinter(tag="cmd", verbosity=1, tag_color='white') as print:
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdout, stderr) = p.communicate()
        exit_code = p.wait()
        if exit_code == 0:
            return True, stdout, stderr
        else:
            return False, stdout, stderr

def runCmds(cmds: list, ignore_errors=False) -> bool:
    retval = True
    retvals = []
    for cmd in cmds:
        if ignore_errors:
            retvals.append(runCmd(cmd))
        else:
            if not runCmd(cmd):
                print(f"failed to run '{cmd}'")
                return False
    if ignore_errors:
        return all(retvals)
    return retval



