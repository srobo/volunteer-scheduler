class Judge:
    def __init__(self, trial, comparator):
        self.trial = trial
        self.comparator = comparator

    def judge(self, inputs, default):
        results = {input: self.trial(input) for input in inputs}
        eligible = {input: result for input, result in results.items() if result is not None}

        champion = default

        for challenger in eligible.items():
            champion = self.comparator(champion, challenger)

        return champion
