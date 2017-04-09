from scheduler.scheduling_exception import SchedulingException


class SlotScheduler:
    def __init__(self, jobs, matchmaker):
        self.jobs = jobs
        self.matchmaker = matchmaker

    def generate_schedule(self):
        schedule = {}

        for job in self.jobs.priority_order():
            nominee = self.matchmaker.suggest_volunteer_for_role(job)
            schedule[nominee] = job

            self.matchmaker.remove_volunteer(nominee)

        if not self.jobs.is_sufficient(list(schedule.values())):
            raise SchedulingException('Not all necessary roles are filled')

        return schedule