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


def mergeBefore(first: dict, second: dict) -> dict:
    new_dict = first.copy()
    for key in second.keys():
        if not key in first.keys():
            new_dict[key] = second[key]
        else:
            if isinstance(first[key], list):
                assert isinstance(second[key], list)
                new_dict[key] = second[key] + new_dict[key]
            elif isinstance(first[key], dict):
                new_dict[key] = mergeBefore(new_dict[key], second[key])
    return new_dict

def mergeAfter(first: dict, second: dict) -> dict:
    new_dict = first.copy()
    for key in second.keys():
        if not key in first.keys():
            new_dict[key] = second[key]
        else:
            if isinstance(first[key], list):
                assert isinstance(second[key], list)
                new_dict[key] += second[key]
            elif isinstance(first[key], dict):
                new_dict[key] = mergeAfter(new_dict[key], second[key])
            else:
                new_dict[key] = second[key]
    return new_dict

def extract_all_keys(input_dict):
    keys = []
    for key, value in input_dict.items():
        keys.append(key)
        if isinstance(value, dict):
            keys.extend(extract_all_keys(value))
    return set(keys)
