import os
import hashlib
import shutil
import stat
import signal
import sys

import psutil

from virtmaker.config import get_cache_dir
from virtmaker.utils.cli import ShellPrinter
from virtmaker.utils.cmd import runCmd
from virtmaker.utils.qemu import qemu_img_revert_snapshot, qemu_img_create_snapshot, qemu_img_list_snapshots, qemu_img_delete_snapshot
from virtmaker.utils.schema import getValidatedData

_runner_cache = {}


class Runner:
    _cache = _runner_cache
    _spec_config = {}
    _spec_schema = NotImplemented
    _tag = NotImplemented
    _required_commands = [[NotImplemented]]
    _previous = None
    _last_result = None
    _warning_messages = []

    def __init__(self, spec_config, previous=None, image_name=None):
        with ShellPrinter(tag=self._tag) as step_print:
            for command_set in self._required_commands:
                found = False
                for command in command_set:
                    if shutil.which(command):
                        found = True
                        break
                if not found:
                    raise Exception(f"could not find one of commands {command_set}")
            if isinstance(spec_config, dict):
                spec_config = getValidatedData(self._spec_schema, spec_config)
            step_print(spec_config)
            self._spec_config = spec_config
            self._previous = previous
            self._signature = self.get_signature()
            self._cache_dir = get_cache_dir()
            if not os.path.isdir(self._cache_dir):
                os.makedirs(self._cache_dir)
            self._image_name = image_name
            self.disk_image_filepath = os.path.join(self._cache_dir, self._image_name)
            if not self._setup():
                raise Exception('Failed setting up')
            for message in self._warning_messages:
                step_print(message)

    def __enter__(self):
        if not self._isStepAlreadyRan():
            self._snapshot_revert()
            # TODO: Why is this here?
            self._snapshot_create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.cleanup():
            raise Exception('failed to cleanup')
        if not self._last_result == False:
            self._snapshot_finalize()
        else:
            print("step failed, not finalizing snapshot")
            self.die()

    @classmethod
    def validate(cls, spec_config):
        return NotImplemented

    @classmethod
    def generate_hash(cls, source):
        result = hashlib.md5(str(source).encode())
        return str(result.hexdigest())

    def get_signature(self, append_to_signature=None):
        return self.generate_hash(str(self._previous).encode()+str(self._spec_config).encode()+str(append_to_signature).encode())

    def execute(self):
        if not self._isStepAlreadyRan():
            if not self._run_pre_script():
                raise Exception("failed running pre_script section")
            retval = self._run(), self.disk_image_filepath, self._signature
            if not self._run_post_script():
                raise Exception("failed running post_script section")
            return retval
        return None, self.disk_image_filepath, self._signature

    def cleanup(self):
        return NotImplemented

    def die(self):
        os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)
        sys.exit(1)

    def _snapshot_revert(self):
        if os.path.isfile(self.disk_image_filepath) and self._previous:
            snapshot_name = self._previous
            assert qemu_img_revert_snapshot(self.disk_image_filepath, snapshot_name)

    def _snapshot_create(self):
        if not os.path.isfile(self.disk_image_filepath):
            return
        snapshot_name = self._signature
        temp_snapshot_name = f"{snapshot_name}_in-progress"
        if not 'snapshots' in self._cache.keys():
            self._cache['snapshots'] = qemu_img_list_snapshots(self.disk_image_filepath)
        if not snapshot_name in self._cache['snapshots']:
            if temp_snapshot_name in self._cache['snapshots']:
                qemu_img_delete_snapshot(self.disk_image_filepath, temp_snapshot_name)
            assert qemu_img_create_snapshot(self.disk_image_filepath, temp_snapshot_name)
            self._cache['snapshots'].append(temp_snapshot_name)

    def _snapshot_finalize(self):
        if not os.path.isfile(self.disk_image_filepath):
            return
        snapshot_name = self._signature
        temp_snapshot_name = f"{snapshot_name}_in-progress"
        if not 'snapshots' in self._cache.keys():
            self._cache['snapshots'] = qemu_img_list_snapshots(self.disk_image_filepath)
        if not snapshot_name in self._cache['snapshots']:
            assert qemu_img_create_snapshot(self.disk_image_filepath, snapshot_name)
            if temp_snapshot_name in self._cache['snapshots']:
                qemu_img_delete_snapshot(self.disk_image_filepath, temp_snapshot_name)
                self._cache['snapshots'].remove(temp_snapshot_name)
            self._cache['snapshots'].append(snapshot_name)

    def _setup(self):
        return NotImplemented



    def _isStepAlreadyRan(self):
        snapshot_name = self._signature
        if not 'snapshots' in self._cache.keys():
            self._cache['snapshots'] = qemu_img_list_snapshots(self.disk_image_filepath)
        if snapshot_name in self._cache['snapshots']:
            return True
        else:
            return False

    def _run(self):
        return NotImplemented

    def _run_script(self, script_string):
        tmp_script_path = os.path.join(self._cache_dir, f"{self._signature}.script")
        with open(tmp_script_path, 'w') as f:
            f.write(script_string)
        st = os.stat(tmp_script_path)
        os.chmod(tmp_script_path, st.st_mode | stat.S_IEXEC)
        return runCmd(tmp_script_path)

    def _run_pre_script(self):
        if (isinstance(self._spec_config, dict) and 'pre_script' in self._spec_config.keys()
                and self._spec_config['pre_script']):
            return self._run_script(self._spec_config['pre_script'])
        return True

    def _run_post_script(self):
        if (isinstance(self._spec_config, dict) and 'post_script' in self._spec_config.keys()
                and self._spec_config['post_script']):
            return self._run_script(self._spec_config['post_script'])
        return True

    def _is_qcow2_opened_by_another_process(self):
        for proc in psutil.process_iter(['pid', 'open_files']):
            try:
                for file in proc.info['open_files'] or []:
                    if file.path == self.disk_image_filepath:
                        return False
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return True
