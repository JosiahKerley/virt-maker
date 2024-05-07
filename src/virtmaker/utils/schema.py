import re
from jsonschema import Draft4Validator, validators, validate, ValidationError, FormatChecker

from virtmaker.utils.humans import fuzzyWordGuess, strings2diff


def extend_with_default(validator_class):
  validate_properties = validator_class.VALIDATORS["properties"]
  def set_defaults(validator, properties, instance, schema):
    for property, subschema in properties.items():
      if "default" in subschema:
        instance.setdefault(property, subschema["default"])
    for error in validate_properties(validator, properties, instance, schema):
      yield error
  return validators.extend(
    validator_class, {"properties": set_defaults},
  )

validator_with_defaults = extend_with_default(Draft4Validator)

@FormatChecker.cls_checks('data-size-format')
def check_size_format(instance):
    if isinstance(instance, str):
        return re.match(r'^[0-9]+(|K|M|G|T)$', instance) is not None
    return False

@FormatChecker.cls_checks('dev-path-format')
def check_dev_path_format(instance):
    if isinstance(instance, str):
        return re.match(r'^/dev/[a-z0-9]+$', instance) is not None
    return False

@FormatChecker.cls_checks('uri-to-qcow2-format')
def check_uri_to_qcow2_format(instance):
    if isinstance(instance, str):
        return (instance.startswith(('http://', 'https://', 'file://')) and
                (instance.endswith('.qcow2') or
                 instance.endswith('.qcow2.gz') or
                 instance.endswith('.qcow2.bz2') or
                 instance.endswith('.qcow2.xz') or
                 instance.endswith('.qcow2.lz') or
                 instance.endswith('.qcow2.lz4') or
                 instance.endswith('.qcow2.lzo')))
    return False

@FormatChecker.cls_checks('valid-posix-path-string')
def check_posix_path_string(instance):
    if isinstance(instance, str):
        return re.match(r'^[a-zA-Z0-9_/\.-]+$', instance) is not None
    return False


# def getValidatedData(schema, data):
#     try:
#         assert isinstance(data, dict)
#     except:
#         raise Exception(f"Data is not a dictionary, got: {data}")
#     try:
#         validator = validator_with_defaults(schema, format_checker=FormatChecker())
#         for error in validator.iter_errors(data):
#             print(f"Validation Error: {error.message}")
#             print(f"Failed data: {error.instance}")
#             print(f"Error in schema path: {'->'.join(error.absolute_schema_path)}")
#             raise error
#     except ValidationError as e:
#         raise e
#     return data


def getValidatedData(schema, data):
    try:
        assert isinstance(data, dict)
    except:
        raise Exception(f"Data is not a dictionary, got: {data}")
    try:
        validator = validator_with_defaults(schema, format_checker=FormatChecker())
        for error in validator.iter_errors(data):
            print(f"Validation Error: {error.message}")
            print(f"Failed data: {error.instance}")
            print(f"Error in schema path: {'->'.join(error.absolute_schema_path)}")
            raise error
    except ValidationError as e:
        if e.args[0].startswith('Additional properties are not allowed'):
            canidate = e.args[0].split('(')[1].split(')')[0]
            list_of_words_between_single_quotes = re.findall(r"'(.*?)'", canidate)
            schema_keys = schema['properties'].keys()
            suggestion_message_template = "Did you mean {0}?"
            suggestions = [options[0][0] for options in [fuzzyWordGuess(word, schema_keys)
                                                         for word in list_of_words_between_single_quotes]]
            e.message += '\n\n'
            for word, suggestion in zip(list_of_words_between_single_quotes, suggestions):
                e.message += f"'{word}' is not a valid property. Did you mean, '{suggestion}'?\n{strings2diff(word, suggestion, indent=1)}\n\n"
        raise e
    return data
