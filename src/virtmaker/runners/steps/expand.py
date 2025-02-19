from virtmaker.runners.steps import Step
from virtmaker.utils.cmd import runCmd


class Expand(Step):
    _tag = "expand"
    _required_commands = [['virt-resize']]
    _spec_schema = {
        "title": "step-expand",
        "type": "object",
        "properties": {
            "partition": {"type": "integer", "default": 1},
            "size": {"type": "string", "default": "10G"}
        },
        "additionalProperties": False
    }

    @classmethod
    def _validate_step_spec(cls, unpopulated_spec):
        pass

    def _run(self):
        cmds = [
            f"virt-resize --expand /dev/sda{self.spec['partition']} {self.previous.image_path} {self.previous.image_path}.expandd",
            f"mv {self.previous.image_path}.expandd {self.previous.image_path}"
        ]
        for cmd in cmds:
            self._last_result = runCmd(cmd)
            if not self._last_result:
                return False
        return True
