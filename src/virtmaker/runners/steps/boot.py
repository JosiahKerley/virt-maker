import shutil

from virtmaker.runners.steps import Step
from virtmaker.utils.cmd import runCmd
from virtmaker.utils.schema import getValidatedData


class Boot(Step):
    _tag = "boot"
    _required_commands = [['qemu-system-x86_64', '/usr/libexec/qemu-kvm']]
    _qemu_system_options = {
        "display": ["gtk", "none", "sdl", "curses"],
        "cpu": "host",
        "cpus": 2,
        "memory": 2048
    }

    _spec_schema = {
        "title": "step-boot",
        "type": "object",
        "properties": {
            "display": {"type": "string", "enum": _qemu_system_options["display"]},
            "cpu": {"type": "string", "default": "host", "enum": ["host"]},
            "cpus": {"type": "number", "default": 2},
            "memory": {"type": "number", "default": 2048},
            "opts": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "additionalProperties": False
    }

    @classmethod
    def _validate_step_spec(cls, unpopulated_spec):
        spec = getValidatedData(cls._spec_schema, unpopulated_spec)
        if not isinstance(spec, None):
            if not isinstance(spec, dict):
                raise Exception(f"boot step must either have no value (using defaults) or values must be a dict, for {type(spec)}")
            if shutil.which('qemu-system-x86_64') and spec:
                if 'display' in spec.keys() and not spec['display'] in cls._qemu_system_options:
                    raise Exception(f"display must be one of {cls._qemu_system_options}, not {spec['display']}")
                if 'cpu' in spec.keys() and not isinstance(spec['cpu'], str):
                    raise Exception(f"cpu must be a string, not {spec['cpu']}")
                if 'cpus' in spec.keys() and not spec['cpus'].isnumeric():
                    raise Exception(f"cpus must be numeric, not {spec['cpus']}")
                if 'memory' in spec.keys() and not spec['memory'].isnumeric():
                    raise Exception(f"memory must be numeric, not {spec['memory']}")
                if 'opts' in spec.keys() and not isinstance(spec['opts'], list):
                    raise Exception(f"opts must be a nested list of strings, not {spec['opts']}")
                    for opt in spec['opts']:
                        if not isinstance(opt, list):
                            raise Exception(f"opt items must be a list of strings, not {type(opt)}")
                        for _ in opt:
                            if not isinstance(_, str):
                                raise Exception(f"opt item entries mist be strings, not, not {type(_)}")

    def _run(self):
        if shutil.which('qemu-system-x86_64'):
            cmd = f'qemu-system-x86_64 {self.disk_image_filepath}'
            if self._spec_config and 'display' in self._spec_config.keys():
                cmd += f" -display {self._spec_config['display']}"
            if self._spec_config and 'cpu' in self._spec_config.keys():
              cmd += f" -cpu {self._spec_config['cpu']}"
            else:
                cmd += f" -cpu host"
            if self._spec_config and 'cpus' in self._spec_config.keys():
              cmd += f" -smp {self._spec_config['cpus']}"
            else:
                cmd += f" -smp {self._qemu_system_options['cpus']}"
            if self._spec_config and 'memory' in self._spec_config.keys():
                cmd += f" -m {self._spec_config['memory']}"
            else:
                cmd += f" -m {self._qemu_system_options['memory']}"
        elif shutil.which('/usr/libexec/qemu-kvm'):
            cmd = f'/usr/libexec/qemu-kvm {self.disk_image_filepath}'
            if self._spec_config and 'cpu' in self._spec_config.keys():
              cmd += f" -cpu {self._spec_config['cpu']}"
            else:
                cmd += f" -cpu host"
            if self._spec_config and 'cpus' in self._spec_config.keys():
              cmd += f" -smp {self._spec_config['cpus']}"
            else:
                cmd += f" -smp {self._qemu_system_options['cpus']}"
            if self._spec_config and 'memory' in self._spec_config.keys():
                cmd += f" -m {self._spec_config['memory']}"
            else:
                cmd += f" -m {self._qemu_system_options['memory']}"
            if self._spec_config and 'opts' in self._spec_config.keys():
                for opt in  self._spec_config['opts']:
                    for _ in opt:
                        cmd += " "+_
        self._last_result = runCmd(cmd)
        return self._last_result
