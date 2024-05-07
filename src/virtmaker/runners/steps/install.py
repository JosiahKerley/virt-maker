from virtmaker.runners.steps.virtcustomize import VirtCustomize


class Install(VirtCustomize):
    _tag = "install"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, list):
            raise Exception("install needs to be defined as a list of package names")
        if spec == []:
            raise Exception("list of packages cannot be empty")
        for i in spec:
            if not isinstance(i, str):
                raise Exception("install items must be a string")

    def _setup(self):
        return True

    def _getVirtCustomizeArgs(self):
        return ['--install', ','.join(self._spec_config)]
