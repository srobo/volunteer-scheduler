import random


def sample(l):
    return random.sample(l, len(l))


def extract_roles(available_roles):
    min = []
    ideal = []
    max = []

    for role, constraints in available_roles.items():
        minimum_count = constraints['min']
        ideal_count = constraints['ideal']
        maximum_count = constraints['max']

        for _ in range(minimum_count):
            min.append(role)
        for _ in range(ideal_count - minimum_count):
            ideal.append(role)
        for _ in range(maximum_count - (ideal_count + minimum_count)):
            max.append(role)

    return min, ideal, max


class RoleRandomiser:
    def __init__(self, available_roles):
        self._available_roles = available_roles

    def get_roles(self):
        necessary_roles, ideal_roles, max_roles = extract_roles(self._available_roles)

        return necessary_roles + ideal_roles + max_roles
