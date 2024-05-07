import os.path
import shutil

from virtmaker import config
from virtmaker.runners.importers import Importer
from virtmaker.utils.cmd import runCmds
from virtmaker.utils.schema import getValidatedData


class Download(Importer):
    _required_commands = [['wget'], ['virt-resize'], ['cp', 'pv'], ['truncate']]

    _spec_schema = {
        "title": "import-download",
        "type": "object",
        "properties": {
            "url": {"type": "string", "format": "uri-to-qcow2-format"},
            "resize": {
                "type": "object",
                "properties": {
                    "expand": {"type": "string", "format": "dev-path-format", "required": True},
                    "size": {"type": "string", "format": "data-size-format", "required": True},
                },
            }
        },
        "required": ["url"],
        "additionalProperties": False
    }

    @classmethod
    def validate(cls, unpopulated_spec):
        spec = getValidatedData(cls._spec_schema, unpopulated_spec)
        if spec['url'].startswith('file://'):
            filepath = os.path.join('/', spec['url'].lstrip('file://'))
            if not os.path.isfile(filepath):
                raise Exception(f"cannot find file '{filepath}' locally")
        if not spec['url'].endsswith('.qcow2'):
            raise Exception(f"'url' must be a qcow2 image, got {spec['url']}")

    def _isStepAlreadyRan(self):
        if config.force_build:
            return False
        if os.path.isfile(self.disk_image_filepath):
            return True
        else:
            return False

    def _run(self):
        cleanup_files = [f'{self.disk_image_filepath}_in-progress']
        if self._spec_config['url'].startswith('file://'):
            stream_cmd = 'cat'
            if shutil.which("pv"):
                stream_cmd = 'pv'
            if self._spec_config['url'].endswith('.qcow2'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' > '{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.qcow2.xz'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' | xz -d | dd of='{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.qcow2.gz'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' | gunzip | dd of='{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.qcow2.bz2'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' | bunzip2 | dd of='{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.img'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' > '{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            elif self._spec_config['url'].endswith('.img.xz'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' | xz -d | dd of='{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            elif self._spec_config['url'].endswith('.img.gz'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' | gunzip | dd of='{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            elif self._spec_config['url'].endswith('.img.bz2'):
                cmds = [f"{stream_cmd} '/{self._spec_config['url'].lstrip('file://')}' | bunzip2 | dd of='{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            else:
                raise Exception(f"unsupported file extension for url '{self._spec_config['url']}'")
        else:
            if self._spec_config['url'].endswith('.qcow2'):
                cmds = [f"wget '{self._spec_config['url']}' -O '{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.qcow2.xz'):
                cmds = [f"wget '{self._spec_config['url']}' -O - | xz -d | dd of='{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.qcow2.gz'):
                cmds = [f"wget '{self._spec_config['url']}' -O - | gunzip | dd of='{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.qcow2.bz2'):
                cmds = [f"wget '{self._spec_config['url']}' -O - | bunzip2 | dd of='{self.disk_image_filepath}_in-progress'"]
            elif self._spec_config['url'].endswith('.img'):
                cmds = [f"wget '{self._spec_config['url']}' -O '{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            elif self._spec_config['url'].endswith('.img.xz'):
                cmds = [f"wget '{self._spec_config['url']}' -O - | xz -d | dd of='{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            elif self._spec_config['url'].endswith('.img.gz'):
                cmds = [f"wget '{self._spec_config['url']}' -O - | gunzip | dd of='{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            elif self._spec_config['url'].endswith('.img.bz2'):
                cmds = [f"wget '{self._spec_config['url']}' -O - | bunzip2 | dd of='{self.disk_image_filepath}.img_in-progress'",
                        f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.img_in-progress' '{self.disk_image_filepath}_in-progress'",
                        f"rm '{self.disk_image_filepath}.img_in-progress'"]
            else:
                raise Exception(f"unsupported file extension for url '{self._spec_config['url']}'")
        if 'resize' in self._spec_config.keys():
            cmds.append(f"truncate -r '{self.disk_image_filepath}_in-progress' '{self.disk_image_filepath}.raw'")
            cmds.append(f"truncate -s {self._spec_config['resize']['size']} '{self.disk_image_filepath}.raw'")
            cleanup_files.append(f'{self.disk_image_filepath}.raw')
            cmd = "virt-resize"
            for partition in self._spec_config['resize'].keys():
                operation = self._spec_config['resize'][partition]
                if partition == "expand":
                    cmd += f" --expand={operation}"
                elif partition == "size":
                    continue
                else:
                    cmd += f" --resize={partition}={operation}"
            cmd += f" '{self.disk_image_filepath}_in-progress' '{self.disk_image_filepath}.raw'"
            cmds.append(cmd)
            cmds.append(f"qemu-img convert -O qcow2 '{self.disk_image_filepath}.raw' '{self.disk_image_filepath}'")
        else:
            cmds.append(f"mv '{self.disk_image_filepath}_in-progress' '{self.disk_image_filepath}'")

        retval = runCmds(cmds)
        for filepath in cleanup_files:
            if os.path.isfile(filepath):
                os.remove(filepath)
        return retval
