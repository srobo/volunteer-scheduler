from random import Random, randint
import copy
import yaml
import sys
from scheduler.utilities import read_yaml_file, deep_merge
from scheduler.validator.constraints import *
from scheduler.partial_competition_scheduler import *
from scheduler.judge import Judge
from scheduler.scorer import calculate_score
from scheduler.scheduling_exception import SchedulingException


def hydrate_volunteers(volunteers, volunteer_profiles):
    return {v: volunteer_profiles[v] for v in volunteers}


def expand_permanent_roles_into_schedule(available_slots, permanent_roles):
    return {slot: copy.deepcopy(permanent_roles) for slot in available_slots}


def build_initial_schedule(available_slots, permanent_roles, tentative_schedule):
    return deep_merge({}, expand_permanent_roles_into_schedule(
        available_slots, permanent_roles
    ), tentative_schedule)


def pick_best_schedule(champion, challenger):
    (_, champ_score) = champion
    (_, new_score) = challenger

    if new_score < champ_score:
        return challenger

    return champion


def run():
    volunteers_file = read_yaml_file('tmp/volunteers.yml')
    role_constraints = read_yaml_file('tmp/constraints.yml')
    permanent_roles = read_yaml_file('tmp/permanent_roles.yml')
    tentative_schedule = read_yaml_file('tmp/tentative_schedule.yml')

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

    available_slots = raw_slots.keys()

    initial_schedule = build_initial_schedule(
        available_slots,
        permanent_roles,
        tentative_schedule)

    hydrated_volunteers_by_slot = {
        k: hydrate_volunteers(v, volunteer_profiles)
        for k, v in raw_slots.items()
    }

    competing_seeds = [randint(-100000000, 100000000)
                       for _ in range(50000)]

    def generate_schedule(seed):
        competition_scheduler = PartialCompetitionScheduler(
                Random(seed),
                people_constraints,
                role_constraints)

        try:
            schedule = competition_scheduler.generate_schedule(
                hydrated_volunteers_by_slot,
                initial_schedule)
            return calculate_score(schedule)
        except SchedulingException:
            return None

    judge = Judge(generate_schedule, pick_best_schedule)

    winning_seed, winning_score = judge.judge(
        competing_seeds, ('NO_WINNER', sys.maxsize))

    if winning_seed == 'NO_WINNER':
        raise SchedulingException('Could not build an eligible schedule!')

    competition_scheduler = PartialCompetitionScheduler(
        Random(winning_seed),
        people_constraints,
        role_constraints)

    schedule = competition_scheduler.generate_schedule(
        hydrated_volunteers_by_slot,
        initial_schedule)

    print(yaml.dump({
        'schedule': schedule,
        'winning_seed': winning_seed,
        'winning_score': winning_score
    }, default_flow_style=False))


if __name__ == "__main__":
    run()
