import yaml

def sample(random, l):
    return random.sample(l, len(l))


def deep_merge(first, *others):
    for other in others:
        for key, value in other.items():
            if not isinstance(value, dict):
                first[key] = value
            else:
                node = first.setdefault(key, {})
                deep_merge(node, value)

    return first


def read_yaml_file(file_name):
    with open(file_name) as f:
        return yaml.load(f.read())
