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
import shutil

from virtmaker.utils.cmd import runCmd


def download_file(url, filepath, ignore_errors=False):
    if not os.path.isfile(filepath):
        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        cmd = f"wget '{url}' -O '{filepath}_in-progress'"
        retval = runCmd(cmd)
        if not retval and not ignore_errors:
            raise Exception(f"failed to download {url} to {filepath}")
        shutil.move(f'{filepath}_in-progress', filepath)
    return filepath
