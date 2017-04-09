from scheduler.match_maker import MatchMaker
from scheduler.jobs_board import JobsBoard
from scheduler.slot_scheduler import SlotScheduler
from scheduler.scheduling_exception import SchedulingException


def expand_roles(available_roles):
    min = []
    ideal = []
    max = []

    for role, constraints in available_roles.items():
        minimum_count = constraints['min']
        ideal_count = constraints['ideal']
        maximum_count = constraints['max']

        for _ in range(minimum_count):
            min.append(role)
        for _ in range(ideal_count - minimum_count):
            ideal.append(role)
        for _ in range(maximum_count - (ideal_count + minimum_count)):
            max.append(role)

    return min, ideal, max


class CompetitionScheduler:
    def __init__(self, people_constraints, role_constraints):
        self.people_constraints = people_constraints
        self.role_constraints = {
            slot: expand_roles(roles)
            for slot, roles in role_constraints.items()
        }

    def generate_slot(self, volunteers, roles):
        jobs = JobsBoard(*roles)
        matchmaker = MatchMaker(volunteers, self.people_constraints)
        slot_scheduler = SlotScheduler(jobs, matchmaker)
        return slot_scheduler.generate_schedule()

    def generate_schedule(self, volunteers_by_slot):
        return {slot: self.generate_slot(volunteers_by_slot[slot], self.role_constraints[slot])
                for slot, volunteers in volunteers_by_slot.items()}