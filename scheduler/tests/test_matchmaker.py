from unittest import TestCase
from scheduler.match_maker import MatchMaker
from scheduler.scheduling_exception import SchedulingException
from scheduler.tests.helpers import *


class TestMatchmaker(TestCase):
    def setUp(self):
        self.volunteers = {
            'Jack': create_chef('Jack'),
            'Jill': create_delivery_driver('Jill'),
            'Sue': create_food_critic('Sue')
        }

        self.constraints_by_role = {
            'chef': [can_cook],
            'taster': [can_eat],
            'delivery': [can_ride_a_bike]
        }

    def test_should_return_volunteer_name(self):
        matchmaker = MatchMaker(self.volunteers, self.constraints_by_role)

        assert matchmaker.suggest_volunteer_for_role('chef') == 'Jack'
        assert matchmaker.suggest_volunteer_for_role('delivery') == 'Jill'
        assert matchmaker.suggest_volunteer_for_role('taster') == 'Sue'

    def test_should_throw_exception_if_no_volunteer_capable(self):
        volunteers = {}
        matchmaker = MatchMaker(volunteers, self.constraints_by_role)

        with self.assertRaises(SchedulingException):
            matchmaker.suggest_volunteer_for_role('chef')

    def test_should_remove_volunteer(self):
        matchmaker = MatchMaker(self.volunteers, self.constraints_by_role)

        matchmaker.remove_volunteer('Jack')

        with self.assertRaises(SchedulingException):
            matchmaker.suggest_volunteer_for_role('chef')
