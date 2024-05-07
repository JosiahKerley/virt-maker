import json
import yaml

def is_object_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

def to_pretty_yaml(obj):
    ## TODO: grosss, I'm doing this for now until I can figure out how to make the dumper stop using anchors and aliases
    obj = from_json(to_pretty_json(obj))
    return yaml.dump(obj, default_flow_style=False, allow_unicode=True)

def to_pretty_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True)

def from_yaml(yaml_str):
    return yaml.safe_load(yaml_str)

def from_json(json_str):
    return json.loads(json_str)
