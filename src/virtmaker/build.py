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


import json

from virtmaker import config
from virtmaker.runners.exporters import Exporter
from virtmaker.runners.importers import Importer
from virtmaker.runners.steps import Step
from virtmaker.template import load_template, template2spec
from virtmaker.utils.cli import ShellPrinter


def build(filepath, build_params=[]):
    config.template_file = filepath
    with ShellPrinter(tag="file", verbosity=0, tag_color='red') as file_print:
        file_print('Starting')
        template = load_template(filepath)
        if not 'before' in template.keys() and not 'after' in template.keys() and not 'spec' in template.keys():
            raise Exception(f"Template {filepath} is missing a 'before', 'after', or 'spec' stanza., "
                            f"Got {template}")

        if 'before' in template.keys():
            for f in template['before']:
                build(f, build_params)
        if 'spec' in template.keys():
            with ShellPrinter(tag="spec", verbosity=3, tag_color='white') as spec_print:
                with ShellPrinter(tag="param", verbosity=4, tag_color='white') as param_print:
                    param_overrides = {}
                    if build_params:
                        for p in build_params:
                            key = p.split('=')[0]
                            value = '='.join(p.split('=')[1:])
                            ## TODO: Gross
                            try:
                                value = json.loads(value)
                            except:
                                print('This is gross, find this string in the code and fix it.')
                                pass
                            param_overrides[key] = value
                            param_print(json.dumps(param_overrides, indent=2))
                    if param_overrides:
                        spec = template2spec(template, param_overrides=param_overrides)
                    else:
                        spec = template2spec(template)
                spec_print(json.dumps(spec, indent=2))


            ## Validation
            Importer.validate(spec['import'])
            if 'steps' in spec.keys():
                for step_stanza in spec['steps']:
                    Step.validate(step_stanza)
            Exporter.validate(spec['export'])

            ## Build
            with Importer.load(spec['import']) as importer:
                retval, image_name, previous = importer.execute()
                assert retval is not False

            if 'steps' in spec.keys():
                for step_stanza in spec['steps']:
                    with Step.load(step_stanza, previous=previous, image_name=image_name) as step:
                        retval, image_name, previous = step.execute()
                        if retval == False:
                            raise Exception(f"Step failed: {step_stanza}")

            with Exporter.load(spec['export'], previous=previous, image_name=image_name) as exporter:
                retval, image_name, previous = exporter.execute()
                assert retval is not False

        if 'after' in template.keys():
            for f in template['after']:
                build(f, build_params)
