import sys
import yaml
from pydash.strings import kebab_case


AVAILABLE_SLOTS = [
    'saturday-0830-1100',
    'saturday-1100-1300',
    'saturday-1300-1500',
    'saturday-1500-1730',
    'sunday-0830-1100',
    'sunday-1100-1300',
    'sunday-1300-1500',
    'sunday-1500-1730'
]


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def read_file(file_name):
    with open(file_name, 'r') as f:
        return [line.strip().split(',') for line in (f.readlines())]


def to_constraint(v):
    return {
        'min': int(v[0]),
        'ideal': int(v[1]),
        'max': int(v[2])
    }


def to_role(line):
    constraints = [to_constraint(v) for v in chunks(line[1:], 3)]
    return dict(zip(AVAILABLE_SLOTS, constraints))


def get_roles_for_slot(roles, slot):
    return {role_name: roles[role_name][slot] for role_name in roles.keys()}


args = sys.argv[1:]

lines = read_file(args[0])

roles = {kebab_case(line[0]): to_role(line) for line in lines}
constraints = {slot: get_roles_for_slot(roles, slot) for slot in AVAILABLE_SLOTS}

print(yaml.dump(constraints, default_flow_style=False))
