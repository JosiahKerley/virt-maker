#!/usr/bin/env python3
# (c) 2015-2024, Josiah Kerley <josiahkerley@gmail.com>
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
import difflib
import textwrap

from fuzzywuzzy import process


def bytes2human(total_bytes: int) -> str:
    current_bytes = total_bytes/10
    for degree in ['b', 'k', 'm', 'g', 't', 'p']:
        if current_bytes < 1024:
            return f"{round(current_bytes, 2)}{degree}"
        current_bytes = current_bytes/1024
    raise Exception("How big is your stuff there bud?")

def fuzzyWordGuess(input_text, correct_texts, limit=1):
    return process.extract(input_text, correct_texts, limit=limit)

def strings2diff(str1, str2, indent=0):
    d = difflib.Differ()
    diff = d.compare(str1.splitlines(), str2.splitlines())
    return textwrap.indent('\n'.join(diff).replace('\n\n', '\n'), '\t'*indent)
