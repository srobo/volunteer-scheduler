from scheduler.match_maker import MatchMakingException
from scheduler.scheduling_exception import SchedulingException


class SlotScheduler:
    def __init__(self, jobs, matchmaker):
        self.jobs = jobs
        self.match_maker = matchmaker

    def generate_schedule(self):
        schedule = {}

        number_needed = self.jobs.minimum_number_of_volunteers()
        number_available = self.match_maker.number_of_available_volunteers()

        if number_needed > number_available:
            raise SchedulingException(
                'Not enough volunteers available [{}] for slot [{}]'.format(
                    number_available,
                    number_needed
                ))

        for job in self.jobs.priority_order():
            try:
                nominee = self.match_maker.suggest_volunteer_for_role(job)
                schedule[nominee] = job
                self.match_maker.remove_volunteer(nominee)
            except MatchMakingException as ex:
                pass

        filled_roles = list(schedule.values())

        if not self.jobs.is_sufficient(filled_roles):
            unfilled_roles = self.jobs.unfilled_necessary_roles(filled_roles)
            raise SchedulingException('Not all necessary roles are filled - {}'.format(unfilled_roles))

        return schedule
