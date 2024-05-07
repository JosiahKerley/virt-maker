import os
from virtmaker.runners.steps.run import VirtCustomize


class RootPass(VirtCustomize):
    _tag = "rootpass"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, str):
            raise Exception(f"the step value for {cls._tag} is supposed to be a string, got {type(spec)}")

    def _setup(self):
        return True

    def _getVirtCustomizeArgs(self):
        return ['--password-crypto=sha512', '--root-password', self._spec_config]
