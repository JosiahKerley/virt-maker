from virtmaker.runners.steps import Step
from virtmaker.utils.cmd import runCmd


class Sysprep(Step):
    _tag = "sysprep"
    _required_commands = [['virt-sysprep']]


    def _run(self):
        cmd = f'virt-sysprep -a {self.disk_image_filepath}'
        self._last_result = runCmd(cmd)
        return self._last_result

