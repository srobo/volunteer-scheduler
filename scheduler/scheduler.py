import yaml

from utilities import read_yaml_file
from validator.constraints import *
from competition_scheduler import *


def hydrate_volunteers(volunteers, volunteer_profiles):
    return {v: volunteer_profiles[v] for v in volunteers}


def run():
    volunteers_file = read_yaml_file('tmp/volunteers.yml')
    role_constraints = read_yaml_file('tmp/constraints.yml')

    raw_slots = volunteers_file['slots']
    volunteer_profiles = volunteers_file['volunteers']

    people_constraints = {
        'intro-briefer': [can_speak, not_a_rookie],
        'commentator': [can_speak, not_a_rookie],
        'refreshments': [can_move_around],
        'robot-inspector': [understands_kit, not_a_rookie],
        'helpdesk-volunteer': [understands_kit],
        'shepherd': [can_move_around],
        'tinker-co-ordinator': [not_a_rookie],
        'roving-helper': [understands_kit, can_move_around],
        'match-scorer': [can_move_around],
        'kit-return': [understands_kit]
    }

    hydrated_volunteers_by_slot = {
        k: hydrate_volunteers(v, volunteer_profiles)
        for k, v in raw_slots.items()
    }

    competition_scheduler = CompetitionScheduler(
        people_constraints, role_constraints)

    schedule = competition_scheduler.generate_schedule(
        hydrated_volunteers_by_slot)

    print(yaml.dumps(schedule, default_flow_style=False))


if __name__ == "__main__":
    run()
