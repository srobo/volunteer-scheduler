from unittest import TestCase
from scheduler.jobs_board import JobsBoard


class TestJobsBoard(TestCase):
    def test_should_return_roles_in_priority_order(self):
        jobs = JobsBoard(
            ['first-role', 'second-role'],
            ['first-role'],
            ['third-role']
        )

        assert [x for x in jobs.priority_order()] == [
            'first-role',
            'second-role',
            'first-role',
            'third-role'
        ]

    def test_should_return_true_when_all_necessary_roles_filled(self):
        jobs = JobsBoard(
            ['first-role', 'second-role'],
            ['first-role'],
            ['third-role']
        )

        assert jobs.is_sufficient([
            'first-role',
            'second-role'
        ]) is True

    def test_should_return_false_when_necessary_roles_remaining(self):
        jobs = JobsBoard(
            ['first-role', 'second-role'],
            ['first-role'],
            ['third-role']
        )

        assert jobs.is_sufficient([
            'first-role',
            'first-role',
            'third-role'
        ]) is False

