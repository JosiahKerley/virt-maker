#!/usr/bin/env python3
# (c) 2015-2025, Josiah Kerley <josiahkerley@gmail.com>
#
# This file is part of Virt Maker.
#
# Virt Maker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Virt Maker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Virt Maker.  If not, see <http://www.gnu.org/licenses/>.

from virtmaker.runners import Runner
class Exporter(Runner):
    _tag = "export"
    _valid_keys = ['qcow2', 'raw']

    @classmethod
    def load(cls, spec_stanza, previous, image_name):
        for exporter_name in spec_stanza.keys():
            if exporter_name == "qcow2":
                from .qcow2 import QCOW2
                return QCOW2(spec_stanza['qcow2'], previous=previous, image_name=image_name)
            if exporter_name == "raw":
                from .raw import Raw
                return Raw(spec_stanza['raw'], previous=previous, image_name=image_name)
        raise Exception('No exporter class found')

    @classmethod
    def validate(cls, spec):
        key = list(spec.keys())[0]
        if not key in cls._valid_keys:
            raise Exception(f'{key} is not a valid {cls._tag}, choose from {cls._valid_keys}')

