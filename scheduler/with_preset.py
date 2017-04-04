import sys
import yaml

from app import schedule_with_seed, read_yaml_file
from constraints.position_constraints import *

if __name__ == "__main__":
    args = sys.argv[1:]
    volunteers_file = read_yaml_file(args[0])
    roles = read_yaml_file(args[1])
    preset = read_yaml_file(args[2])['schedule']

    slots = volunteers_file['slots']
    volunteer_profiles = volunteers_file['volunteers']

    position_constraints = [
        intro_briefer_constraint,
        commentator_constraint,
        refreshments_constraint,
        inspector_constraint,
        shepherd_constraint,
        roving_helper_constraint,
        scorer_constraint,
        tinker_coordinator_constraint,
        kit_return_constraint,
        helpdesk_volunteer_constraint
    ]

    best_schedule = schedule_with_seed(
        16145964,
        slots,
        roles,
        volunteer_profiles,
        position_constraints,
        default_schedule=preset)

    print(yaml.dump(best_schedule, default_flow_style=False))
