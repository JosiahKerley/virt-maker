from virtmaker.runners.steps import Step
from virtmaker.utils.cmd import runCmd


class LocalRun(Step):
    _required_commands = [['scp']]
    _tag = "local_run"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, str):
            raise Exception(f"the step value for {cls._tag} is supposed to be a string, got {type(spec)}")

    def _run(self):
        return runCmd(self._spec_config)

