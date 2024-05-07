from virtmaker.runners.steps.virtcustomize import VirtCustomize


class InjectVirtIOWin(VirtCustomize):
    _tag = "inject_virtio_win"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, str):
            raise Exception(f"the step value for {cls._tag} is supposed to be a string, got {type(spec)}")


    def _setup(self):
        return True

    def _getVirtCustomizeArgs(self):
        return ['--inject-virtio-win', self._spec_config]
