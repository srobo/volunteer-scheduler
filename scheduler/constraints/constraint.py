class Verdict:
    def __init__(self):
        pass

    FAIL = float('inf')
    OK = 0.0


class PositionConstraint:
    def __init__(self):
        pass

    def evaluate(self, volunteer, role):
        return 0.0


class SlotConstraint:
    def __init__(self):
        pass

    def evaluate(self, slot):
        return 0.0
