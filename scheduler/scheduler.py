from sys import maxsize
from random import Random
from scheduler.partial_competition_scheduler import *
from scheduler.judge import Judge
from scheduler.scorer import calculate_score
from scheduler.scheduling_exception import SchedulingException


def pick_best_schedule(champion, challenger):
    (_, champ_score) = champion
    (_, new_score) = challenger

    if new_score < champ_score:
        return challenger

    return champion


def get_best_schedule(
        competing_seeds,
        volunteers_by_slot,
        people_constraints,
        role_constraints,
        initial_schedule):
    def generate_schedule(seed):
        scheduler = PartialCompetitionScheduler(
            Random(seed),
            people_constraints,
            role_constraints)

        try:
            return calculate_score(
                scheduler.generate_schedule(
                    volunteers_by_slot,
                    initial_schedule
                ))
        except SchedulingException:
            return None

    judge = Judge(generate_schedule, pick_best_schedule)

    default_winner = ('NO_WINNER', maxsize)
    winning_seed, winning_score = judge.judge(
        competing_seeds, default_winner)

    if winning_seed == 'NO_WINNER':
        raise SchedulingException('Could not build an eligible schedule!')

    competition_scheduler = PartialCompetitionScheduler(
        Random(winning_seed),
        people_constraints,
        role_constraints)

    schedule = competition_scheduler.generate_schedule(
        volunteers_by_slot,
        initial_schedule)

    return {
        'schedule': schedule,
        'winning_seed': winning_seed,
        'winning_score': winning_score
    }
