from scheduler.slot_scheduler import SlotScheduler


class PartialSlotScheduler:
    def __init__(self, jobs, matchmaker):
        self.jobs = jobs
        self.matchmaker = matchmaker

    def generate_schedule(self, partial_schedule):
        slot_scheduler = SlotScheduler(
            self.jobs,
            self.matchmaker)

        for name, role in partial_schedule.items():
            self.matchmaker.remove_volunteer(name)
            self.jobs.remove_role(role)

        return {
            **partial_schedule,
            **slot_scheduler.generate_schedule()
        }