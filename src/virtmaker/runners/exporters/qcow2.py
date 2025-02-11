import os
import shutil

from virtmaker import config

from virtmaker.runners.exporters import Exporter
from virtmaker.utils.cmd import runCmd
from virtmaker.utils.qemu import qemu_img_list_snapshots
from virtmaker.utils.schema import getValidatedData


class QCOW2(Exporter):
    _virt_sparsify_convert = 'qcow2'
    _required_commands = [['lz4c'], ['xz'], ['gzip'], ['mv'], ['pv'], ['virt-sparsify']]
    _compression_types = ['lz4', 'xz', 'gzip']
    #_compression_types = ['lz4']
    _compression_levels = range(1, 9)

    _spec_schema = {
        "title": f"export-{_virt_sparsify_convert}",
        "type": "object",
        "properties": {
            "path": {"type": "string", "format": "valid-posix-path-string"},
            "create_dir": {"type": "boolean", "default": False},
            "compress": {
                "type": "string",
                "enum": _compression_types
            },
            "level": {
                "type": "integer",
                "minimum": 1,
                "maximum": 9,
                "default": 1
            },
            "sparsify": {"type": "boolean", "default": False},
            "pre_script": {"type": "string"},
            "post_script": {"type": "string"}
        },
        "required": ["path"],
        "additionalProperties": False
    }

    @classmethod
    def validate(cls, unpopulated_spec):
        spec = getValidatedData(cls._spec_schema, unpopulated_spec)
        if not 'path' in spec.keys():
            raise Exception("'path' is a required field in qcow2")
        if not 'create_dir' in spec.keys() and not os.path.isdir(os.path.dirname(spec['path'])):
            raise Exception(f"missing directory {os.path.realpath(os.path.dirname(spec['path']))}, create it or use create_dir")
        if 'compress' in spec.keys():
            if not spec['compress'] in cls._compression_types:
                raise Exception(f"'compress' must be one of {cls._compression_types}")
            if 'level' in spec.keys():
                if not spec['level'] in cls._compression_levels:
                    raise Exception(f"'level' must be one of {cls._compression_levels}")

    def _isStepAlreadyRan(self):
        if config.force_export:
            return False
        snapshot_name = self._signature
        if not os.path.isfile(self._spec_config['path']):
            return False
        if not 'snapshots' in self._cache.keys():
            self._cache['snapshots'] = qemu_img_list_snapshots(self.disk_image_filepath)
        if snapshot_name in self._cache['snapshots']:
            return True
        else:
            return False

    def _run(self):
        if 'create_dir' in self._spec_config.keys():
            if self._spec_config['create_dir'] and not os.path.isdir(os.path.dirname(self._spec_config['path'])):
                os.makedirs(os.path.dirname(self._spec_config['path']))
        tmp_filepath = os.path.join(self._cache_dir, self._signature+'_in-progress')
        if 'sparsify' in self._spec_config.keys() and self._spec_config['sparsify'] or self._spec_config['sparsify'] == None:
            if 'compress' in self._spec_config.keys():
                cmds = [f'TMPDIR={self._cache_dir} virt-sparsify --convert={self._virt_sparsify_convert} "{self.disk_image_filepath}" "{tmp_filepath}"']
            else:
                cmds = [f'TMPDIR={self._cache_dir} virt-sparsify --compress --convert={self._virt_sparsify_convert} "{self.disk_image_filepath}" "{tmp_filepath}"']
        else:
            cmds = [f'TMPDIR={self._cache_dir} qemu-img convert -p -O {self._virt_sparsify_convert} "{self.disk_image_filepath}" "{tmp_filepath}"']
        if 'compress' in self._spec_config.keys():
            if self._spec_config['compress'] == 'lz4':
                level = 1
                if 'level' in self._spec_config.keys():
                    level = self._spec_config['level']
                if shutil.which('pv'):
                    cmds += [f"pv '{tmp_filepath}' | lz4c -{level} > '{tmp_filepath}.lz4'"]
                else:
                    cmds += [f"lz4c -{level} -c '{tmp_filepath}' > '{tmp_filepath}.lz4'"]
                cmds += [f"mv -f '{tmp_filepath}.lz4' '{tmp_filepath}'"]
            elif self._spec_config['compress'] == 'xz':
                if shutil.which('pv'):
                    cmds += [f"pv '{tmp_filepath}' | xz -{self._spec_config['level']} > '{tmp_filepath}.xz'"]
                else:
                    cmds += [f"xz -{self._spec_config['level']} -c '{tmp_filepath}' > '{tmp_filepath}.xz'"]
                cmds += [f"mv -f '{tmp_filepath}.xz' '{tmp_filepath}'"]
            elif self._spec_config['compress'] == 'gzip' or self._spec_config['compress'] == 'gz':
                if 'level' in self._spec_config.keys():
                    level = self._spec_config['level']
                if shutil.which('pv'):
                    cmds += [f"pv '{tmp_filepath}' | gzip -{level} > '{tmp_filepath}.gz'"]
                else:
                    cmds += [f"gzip -{level} -c '{tmp_filepath}' > '{tmp_filepath}.gz'"]
                cmds += [f"mv -f '{tmp_filepath}.gz' '{tmp_filepath}'"]
        for cmd in cmds:
            if not runCmd(cmd):
                raise Exception(f'failed executing {cmd}')
        if os.path.dirname(self._spec_config['path']) and not os.path.isdir(os.path.dirname(self._spec_config['path'])):
            os.makedirs(os.path.dirname(self._spec_config['path']))
        return shutil.move(tmp_filepath, self._spec_config['path'])

