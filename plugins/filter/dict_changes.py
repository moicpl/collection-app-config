# Compare nested settings with their defaults, e.g. an app's whole config with
# the app's defaults, to keep only the settings that were changed.

DOCUMENTATION_DICT_CHANGES = """
name: dict_changes
short_description: The parts of a nested dict that differ from a base dict
positional: base
options:
  _input:
    type: dict
    required: true
  base:
    description: The dict to compare with, e.g. the defaults.
    type: dict
    required: true
"""


def dict_changes(value, base):
    """The keys of value whose values differ from base's, recursively: a nested
    dict keeps only its changed keys, other values (lists...) are kept whole."""
    changes = {}
    for key, item in value.items():
        if key not in base:
            changes[key] = item
        elif isinstance(item, dict) and isinstance(base[key], dict):
            nested = dict_changes(item, base[key])
            if nested:
                changes[key] = nested
        elif item != base[key]:
            changes[key] = item
    return changes


def dict_unknown_keys(value, base, prefix=""):
    """The dotted paths of the keys of value that base doesn't have."""
    unknown = []
    for key, item in value.items():
        path = prefix + str(key)
        if key not in base:
            unknown.append(path)
        elif isinstance(item, dict) and isinstance(base[key], dict):
            unknown.extend(dict_unknown_keys(item, base[key], path + "."))
    return unknown


class FilterModule:
    def filters(self):
        return {
            "dict_changes": dict_changes,
            "dict_unknown_keys": dict_unknown_keys,
        }
