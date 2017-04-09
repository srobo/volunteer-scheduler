import yaml
from copy import deepcopy
from random import randint

from scheduler.utilities import read_yaml_file, deep_merge
from scheduler.validator.constraints import *
from scheduler.scheduler import get_best_schedule


def hydrate_volunteers(volunteers, volunteer_profiles):
    return {v: volunteer_profiles[v] for v in volunteers}


def expand_permanent_roles_into_schedule(available_slots, permanent_roles):
    return {slot: deepcopy(permanent_roles) for slot in available_slots}


def build_initial_schedule(available_slots, permanent_roles, tentative_schedule):
    return deep_merge({}, expand_permanent_roles_into_schedule(
        available_slots, permanent_roles
    ), tentative_schedule)


def run():
    volunteers = read_yaml_file('tmp/volunteers.yml')
    availability = read_yaml_file('tmp/availability.yml')
    role_constraints = read_yaml_file('tmp/role_constraints.yml')
    permanent_roles = read_yaml_file('tmp/permanent_roles.yml')
    tentative_schedule = read_yaml_file('tmp/tentative_schedule.yml')

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

    available_slots = availability.keys()

    initial_schedule = build_initial_schedule(
        available_slots,
        permanent_roles,
        tentative_schedule)

    hydrated_volunteers_by_slot = {
        k: hydrate_volunteers(v, volunteers)
        for k, v in availability.items()
    }

    competing_seeds = [randint(-100000000, 100000000)
                       for _ in range(50000)]

    result = get_best_schedule(
        competing_seeds,
        hydrated_volunteers_by_slot,
        people_constraints,
        role_constraints,
        initial_schedule)

    print(yaml.dump(result, default_flow_style=False))


if __name__ == "__main__":
    run()
