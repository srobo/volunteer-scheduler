from scheduler.jobs_board import JobsBoard
from scheduler.match_maker import MatchMaker
from scheduler.partial_slot_scheduler import PartialSlotScheduler
from scheduler.competition_scheduler import expand_roles
from scheduler.utilities import sample
from scheduler.scheduling_exception import SchedulingException


class PartialCompetitionScheduler:
    def __init__(self, random, people_constraints, role_constraints):
        self.random = random
        self.people_constraints = people_constraints
        self.role_constraints = {
            slot: expand_roles(roles)
            for slot, roles in role_constraints.items()
        }

    def shuffle(self, l):
        return sample(self.random, l)

    def generate_slot(self, slot, volunteers, roles, partial_schedule):
        min_roles, ideal_roles, max_roles = roles
        jobs = JobsBoard(
            self.shuffle(min_roles),
            self.shuffle(ideal_roles),
            self.shuffle(max_roles))
        matchmaker = MatchMaker(volunteers, self.people_constraints)
        slot_scheduler = PartialSlotScheduler(jobs, matchmaker)

        try:
            return slot_scheduler.generate_schedule(partial_schedule)
        except Exception as ex:
            raise SchedulingException("Exception in slot [{}]".format(slot), ex)

    def generate_schedule(self, volunteers_by_slot, partial_schedule):
        return {
            slot: self.generate_slot(
                slot,
                volunteers_by_slot[slot],
                self.role_constraints[slot],
                partial_schedule[slot]
            ) for slot, volunteers in volunteers_by_slot.items()}
