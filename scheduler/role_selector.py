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

    return sample(min), sample(ideal), sample(max)


class RoleSelector:
    def __init__(self, roles):
        self._necessary, self._ideal, self._max = extract_roles(roles)

    def get_minimum_number_of_volunteers(self):
        return len(self._necessary)

    def is_role_needed(self, role):
        return role in self._necessary

    def fill_role(self, role):
        if role in self._necessary:
            self._necessary.remove(role)
            return True
        elif role in self._ideal:
            self._ideal.remove(role)
            return True
        elif role in self._max:
            self._max.remove(role)
            return True
        else:
            return False

    def remaining_necessary_roles(self):
        return self._necessary

    def any_necessary_roles_unfilled(self):
        return self._necessary

    def select_role(self, volunteer, is_safe):
        for role in self._necessary:
            if is_safe(volunteer, role):
                self._necessary.remove(role)
                return role

        for role in self._ideal:
            if is_safe(volunteer, role):
                self._ideal.remove(role)
                return role

        for role in self._max:
            if is_safe(volunteer, role):
                self._max.remove(role)
                return role
