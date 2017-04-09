from unittest import TestCase
from scheduler.tests.helpers import *


class TestPartialCompetitionScheduler(TestCase):
    def setUp(self):
        self.volunteers = {
            'Jack': create_chef('Jack'),
            'Jill': create_delivery_driver('Jill'),
            'Sue': create_food_critic('Sue'),
            'John': create_volunteer('John', can_cook=True, can_deliver=True, can_critique=True),
            'Sarah': create_volunteer('Sarah', can_cook=True, can_deliver=True, can_critique=False),
            'Peter': create_volunteer('Peter', can_cook=False, can_deliver=True, can_critique=True),
            'Alan': create_volunteer('Alan', can_cook=True, can_deliver=False, can_critique=True)
        }

        self.people_constraints = {
            'chef': [can_cook],
            'taster': [can_critique],
            'delivery': [can_deliver]
        }

        self.role_constraints = {
            'first-slot': {
                'chef': build_role(min=1, ideal=2, max=3),
                'delivery-driver': build_role(min=1, ideal=3, max=10),
                'critic': build_role(min=1, ideal=1, max=5),
            },
            'second-slot': {
                'chef': build_role(min=3, ideal=3, max=3),
                'delivery-driver': build_role(min=1, ideal=3, max=10),
                'critic': build_role(min=1, ideal=1, max=5),
            },
        }

    def test_should_merge_two_schedules(self):
        volunteers_by_slot = {
            'first-slot': {
                'Jack': self.volunteers['Jack'],
                'Jill': self.volunteers['Jill'],
                'Sue': self.volunteers['Sue'],
                'John': self.volunteers['John'],
                'Sarah': self.volunteers['Sarah'],
            },
            'second-slot': {
                'John': self.volunteers['John'],
                'Jill': self.volunteers['Jill'],
                'Sarah': self.volunteers['Sarah'],
                'Peter': self.volunteers['Peter'],
                'Alan': self.volunteers['Alan']
            }
        }

        scheduler = PartialCompetitionScheduler(
            self.people_constraints,
            self.role_constraints)

        partial_schedule = {
            'first-slot': {
                'Jack': 'manager'
            },
            'second-slot': {
                'Jack': 'manager'
            }
        }

        schedule = scheduler.generate_schedule(
            volunteers_by_slot,
            partial_schedule
        )

        self.assertEqual(schedule, {
            'first-slot': {
                'Jack': 'manager',
                'John': 'chef',
                'Sarah': 'chef',
                'Jill': 'delivery-driver',
                'Sue': 'critic'
            },
            'second-slot': {
                'Jack': 'manager',
                'John': 'chef',
                'Sarah': 'chef',
                'Alan': 'chef',
                'Jill': 'delivery-driver',
                'Peter': 'critic'
            }
        })

