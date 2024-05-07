from virtmaker.runners import Runner


class Importer(Runner):
    ## TODO: needed?
    #_importer = None
    _tag = "import"
    _valid_keys = ['virt-builder', 'isoboot', 'download']

    @classmethod
    def load(cls, spec_stanza):
        for importer_name in spec_stanza.keys():
            if importer_name == "virt-builder":
                from .virtbuilder import VirtBuilder
                starting_hash = cls.generate_hash(spec_stanza['virt-builder'])
                return VirtBuilder(spec_stanza['virt-builder'], image_name=f"{starting_hash}.qcow2")
            elif importer_name == "isoboot":
                from .isoboot import ISOBoot
                starting_hash = cls.generate_hash(spec_stanza['isoboot'])
                return ISOBoot(spec_stanza['isoboot'], image_name=f"{starting_hash}.qcow2")
            elif importer_name == "download":
                from .download import Download
                starting_hash = cls.generate_hash(spec_stanza['download'])
                return Download(spec_stanza['download'], image_name=f"{starting_hash}.qcow2")
        raise Exception('No importer class found')

    @classmethod
    def validate(cls, spec):
        key = list(spec.keys())[0]
        if not key in cls._valid_keys:
            raise Exception(f'{key} is not a valid {cls._tag}, choose from {cls._valid_keys}')
