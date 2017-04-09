from unittest import TestCase
from scheduler.utilities import deep_merge

class TestDeepMerge(TestCase):
    def test_should_merge_two_dicts_with_no_collisions(self):
        a = {
            'some_key': 'some_value'
        }

        b = {
            'some_other_key': 'some_other_value'
        }

        self.assertEquals(deep_merge(a, b), {
            'some_key': 'some_value',
            'some_other_key': 'some_other_value'
        })

    def test_should_merge_three_dicts_with_no_collisions(self):
        a = {'some_key': 'some_value'}
        b = {'some_other_key': 'some_other_value'}
        c = {'and_another_key': 'and_another_value'}

        self.assertEquals(deep_merge(a, b, c), {
            'some_key': 'some_value',
            'some_other_key': 'some_other_value',
            'and_another_key': 'and_another_value'
        })

    def test_should_deep_merge_dicts_within_dicts(self):
        a = {'parent_key': {'some_key': 'some_value'}}
        b = {'parent_key': {'some_other_key': 'some_other_value'}}
        c = {'parent_key': {'and_another_key': 'and_another_value'}}

        self.assertEquals(deep_merge(a, b, c), {
            'parent_key': {
                'some_key': 'some_value',
                'some_other_key': 'some_other_value',
                'and_another_key': 'and_another_value'
            }
        })
