from unittest import TestCase
from scheduler.jobs_board import JobsBoard
from scheduler.match_maker import MatchMaker
from scheduler.slot_scheduler import SlotScheduler
from scheduler.scheduling_exception import SchedulingException
from scheduler.tests.helpers import *


class TestSlotScheduler(TestCase):
    def setUp(self):
        self.volunteers = {
            'Jack': create_chef('Jack'),
            'Jill': create_delivery_driver('Jill'),
            'Sue': create_food_critic('Sue')
        }

        self.constraints_by_role = {
            'chef': [can_cook],
            'taster': [can_critique],
            'delivery': [can_deliver]
        }

    def test_generates_a_schedule(self):
        matchmaker = MatchMaker(self.volunteers, self.constraints_by_role)
        jobs = JobsBoard(
            ['chef'],
            ['delivery'],
            ['taster']
        )
        scheduler = SlotScheduler(jobs, matchmaker)

        assert scheduler.generate_schedule() == {
            'Jack': 'chef',
            'Sue': 'taster',
            'Jill': 'delivery'
        }

    def test_raises_exception_when_not_all_necessary_roles_filled(self):
        matchmaker = MatchMaker(self.volunteers, self.constraints_by_role)
        jobs = JobsBoard(
            ['chef', 'chef'],
            ['delivery'],
            ['taster']
        )
        scheduler = SlotScheduler(jobs, matchmaker)

        with self.assertRaises(SchedulingException):
            scheduler.generate_schedule()
