from scheduler.slot_scheduler import SlotScheduler
from scheduler.utilities import deep_merge


class PartialSlotScheduler:
    def __init__(self, jobs, match_maker):
        self.jobs = jobs
        self.match_maker = match_maker

    def generate_schedule(self, partial_schedule):
        slot_scheduler = SlotScheduler(
            self.jobs,
            self.match_maker)

        for name, role in partial_schedule.items():
            self.match_maker.remove_volunteer(name)
            self.jobs.remove_role(role)

        return deep_merge(
            {},
            partial_schedule,
            slot_scheduler.generate_schedule())
