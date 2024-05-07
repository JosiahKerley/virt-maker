import ast
import json
import sys
from yaml import load
from jinja2 import Environment, BaseLoader
from virtmaker.template import filters
from virtmaker.utils.data import mergeBefore, mergeAfter

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def render(template_string, params):
    env = Environment(loader=BaseLoader)
    for _ in [_.replace('filter_', '') for _ in dir(filters) if _.startswith('filter_')]:
        env.globals[_] = getattr(filters, 'filter_' + _)
    return env.from_string(template_string).render(params)

def traverse(value, params):
    if isinstance(value, dict):
        for _ in value.copy().keys():
            new_key = render(_, params)
            value[new_key] = traverse(value[_], params)
            if not new_key == _:
                del value[_]
    elif isinstance(value, list):
        for idx, _ in enumerate(value):
            value[idx] = traverse(_, params)
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    elif isinstance(value, int):
        return value
    elif isinstance(value, bool):
        return str(value)
    elif value == None:
        return value
    else:
        try:
            while True:
                try:
                    value = traverse(ast.literal_eval(value), params)
                    break
                except:
                    new_value = render(value, params)
                    if new_value == value:
                        break
                    value = new_value
        except:
            print(f"{value} failed templating")
            # import json
            # print(json.dumps(params['autounattend_commands'], indent=2))
            sys.exit(1)
    return value

## TODO: This needs to handle more than just some local file
def load_template(uri):
    with open(uri) as f:
        return load(f, Loader=Loader)

def _handle_to_and_from(template):
    while 'from' in template.keys():
        from_template = load_template(template['from'])
        del template['from']
        template = mergeBefore(template, from_template)
    while 'to' in template.keys():
        from_template = load_template(template['to'])
        del template['to']
        template = mergeAfter(template, from_template)
    return template

def template2spec(template, param_overrides={}):
    while 'from' in template.keys() or 'to' in template.keys():
        template = _handle_to_and_from(template)
    if 'params' in template.keys():
        params = template['params']
    else:
        params = {}
    for p in param_overrides.keys():
        params[p] = param_overrides[p]
    template = traverse(template, params)

    ## Check if steps are in the template, and if so, merge any nested lists
    if 'steps' in template['spec'].keys():
        steps = []
        for step in template['spec']['steps']:
            if isinstance(step, list):
                steps = steps + step
            else:
                steps.append(step)
        template['spec']['steps'] = steps
    return template['spec']
