from virtmaker.runners.steps import Step
from virtmaker.utils.cmd import runCmd


class VirtCustomize(Step):
    _required_commands = [['virt-customize']]
    _relabel_opt = '--no-selinux-relabel'

    def _getVirtCustomizeArgs(self):
        return [NotImplemented]

    def _run(self):
        cmd = f'virt-customize ' \
              f'-a {self.disk_image_filepath} ' \
              f'{" ".join(self._getVirtCustomizeArgs())} ' \
              f'{self._relabel_opt}'
        self._last_result = runCmd(cmd)
        return self._last_result
