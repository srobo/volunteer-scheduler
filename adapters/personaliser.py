import sys
import yaml


def read_yaml_file(file_name):
    with open(file_name) as f:
        return yaml.load(f.read())


args = sys.argv[1:]
schedule = read_yaml_file(args[0])['schedule']
volunteer_schedules = {}

for slot, assignments in schedule.items():
    for name, role in assignments.items():
        if name not in volunteer_schedules:
            volunteer_schedules[name] = {}

        volunteer_schedules[name][slot] = role

print(yaml.dump(volunteer_schedules, default_flow_style=False))
