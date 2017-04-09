from scheduler.match_maker import MatchMakingException
from scheduler.scheduling_exception import SchedulingException


class SlotScheduler:
    def __init__(self, jobs, matchmaker):
        self.jobs = jobs
        self.matchmaker = matchmaker

    def generate_schedule(self):
        schedule = {}

        for job in self.jobs.priority_order():
            try:
                nominee = self.matchmaker.suggest_volunteer_for_role(job)
                schedule[nominee] = job
                self.matchmaker.remove_volunteer(nominee)
            except MatchMakingException as ex:
                pass

        filled_roles = list(schedule.values())

        if not self.jobs.is_sufficient(filled_roles):
            unfilled_roles = self.jobs.unfilled_necessary_roles(filled_roles)
            raise SchedulingException('Not all necessary roles are filled - {}'.format(unfilled_roles))

        return schedule
