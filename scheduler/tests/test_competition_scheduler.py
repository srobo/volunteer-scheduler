from unittest import TestCase
from scheduler.competition_scheduler import CompetitionScheduler
from scheduler.tests.helpers import *


def build_role(min, ideal, max):
    return {
        'min': min,
        'ideal': ideal,
        'max': max
    }


class TestCompetitionScheduler(TestCase):
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

    def test_schedules_competition(self):
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

        scheduler = CompetitionScheduler(
            self.people_constraints,
            self.role_constraints)

        schedule = scheduler.generate_schedule(volunteers_by_slot)

        assert schedule == {
            'first-slot': {
                'Jack': 'chef',
                'John': 'chef',
                'Jill': 'delivery-driver',
                'Sarah': 'delivery-driver',
                'Sue': 'critic'
            },
            'second-slot': {
                'John': 'chef',
                'Sarah': 'chef',
                'Alan': 'chef',
                'Jill': 'delivery-driver',
                'Peter': 'critic'
            }
        }
