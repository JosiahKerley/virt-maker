from virtmaker.runners import Runner

class Step(Runner):
    _tag = 'step'
    _valid_keys = ['run', 'firstboot', 'copy', 'install', 'hostname', 'ssh_keygen', 'selinux', 'boot', 'grub_append',
                   'local_run', 'sysprep', 'inject_virtio_win', 'inject_qemu_ga', 'rootpass']

    @classmethod
    def load(cls, spec_stanza, previous=None, image_name=None):
        for step_name in spec_stanza.keys():
            if step_name == "run":
                from .run import Run
                return Run(spec_stanza['run'], previous=previous, image_name=image_name)
            if step_name == "firstboot":
                from .firstboot import Firstboot
                return Firstboot(spec_stanza['firstboot'], previous=previous, image_name=image_name)
            if step_name == "copy":
                from .copy import Copy
                return Copy(spec_stanza['copy'], previous=previous, image_name=image_name)
            if step_name == "install":
                from .install import Install
                return Install(spec_stanza['install'], previous=previous, image_name=image_name)
            if step_name == "hostname":
                from .hostname import Hostname
                return Hostname(spec_stanza['hostname'], previous=previous, image_name=image_name)
            if step_name == "ssh_keygen":
                from .ssh_keygen import SshKeygen
                return SshKeygen(spec_stanza['ssh_keygen'], previous=previous, image_name=image_name)
            if step_name == "selinux":
                from .selinux import SELinux
                return SELinux(spec_stanza['selinux'], previous=previous, image_name=image_name)
            if step_name == "boot":
                from .boot import Boot
                return Boot(spec_stanza['boot'], previous=previous, image_name=image_name)
            if step_name == "grub_append":
                from .grub_append import GrubAppend
                return GrubAppend(spec_stanza['grub_append'], previous=previous, image_name=image_name)
            if step_name == "local_run":
                from .local_run import LocalRun
                return LocalRun(spec_stanza['local_run'], previous=previous, image_name=image_name)
            if step_name == "sysprep":
                from .sysprep import Sysprep
                return Sysprep(spec_stanza['sysprep'], previous=previous, image_name=image_name)
            if step_name == "inject_virtio_win":
                from .inject_virtio_win import InjectVirtIOWin
                return InjectVirtIOWin(spec_stanza['inject_virtio_win'], previous=previous, image_name=image_name)
            if step_name == "inject_qemu_ga":
                from .inject_qemu_ga import InjectQEMUGuestAgent
                return InjectQEMUGuestAgent(spec_stanza['inject_qemu_ga'], previous=previous, image_name=image_name)
            if step_name == "rootpass":
                from .rootpass import RootPass
                return RootPass(spec_stanza['rootpass'], previous=previous, image_name=image_name)
            raise Exception(f'No step class found for {step_name}')

    @classmethod
    def _validate_step_spec(cls, spec):
        pass

    @classmethod
    def validate(cls, spec):
        try:
            key = list(spec.keys())[0]
        except:
            raise Exception(f"failed when trying to real the keys of {spec}")
        if not key in cls._valid_keys:
            raise Exception(f'{key} is not a valid {cls._tag}, choose from {cls._valid_keys}')
        cls._validate_step_spec(spec)

