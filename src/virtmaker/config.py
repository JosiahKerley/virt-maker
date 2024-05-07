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

import os

if not any([_ for _ in os.environ if _ == 'LIBGUESTFS_BACKEND']):
    os.environ['LIBGUESTFS_BACKEND'] = 'direct'
verbosity = 0
force_build = False
force_export = False
_cache_dirs_parents = [
    'cache',
    '.cache',
    '../cache',
    '../.cache',
    '../../.cache',
    '../../../.cache',
    '../../../../.cache',
    '../../../../../.cache',
    '../../../../../../.cache',
    '../../../../../../../.cache',
    '../../../../../../../../.cache',
    os.path.join(os.path.expanduser('~'), 'cache'),
    os.path.join(os.path.expanduser('~'), '.cache'),
    '/var/lib/cache',
    '/var/lib/.cache',
    '/var/cache',
    '/var/.cache',
    '/tmp/cache',
    '/tmp/.cache',
    '/tmp',
]

template_file = None

def get_cache_dir():
    for cache_dir_parent in _cache_dirs_parents:
        cache_dir = os.path.join(cache_dir_parent, 'virt-maker')
        if os.path.isdir(cache_dir_parent):
            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir)
            return os.path.realpath(cache_dir)
    cache_dir = os.path.join('.cache', 'virt-maker')
    if os.path.isdir(cache_dir_parent):
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        return os.path.realpath(cache_dir)
