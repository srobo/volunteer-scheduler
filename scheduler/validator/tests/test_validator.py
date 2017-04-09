from unittest import TestCase
from scheduler.validator.validator import is_valid


def always_passing_constraint(_):
    return True


def always_failing_constraint(_):
    return False


class TestValidator(TestCase):
    def test_passes_validation_when_all_constraints_pass(self):
        volunteer = {}

        assert is_valid(volunteer, [
            always_passing_constraint,
            always_passing_constraint,
            always_passing_constraint
        ]) is True

    def test_fails_validation_when_one_constraint_fails(self):
        volunteer = {}

        assert is_valid(volunteer, [
            always_passing_constraint,
            always_failing_constraint,
            always_passing_constraint
        ]) is False
