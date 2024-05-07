import os.path

from virtmaker import config
from virtmaker.runners.importers import Importer
from virtmaker.utils.cmd import runCmd
from virtmaker.utils.schema import getValidatedData


class VirtBuilder(Importer):
    _required_commands = [['virt-builder']]

    _spec_example = {
        "image": "fedora-33",
        "size": "16G"
    }

    _spec_schema = {
        "title": "import-virtbuilder",
        "type": "object",
        "properties": {
            "image": {"type": "string"},
            "size": {"type": "string"}
        },
        "required": ["image", "size"],
        "additionalProperties": False
    }

    @classmethod
    def validate(cls, unpopulated_spec):
        spec = getValidatedData(cls._spec_schema, unpopulated_spec)
        if not 'image' in spec.keys():
            raise Exception("'image' is a required field in virt-builder")
        if not 'size' in spec.keys():
            raise Exception("'size' is a required field in virt-builder")
        if not spec.keys['size'].isdigit():
            raise Exception("'size' must be a value, e.g., 16G")

    def _isStepAlreadyRan(self):
        if config.force_build:
            return False
        if os.path.isfile(self.disk_image_filepath):
            return True
        else:
            return False

    def _run(self):
        cmd = f"virt-builder {self._spec_config['image']} --format=qcow2 " \
              f"--size {self._spec_config['size']} " \
              f"--output '{self.disk_image_filepath}'"
        return runCmd(cmd)
