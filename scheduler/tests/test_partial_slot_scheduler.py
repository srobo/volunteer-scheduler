from unittest import TestCase
from scheduler.jobs_board import JobsBoard
from scheduler.match_maker import MatchMaker
from scheduler.partial_slot_scheduler import PartialSlotScheduler
from scheduler.tests.helpers import *


class TestPartialSlotScheduler(TestCase):
    def setUp(self):
        self.volunteers = {
            'Jack': create_chef('Jack'),
            'John': create_chef('John'),
            'Jill': create_delivery_driver('Jill'),
            'Sue': create_food_critic('Sue')
        }

        self.constraints_by_role = {
            'chef': [can_cook],
            'taster': [can_critique],
            'delivery': [can_deliver]
        }

    def test_merges_two_schedules(self):
        matchmaker = MatchMaker(self.volunteers, self.constraints_by_role)
        jobs = JobsBoard(
            ['chef'],
            ['delivery'],
            ['taster']
        )

        partial_schedule = {
            'Jack': 'manager'
        }

        scheduler = PartialSlotScheduler(jobs, matchmaker)

        assert scheduler.generate_schedule(partial_schedule) == {
            'Jack': 'manager',
            'John': 'chef',
            'Sue': 'taster',
            'Jill': 'delivery'
        }
