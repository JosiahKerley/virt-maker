import json
import yaml

def is_object_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

## TODO: grosss, I'm doing this for now until I can figure out how to make the dumper stop using anchors and aliases
def to_pretty_yaml(obj):
    obj = from_json(to_pretty_json(obj))
    yaml_str = yaml.dump(obj, default_flow_style=False, allow_unicode=True)
    lines = yaml_str.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i > 0 and line and not line.startswith(' '):
            result.append('')
        result.append(line)
    return '\n'.join(result)

def to_pretty_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True)

def from_yaml(yaml_str):
    return yaml.safe_load(yaml_str)

def from_json(json_str):
    return json.loads(json_str)
