import random
import yaml

def sample(l):
    return random.sample(l, len(l))

def merge_dicts(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


def read_yaml_file(file_name):
    with open(file_name) as f:
        return yaml.load(f.read())
