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
import inspect
import os
import sys
import shutil
import pkgutil
import argparse

import yaml

import virtmaker
from virtmaker import config
from virtmaker.build import build
from virtmaker.config import get_cache_dir
from virtmaker.utils.cli import get_runner_info
from virtmaker.utils.humans import bytes2human
from virtmaker.utils.serialization import to_pretty_yaml


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Actions')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-V', '--version', required=False, default=False, action='store_true', help='Show virt-maker version')

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("-f", "--file", required=True, dest='build_files', help='Path to template file(s)', nargs=argparse.ONE_OR_MORE)
    build_parser.add_argument("-p", "--param", required=False, dest='build_params', help='Set or override template parameter', nargs=argparse.ONE_OR_MORE)
    build_parser.add_argument("-F", "--force", required=False, default=False, action='store_true', dest="build_force", help='Force build from scratch')
    build_parser.add_argument("-X", "--force-export", required=False, default=False, action='store_true', dest="build_force_export", help='Force export to re-run')

    cache_parser = subparsers.add_parser("cache")
    cache_parser.add_argument('cache_operation', choices=('clean', 'usage'))
    cache_parser.add_argument("-H", "--human-readable", required=False, default=False, action='store_true', dest="cache_humanreadable", help='Output as human-readable values')

    runners_parser = subparsers.add_parser("runners")
    runners_parser.add_argument('runner_type', choices=('steps', 'importers', 'exporters'), help='Show the types of runners')

    args = parser.parse_args()
    if 'VERBOSE' in os.environ.keys():
        config.verbosity = int(os.environ['VERBOSE'])
    elif 'VERBOSITY' in os.environ.keys():
        config.verbosity = int(os.environ['VERBOSITY'])
    else:
        config.verbosity = args.verbose

    if 'version' in args and args.version:
        print(virtmaker.__version__)

    elif 'cache_operation' in args:
        os.chdir(get_cache_dir())
        current_usage = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
        if 'cache_humanreadable' in args:
            cache_size = bytes2human(current_usage)
        else:
            cache_size = current_usage
        if args.cache_operation == 'usage':
            print(cache_size)
        elif args.cache_operation == 'clean':
            shutil.rmtree(get_cache_dir())
            print(f"cleaned up {cache_size}")

    elif 'build_files' in args:
        config.force_build = args.build_force
        config.force_export = args.build_force_export
        for filepath in args.build_files:
            if not os.path.isfile(filepath):
                raise Exception(f"File {filepath} does not exist or is not a file")
            config.template_file = filepath
            build(filepath, args.build_params)

    elif 'runner_type' in args:
        print(to_pretty_yaml(get_runner_info(args.runner_type, verbosity=config.verbosity)))

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    cli()
