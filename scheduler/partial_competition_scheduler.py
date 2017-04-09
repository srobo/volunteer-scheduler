from scheduler.jobs_board import JobsBoard
from scheduler.match_maker import MatchMaker
from scheduler.partial_slot_scheduler import PartialSlotScheduler
from scheduler.competition_scheduler import expand_roles


class PartialCompetitionScheduler:
    def __init__(self, people_constraints, role_constraints):
        self.people_constraints = people_constraints
        self.role_constraints = {
            slot: expand_roles(roles)
            for slot, roles in role_constraints.items()
        }

    def generate_slot(self, slot, volunteers, roles, partial_schedule):
        jobs = JobsBoard(*roles)
        matchmaker = MatchMaker(volunteers, self.people_constraints)
        slot_scheduler = PartialSlotScheduler(jobs, matchmaker)
        try:
            return slot_scheduler.generate_schedule(partial_schedule)
        except Exception as ex:
            print("Exception in slot [{}]".format(slot))
            raise ex

    def generate_schedule(self, volunteers_by_slot, partial_schedule):
        return {
            slot: self.generate_slot(
                slot,
                volunteers_by_slot[slot],
                self.role_constraints[slot],
                partial_schedule[slot]
            ) for slot, volunteers in volunteers_by_slot.items()}
