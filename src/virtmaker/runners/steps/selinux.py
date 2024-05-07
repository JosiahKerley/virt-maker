import os
from virtmaker.runners.steps.run import Run


class SELinux(Run):
    _tag = "selinux"
    _se_modes = ['enforcing', 'disabled', 'permissive', 'relabel']

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, str):
            raise Exception(f"the step value for {cls._tag} is supposed to be a string, got {type(spec)}")
        if spec in cls._se_modes:
            raise Exception(f"the step value for {cls._tag} must be one of {cls._se_modes}")

    def _write_local_file(self):
        if self._spec_config == 'relabel':
            self._virt_customize_first_arg = '--selinux-relabel'
            return ''
        else:
            cmd = f"sed -i 's/^SELINUX=.*$/SELINUX={self._spec_config}/' /etc/selinux/config"
            local_file_path = os.path.join(self._cache_dir, self._signature)
            with open(local_file_path, 'w') as f:
                f.write(cmd)
            return local_file_path
