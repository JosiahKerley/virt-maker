import os
from virtmaker.runners.steps.run import Run


class GrubAppend(Run):
    _tag = "grub_append"

    @classmethod
    def _validate_step_spec(cls, spec):
        if not isinstance(spec, list):
            raise Exception(f"the step value for {cls._tag} is supposed to be a list, got {type(spec)}")
        for i in spec:
            if not isinstance(i, str):
                raise Exception(f"the step value for {cls._tag}: [] is supposed to be a string, got {type(spec)}")

    def _write_local_file(self):
        cmd = 'set -x\n'
        for append in self._spec_config:
            cmd += f"""
            sed -i '/^GRUB_CMDLINE_LINUX=.*/s/GRUB_CMDLINE_LINUX="/GRUB_CMDLINE_LINUX="{append} /g' /etc/default/grub
            """
        cmd += """
        cat /etc/default/grub
        find /boot -name grub.cfg | xargs -I {} grub2-mkconfig -o {}
        [[ -f /boot/grub/grub.cfg ]] && grub2-mkconfig -o /boot/grub/grub.cfg
        ls /boot/efi/EFI/ | xargs -I {} grub2-mkconfig -o /boot/efi/EFI/{}/grub.cfg 
        """
        local_file_path = os.path.join(self._cache_dir, self._signature)
        with open(local_file_path, 'w') as f:
            f.write(cmd)
        return local_file_path
