import os
from virtmaker.runners.steps.run import Run
from virtmaker.utils.cli import ShellPrinter


class SshKeygen(Run):
    _tag = "ssh_keygen"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, str) or not isinstance(spec, None):
            raise Exception(f"the step value for {cls._tag} is supposed to be a string or None, got {type(spec)}")

    def _write_local_file(self):
        if not self._spec_config:
            user = 'root'
        else:
            user = self._spec_config
        cmd = f'''
        su - {user} -c 'yes | ssh-keygen -b 2048 -t rsa -f `realpath ~`/.ssh/id_rsa -q -N ""'
        '''
        with ShellPrinter(tag="key", verbosity=4, tag_color='white') as cmd_print:
            cmd_print(cmd)
        local_file_path = os.path.join(self._cache_dir, self._signature)
        with open(local_file_path, 'w') as f:
            f.write(cmd)
        return local_file_path
