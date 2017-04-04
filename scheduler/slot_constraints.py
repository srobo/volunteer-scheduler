import itertools


def are_volunteers_doing_anything_they_cannot_do(slot, volunteers):
    for name, role in slot.items():
        volunteer = volunteers[name]

        if role == 'commentator' and not volunteer['can_speak']:
            return False

        if role == 'intro-briefer' and volunteer['is_rookie']:
            return False

        if role == 'intro-briefer' and not volunteer['can_speak']:
            return False

        if role == 'refreshments' and not volunteer['can_move']:
            return False

        if role == 'commentator' and not volunteer['can_move']:
            return False

        if role == 'robot-inspector' and not volunteer['is_technical']:
            return False

    return True


def are_any_roles_under_or_overstaffed(slot, constraints):
    assigned_roles = slot.values()
    role_tally = {}

    for role in assigned_roles:
        if role in role_tally:
            role_tally[role] = role_tally[role] + 1
        else:
            role_tally[role] = 0

    print(constraints)
    for role, constraints in constraints.items():
        volunteer_count = role_tally.get(role, 0)
        print('Comparing role {}: minimum {}, maximum {}, assigned {}'.format(role, constraints['min'], constraints['max'], volunteer_count))
        if volunteer_count < constraints['min']:
            print('Comparing role {}: under minimum')
            return False
        elif volunteer_count > constraints['max']:
            print('Comparing role {}: over maximum'.format(role))
            return False

    return True


def are_any_volunteers_multitasking(slot):
    volunteers = list(itertools.chain.from_iterable(slot.values()))
    unique_volunteers = list(set(volunteers))

    return volunteers != unique_volunteers
