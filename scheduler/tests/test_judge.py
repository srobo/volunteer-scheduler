from unittest import TestCase
from scheduler.judge import Judge

citrus_content = {
    'lemons': 999,
    'cheese': 20,
    'doorknobs': 1
}


def get_citrus_content(input):
    return citrus_content.get(input, 0)


def get_citrus_content_but_no_lemons(input):
    if input == 'lemons':
        return None

    return get_citrus_content(input)


def judge_citrus(reigning_champion, challenger):
    _, champ_citrus = reigning_champion
    _, new_citrus = challenger

    if new_citrus > champ_citrus:
        return challenger

    return reigning_champion


class TestJudge(TestCase):
    def test_should_return_best_input(self):
        judge = Judge(get_citrus_content, judge_citrus)
        default_champion = ('nothing', 0)

        winner, winning_value = judge.judge([
            'crab claws',
            'doorknobs'
            'chicken dippers',
            'cheese',
            'lemons'
        ], default_champion)

        self.assertEquals(winner, 'lemons')

    def test_should_return_default_champion_if_no_challengers(self):
        judge = Judge(get_citrus_content, judge_citrus)
        default_champion = ('nothing', 0)

        winner, winning_value = judge.judge([], default_champion)

        self.assertEquals(winner, 'nothing')

    def test_should_remove_ineligible_contestants(self):
        judge = Judge(get_citrus_content_but_no_lemons, judge_citrus)
        default_champion = ('nothing', 0)

        winner, winning_value = judge.judge([
            'crab claws',
            'doorknobs',
            'lemons',
            'chicken dippers',
            'cheese'
        ], default_champion)

        self.assertEquals(winner, 'cheese')
