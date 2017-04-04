import sys
import yaml
import random
from collections import Counter

from scheduling_exception import SchedulingException
from constraints.position_constraints import *
from constraints.constraint import Verdict
from role_selector import RoleSelector


def read_yaml_file(file_name):
    with open(file_name) as f:
        return yaml.load(f.read())


def get_volunteer_schedules(schedule):
    volunteer_schedules = {}
    for slot, assignments in schedule.items():
        for name, role in assignments.items():
            if name not in volunteer_schedules:
                volunteer_schedules[name] = {}

            volunteer_schedules[name][slot] = role

    return volunteer_schedules


def calculate_score(schedule):
    score = 0
    previous_slot = None

    for slot, assignments in schedule.items():
        for name, role in assignments.items():
            if previous_slot is not None:
                if name in schedule[previous_slot] and schedule[previous_slot][name] == role:
                    score += 1

        previous_slot = slot

    for name, assignments in get_volunteer_schedules(schedule).items():
        role_counter = Counter()

        for role in assignments.values():
            role_counter[role] += 1

        for role, count in role_counter.items():
            score += max(0, count - 2)

    return score


def is_suitable_role(volunteer, role, constraints):
    return evaluate_role_constraints(
        volunteer,
        role,
        *constraints) == Verdict.OK


def generate_schedule(slots, roles, volunteer_profiles, position_constraints, default_schedule={}):
    schedule = default_schedule

    for slot, volunteers in slots.items():
        available_roles = roles[slot]
        role_selector = RoleSelector(available_roles)
        constraints = position_constraints

        schedule[slot] = schedule.get(slot, {
            "rspanton": "competition-event-coordinator",
            "rbarlow": "competition-team-support-coordinator",
            "sbedford": "competition-team-coordinator",
            "tscarsbrook": "competition-health-and-safety-coordinator",
            "jthompson": "volunteer-coordinator",
            "plaw": "competition-software-coordinator",
            "tleese": "head-match-scorer",
            "pdavies": "head-shepherd"
        })

        if role_selector.is_role_needed('intro-briefer'):
            schedule[slot]['rspanton'] = 'intro-briefer'

        if role_selector.is_role_needed('tinker-co-ordinator'):
            schedule[slot]['jhoward'] = 'tinker-co-ordinator'

        if slot == 'saturday-0830-1100':
            schedule[slot]['abarrettsprot'] = 'robot-inspector'
            schedule[slot]['jgough'] = 'robot-inspector'

        if slot == 'sunday-0830-1100':
            schedule[slot]['jgough'] = 'robot-inspector'

        if slot in ['sunday-0830-1100', 'sunday-1100-1300', 'sunday-1300-1500', 'sunday-1500-1730']:
            schedule[slot]['gpayne'] = 'commentator'

        if slot in ['sunday-0830-1100', 'sunday-1100-1300', 'sunday-1300-1500']:
            schedule[slot]['senglish'] = 'commentator'

        if slot == 'sunday-1500-1730':
            schedule[slot]['senglish'] = 'arena-changeroverer'

        if slot == 'sunday-1500-1730':
            constraints.append(no_rookie_match_scorers_constraint)

        # Remove manually filled roles from available role selection
        for role in schedule.get(slot, {}).values():
            role_selector.fill_role(role)

        for volunteer in schedule.get(slot, {}).keys():
            if volunteer in volunteers:
                del volunteers[volunteers.index(volunteer)]

        required_number_of_volunteers = role_selector.get_minimum_number_of_volunteers()
        if required_number_of_volunteers > len(volunteers):
            raise SchedulingException("Not enough volunteers [{}] to run slot [{}] [{}]".format(
                len(volunteers),
                slot,
                required_number_of_volunteers))

        randomised_volunteers = random.sample(volunteers, len(volunteers))
        for name in randomised_volunteers:
            if name in schedule[slot]:
                # volunteer is busy in a pre-defined role
                continue

            volunteer = volunteer_profiles[name]
            assignment = role_selector.select_role(
                volunteer,
                (lambda v, r: is_suitable_role(v, r, constraints)))

            if assignment is None:
                raise SchedulingException("CANNOT STAFF VOLUNTEER {} IN {}".format(name, slot))
            else:
                schedule[slot][name] = assignment

        if role_selector.any_necessary_roles_unfilled():
            raise SchedulingException("SOME NECESSARY ROLES ARE UNFILLED IN SLOT [{}]: [{}], SLOT [{}]".format(
                slot,
                role_selector.remaining_necessary_roles(),
                schedule[slot]))

    score = calculate_score(schedule)
    return {'score': score, 'schedule': schedule}


def schedule_with_seed(seed, slots, roles, volunteer_profiles, position_constraints, default_schedule={}):
    random.seed(seed)
    try:
        schedule = generate_schedule(
            slots,
            roles,
            volunteer_profiles,
            position_constraints,
            default_schedule)

        return {
            'seed': seed,
            **schedule
        }
    except SchedulingException as ex:
        print("Seed [{}] - {}".format(seed, ex), file=sys.stderr)
        return {
            'score': 99999999999
        }


def pick_best_schedule(a, b):
    if a['score'] <= b['score']:
        return a
    return b

# if __name__ == "__main__":
#     args = sys.argv[1:]
#     volunteers_file = read_yaml_file(args[0])
#     roles = read_yaml_file(args[1])
#
#     slots = volunteers_file['slots']
#     volunteer_profiles = volunteers_file['volunteers']
#
#     position_constraints = [
#         intro_briefer_constraint,
#         commentator_constraint,
#         refreshments_constraint,
#         inspector_constraint,
#         shepherd_constraint,
#         roving_helper_constraint,
#         scorer_constraint,
#         tinker_coordinator_constraint,
#         kit_return_constraint,
#         helpdesk_volunteer_constraint
#     ]
#
#     seeds = [random.randint(-100000000, 100000000) for r in range(3000)]
#     schedules = [schedule_with_seed(
#         seed,
#         slots,
#         roles,
#         volunteer_profiles,
#         position_constraints) for seed in seeds]
#
#     best_schedule = reduce(pick_best_schedule, schedules, {
#         'score': 99999999999
#     })
#
#     print(yaml.dump(best_schedule, default_flow_style=False))
