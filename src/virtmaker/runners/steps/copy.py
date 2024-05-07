import os
import shutil

from virtmaker.runners.steps.virtcustomize import VirtCustomize
from virtmaker.utils.cmd import runCmd


class Copy(VirtCustomize):
    _tag = "copy"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not 'dest' in spec.keys():
            raise Exception("'dest' is required for copy step")
        if not 'content' in spec.keys():
            raise Exception("'content' is required for copy step")
        if 'simple' in spec.keys() and not isinstance(spec['simple'], bool):
            raise Exception("'simple' must be a boolean")

    def _setup(self):
        if not self._isStepAlreadyRan():
            self._dest_dir = os.path.dirname(self._spec_config["dest"])
            self._dest_filename = os.path.basename(self._spec_config["dest"])
            if self._spec_config.get('simple', False):
                cust_runtype_opt = f'--firstboot-command'
            else:
                cust_runtype_opt = f'--run-command'
            cmd = f'virt-customize ' \
                  f'-a {self.disk_image_filepath} ' \
                  f'{cust_runtype_opt} \'' \
                  f'[[ -d "{self._dest_dir}" ]] || mkdir -p "{self._dest_dir}"' \
                  f'\' {self._relabel_opt}'
            self._last_result = runCmd(cmd)
            return self._last_result
        return True

    def _getVirtCustomizeArgs(self):
        if not os.path.isfile(self._spec_config['content']):
            local_file_path = self._write_local_file()
        else:
            local_file_path = self._copy_local_file(self._spec_config['content'])

        if self._spec_config.get('simple', False):
            return ['--copy-in', f'{local_file_path}:{self._dest_dir}']
        else:
            return ['--run-command', f'cp {local_file_path} {self._dest_dir}']

    def _write_local_file(self):
        local_file_path = os.path.join(self._cache_dir, self._signature)
        with open(local_file_path, 'w') as f:
            f.write(self._spec_config['content'])
        return local_file_path

    def _copy_local_file(self, filepath):
        local_file_path = os.path.join(self._cache_dir, self._signature)
        shutil.copy2(filepath, local_file_path)
        return local_file_path

    def cleanup(self):
        local_file_path = os.path.join(self._cache_dir, self._signature)
        if os.path.isfile(local_file_path):
            os.remove(local_file_path)
        if not self._isStepAlreadyRan():
            if self._spec_config.get('simple', False):
                cust_runtype_opt = f'--firstboot-command'
            else:
                cust_runtype_opt = f'--run-command'
            cmds = [f'virt-customize ' \
                  f'-a {self.disk_image_filepath} ' \
                  f'{cust_runtype_opt} \'' \
                  f'mv -f "{self._dest_dir}/{self._signature}" "{self._dest_dir}/{self._dest_filename}"' \
                  f'\' {self._relabel_opt}']
            if 'chmod' in self._spec_config.keys():
                cmds += [f'virt-customize ' \
                      f'-a {self.disk_image_filepath} ' \
                      f'{cust_runtype_opt} \'' \
                      f'chmod {self._spec_config["chmod"]} "{self._dest_dir}/{self._dest_filename}"' \
                      f'\' {self._relabel_opt}']
            if 'chown' in self._spec_config.keys():
                cmds += [f'virt-customize ' \
                      f'-a {self.disk_image_filepath} ' \
                      f'{cust_runtype_opt} \'' \
                      f'chown {self._spec_config["chown"]} "{self._dest_dir}/{self._dest_filename}"' \
                      f'\' {self._relabel_opt}']
            for cmd in cmds:
                self._last_result = runCmd(cmd)
                if not self._last_result:
                    return False
            return True
        return True
