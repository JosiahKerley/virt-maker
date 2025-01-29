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

import os
import json
from colorama import Fore, Style

from virtmaker import config
from virtmaker.utils.serialization import is_object_serializable


class ShellPrinter:
    def __init__(self, tag: str, tag_color: str = 'blue', slug: str = None,
                 max_width: int = 6, verbosity: int = 0):
        self._slug = slug
        self._tag = tag
        self._tag_color = tag_color
        self._max_width = max_width
        self._verbosity = verbosity

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs):
        try:
            if config.verbosity < self._verbosity:
                return None
            if self._tag_color == 'blue':
                color = Fore.BLUE
            elif self._tag_color == 'white':
                color = Fore.WHITE
            elif self._tag_color == 'red':
                color = Fore.RED
            line = args[0]
            if not line:
                line = ''
            try:
                columns = os.get_terminal_size().columns - 9
            except:
                try:
                    columns = int(os.environ['COLUMNS']) - 9
                except:
                    columns = 120
            columns = columns - (self._max_width + 4)
            if len(self._tag) < self._max_width:
                lpad = len(self._tag) + 1
                rpad = self._max_width - lpad
                trunc_tag = str(self._tag).rjust(lpad).upper() + " " * rpad
            else:
                trunc_tag = str(self._tag)[:6].ljust(6).upper()
            if config.verbosity < 2:
                trunc_msg = '\\n'.join(str(line).splitlines())
                if self._slug:
                    trunc_msg = f'{self._slug}: ' + trunc_msg
                else:
                    if config.template_file:
                        trunc_msg = f'{config.template_file}: ' + trunc_msg
                if len(trunc_msg) >= columns:
                    column_center = int((columns / 2) - 2)
                    trunc_left = trunc_msg[:column_center]
                    trunc_right = trunc_msg[::-1][:column_center][::-1]
                    trunc_msg = f'{trunc_left} ... {trunc_right}'
                msg = f'[{color + trunc_tag + Style.RESET_ALL}] {trunc_msg}'
            else:
                pretty_msg = str(line)
                if isinstance(line, dict) or isinstance(line, list):
                    pretty_msg = json.dumps(line, indent=2)
                msg = f'\n[{color + self._tag + Style.RESET_ALL}]\n{pretty_msg}'
            # print(msg, end="\r")
            print(msg)
        except Exception as e:
            print(e)
            pass


def get_runner_info(runner_type: str, verbosity: int = 0):
    import pkgutil
    import inspect
    import virtmaker.runners.steps as steps
    import virtmaker.runners.importers as importers
    import virtmaker.runners.exporters as exporters
    if runner_type == 'steps':
        runner_type = steps
    elif runner_type == 'importers':
        runner_type = importers
    elif runner_type == 'exporters':
        runner_type = exporters
    if verbosity > 0:
        runner_info = {}
        for loader, module_name, is_pkg in pkgutil.walk_packages(runner_type.__path__):
            runner_info[module_name] = {}
            for name, obj in inspect.getmembers(loader.find_module(module_name).load_module(module_name)):
                for info_key in ['_spec_schema', '_spec_example', '_required_commands']:
                    if hasattr(obj, info_key):
                        if is_object_serializable(getattr(obj, info_key)):
                            the_info = getattr(obj, info_key)
                            if info_key == '_required_commands':
                                the_info = [' or '.join(x) for x in the_info]
                            runner_info[module_name][info_key.lstrip('_')
                            .rstrip('_')
                            .replace('_', ' ')
                            .title()] = the_info
    else:
        runner_info = [module_name for loader, module_name, is_pkg in pkgutil.walk_packages(runner_type.__path__)]
    return runner_info
