from collections import Counter


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
