from constraints.constraint import Verdict
from functools import reduce


def evaluate_role_constraints(volunteer, role, *constraints):
    return reduce(
        lambda so_far, constraint: max(so_far, constraint(volunteer, role)),
        constraints,
        Verdict.OK)


def intro_briefer_constraint(volunteer, role):
    if role == 'intro-briefer':
        if volunteer['is_rookie'] or not volunteer['can_speak']:
            return Verdict.FAIL

    return Verdict.OK


def commentator_constraint(volunteer, role):
    if role == 'commentator':
        if volunteer['is_rookie'] or not volunteer['can_speak']:
            return Verdict.FAIL

    return Verdict.OK


def refreshments_constraint(volunteer, role):
    if role == 'refreshments' and not volunteer['can_move']:
            return Verdict.FAIL

    return Verdict.OK


def inspector_constraint(volunteer, role):
    if role == 'robot-inspector' and (volunteer['is_rookie'] or not volunteer['is_technical']):
        return Verdict.FAIL

    return Verdict.OK


def shepherd_constraint(volunteer, role):
    if role == 'shepherd' and not volunteer['can_move']:
        return Verdict.FAIL

    return Verdict.OK


def helpdesk_volunteer_constraint(volunteer, role):
    if role == 'helpdesk-volunteer':
        if not volunteer['is_technical']:
            return Verdict.FAIL

    return Verdict.OK


def roving_helper_constraint(volunteer, role):
    if role == 'roving-helper':
        if not (volunteer['is_technical'] and volunteer['can_move']):
            return Verdict.FAIL

    return Verdict.OK


def tinker_coordinator_constraint(volunteer, role):
    if role == 'tinker-co-ordinator' and volunteer['is_rookie']:
        return Verdict.FAIL

    return Verdict.OK


def scorer_constraint(volunteer, role):
    if role == 'match-scorer' and not volunteer['can_move']:
        return Verdict.FAIL

    return Verdict.OK


def kit_return_constraint(volunteer, role):
    if role == 'kit-return' and not volunteer['is_technical']:
        return Verdict.FAIL

    return Verdict.OK


def no_rookie_match_scorers_constraint(volunteer, role):
    if role == 'match-scorer' and volunteer['is_rookie']:
        return Verdict.FAIL

    return Verdict.OK
