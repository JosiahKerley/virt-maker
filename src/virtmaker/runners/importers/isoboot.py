import os.path
import shutil

from virtmaker import config
from virtmaker.runners.importers import Importer
from virtmaker.utils.cmd import runCmd, runCmds, runQemuCmdVncKeystrokes
from virtmaker.utils.schema import getValidatedData


class ISOBoot(Importer):
    _warning_messages = ["ISOBOOT is experimental and may not work as expected.",
                         "The ISOBOOT api is still in development and is subject to change.",
                         "Please do not use ISOBOOT for production builds until the api has stabilized."]
    _tag = "isoboot"
    _required_commands = [['qemu-system-x86_64', '/usr/libexec/qemu-kvm'],
                          ['pv', 'cp'], ['mkfs.msdos'], ['mcopy'], ['qemu-img'], ['wget']]

    _spec_schema = {
        "title": "import-isoboot",
        "type": "object",
        "properties": {
            "isos": {
                "type": "array",
                "items": {"type": "string"}
            },
            "cores": {
                "type": ["integer"],
                "default": 2
            },
            "ram": {
                "type": ["integer"],
                "default": 2048
            },
            "size": {
                "type": "string",
                "format": "data-size-format",
                "default": "16G"
            },
            "floppies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": {"type": "string"}
                }
            },
            "keystrokes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "ocr": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": {"type": "array", "items": {"type": "string"}}
                            }
                        },
                        "blind": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    },
                    "minProperties": 1,
                    "maxProperties": 1,
                    "additionalProperties": False
                }
            },
            "delay_time": {"type": ["number", "null"]},
            "key_delay_time": {"type": ["number", "null"]},
            "timeout": {"type": ["number", "null"]},
            "extra_opts": {"type": "string"},
        },
        "required": ["isos"],
        "additionalProperties": False
    }

    @classmethod
    def validate(cls, unpopulated_spec):
        return getValidatedData(cls._spec_schema, unpopulated_spec)

    def _isStepAlreadyRan(self):
        if config.force_build:
            return False
        if os.path.isfile(self.disk_image_filepath):
            return True
        else:
            return False

    def _prep_file(self, url):
        iso_filename = url.split('/')[-1]
        iso_filepath = os.path.join(self._cache_dir, iso_filename)
        orig_iso_filepath = iso_filepath
        # ['http://', 'https://', 'ftp://', 'sftp://', 'file://']
        if shutil.which("pv"):
            stream_cmd = 'pv'
        else:
            stream_cmd = 'cat'
        if url.startswith('file://'):
            cmd = f"{stream_cmd} '/{url.lstrip('file://')}' > '{iso_filepath}_in-progress'"
        else:
            cmd = f"wget '{url}' -O '{iso_filepath}_in-progress'"
        if iso_filename.endswith('.gz'):
            iso_filepath = iso_filepath.rstrip('.gz')
            cmd += f" && {stream_cmd} '{orig_iso_filepath}_in-progress' | gunzip > '{iso_filepath}_in-progress'"
        elif iso_filename.endswith('.bz2') or iso_filename.endswith('.bz'):
            iso_filepath = iso_filepath.rstrip('.bz2').rstrip('.bz')
            cmd += f" && {stream_cmd} '{orig_iso_filepath}_in-progress' | bunzip2 > '{iso_filepath}_in-progress'"
        elif iso_filename.endswith('.lz') or iso_filename.endswith('.lzma') or iso_filename.endswith('.lz4'):
            iso_filepath = iso_filepath.rstrip('.lz').rstrip('.lzma').rstrip('.lz4')
            cmd += f" && {stream_cmd} '{orig_iso_filepath}_in-progress' | unlzma > '{iso_filepath}_in-progress'"
        elif iso_filename.endswith('.xz'):
            iso_filepath = iso_filepath.rstrip('.xz')
            cmd += f" && {stream_cmd} '{orig_iso_filepath}_in-progress' | unxz > '{iso_filepath}_in-progress'"
        if not os.path.isfile(iso_filepath):
            retval = runCmd(cmd)
            shutil.move(f'{iso_filepath}_in-progress', iso_filepath)
        else:
            retval = True
        return iso_filepath, retval

    def _setup(self):
        if not os.path.isfile(self.disk_image_filepath):
            qcow_path = os.path.join(self._cache_dir, f"{self.disk_image_filepath}_in-progress")
            if os.path.isfile(qcow_path):
                os.remove(qcow_path)
            return runCmd(f"qemu-img create -f qcow2 {qcow_path} {self._spec_config['size']}")
        return True

    def _run(self):
        # qcow_path = os.path.join(self._cache_dir, f"{self.disk_image_filepath}_in-progress")
        qcow_path = f"{self.disk_image_filepath}_in-progress"
        keystrokes = self._spec_config.get('keystrokes', None)
        delay_time = (self._spec_config.get('delay_time', None))
        key_delay_time = self._spec_config.get('key_delay_time', None)
        timeout = self._spec_config.get('timeout', 3600)
        extra_opts = self._spec_config.get('extra_opts', '')
        floppies = self._spec_config.get('floppies', [])
        isos = self._spec_config.get('isos')
        cmds = []
        opts = ''
        cp_floppy_cmds = []
        if len(floppies) > 0:
            cmds += [f"mkfs.msdos -C {self._cache_dir}/floppy{_}.img 1440"
                     for _ in range(len(floppies))]
            for idx, floppy in enumerate(floppies):
                floppyname = f'floppy{idx}.img'
                floppypath = os.path.realpath(os.path.join(self._cache_dir, floppyname))
                for floppy in floppies:
                    opts += f" -fda {floppypath} "
                for filename in floppy.keys():
                    filedir = os.path.join(self._cache_dir, f'floppy{idx}')
                    if os.path.isfile(floppypath):
                        os.remove(floppypath)
                    filepath = os.path.join(filedir, filename)
                    if not os.path.isdir(os.path.dirname(filepath)):
                        os.makedirs(os.path.dirname(filepath))
                    if os.path.isfile(floppy[filename]):
                        shutil.copy2(floppy[filename], filepath)
                    else:
                        with open(filepath, 'w') as f:
                            f.write(floppy[filename])
                    # cp_floppy_cmds.append(f"cd '{filedir}' ; mcopy -i {floppypath} {filename} ::/")
                    cmds.append(f"mcopy -i {floppypath} {filepath} ::/{filename}")
        for idx, iso in enumerate(isos):
            iso_filepath, retval = self._prep_file(iso)
            assert retval
            opts += f" -drive file={iso_filepath},if=ide,index={idx},media=cdrom "
        qemu_system_cmds = ["/usr/bin/qemu-system-x86_64", "/usr/libexec/qemu-kvm"]
        for cmd in qemu_system_cmds:
            if os.path.isfile(cmd):
                qemu_system_cmd = cmd
        if 'cpu' in self._spec_config.keys():
            cpu = self._spec_config['cpu']
        else:
            cpu = 'host'
        if 'cpus' in self._spec_config.keys():
            cpus = self._spec_config['cpus']
        else:
            cpus = 2
        if 'memory' in self._spec_config.keys():
            memory = self._spec_config['memory']
        else:
            memory = 2048
        qemu_cmd = f"{qemu_system_cmd} -enable-kvm -cpu {cpu} -smp {cpus} -m {memory} -drive file={qcow_path},if=virtio {opts} -boot order=cd {extra_opts}"
        assert runCmds(cmds)
        if not runQemuCmdVncKeystrokes(qemu_cmd, keystrokes=keystrokes, delay_time=delay_time,
                                       key_delay_time=key_delay_time, timeout=timeout):
            print(f"QEMU failed to build from {qcow_path}")
            self.die()
        shutil.move(qcow_path, self.disk_image_filepath)
        return retval
