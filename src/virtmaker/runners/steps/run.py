import os
from virtmaker.runners.steps.virtcustomize import VirtCustomize


class Run(VirtCustomize):
    _tag = "run"
    _virt_customize_first_arg = '--run'

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, str):
            raise Exception(f"the step value for {cls._tag} is supposed to be a string, got {type(spec)}")

    def _setup(self):
        return True

    def _getVirtCustomizeArgs(self):
        return [self._virt_customize_first_arg, self._write_local_file()]

    def _write_local_file(self):
        local_file_path = os.path.join(self._cache_dir, self._signature)
        with open(local_file_path, 'w') as f:
            f.write(self._spec_config)
        return local_file_path

    def cleanup(self):
        local_file_path = os.path.join(self._cache_dir, self._signature)
        if os.path.isfile(local_file_path):
            os.remove(local_file_path)
        return True
