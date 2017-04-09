from unittest import TestCase
from scheduler.jobs_board import JobsBoard
from scheduler.scheduling_exception import SchedulingException


class TestJobsBoard(TestCase):
    def test_should_return_roles_in_priority_order(self):
        jobs = JobsBoard(
            ['first-role', 'second-role'],
            ['first-role'],
            ['third-role']
        )

        self.assertEquals(
            [x for x in jobs.priority_order()],
            [
                'first-role',
                'second-role',
                'first-role',
                'third-role'
            ])

    def test_should_return_true_when_all_necessary_roles_filled(self):
        jobs = JobsBoard(
            ['first-role', 'second-role'],
            ['first-role'],
            ['third-role']
        )

        self.assertTrue(jobs.is_sufficient([
            'first-role',
            'second-role'
        ]))

    def test_should_return_false_when_necessary_roles_remaining(self):
        jobs = JobsBoard(
            ['first-role', 'second-role'],
            ['first-role'],
            ['third-role']
        )

        self.assertFalse(jobs.is_sufficient([
            'first-role',
            'first-role',
            'third-role'
        ]))

    def test_should_remove_job(self):
        jobs = JobsBoard(
            ['second-role'],
            ['first-role'],
            ['third-role']
        )

        jobs.remove_role('second-role')

        self.assertTrue(jobs.is_sufficient([]))

    def test_should_return_minimum_number_of_volunteers(self):
        jobs = JobsBoard(
            ['first-role', 'second-role', 'third-role'],
            ['fourth-role'],
            []
        )

        self.assertEquals(jobs.minimum_number_of_volunteers(), 3)
