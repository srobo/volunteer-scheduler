class JobsBoard:
    def __init__(self, minimum_roles, ideal_roles, maximum_roles):
        self.minimum = minimum_roles
        self.ideal = ideal_roles
        self.max = maximum_roles

    def priority_order(self):
        for role in self.minimum:
            yield role

        for role in self.ideal:
            yield role

        for role in self.max:
            yield role

    def is_sufficient(self, filled_roles):
        necessary_roles = self.minimum[:]

        for role in filled_roles:
            if role in necessary_roles:
                necessary_roles.remove(role)

        return necessary_roles == []

    def minimum_number_of_volunteers(self):
        return len(self.minimum)

    def unfilled_necessary_roles(self, filled_roles):
        necessary_roles = self.minimum[:]

        for role in filled_roles:
            if role in necessary_roles:
                necessary_roles.remove(role)

        return necessary_roles

    def remove_role(self, role):
        if role in self.minimum:
            self.minimum.remove(role)
        elif role in self.ideal:
            self.ideal.remove(role)
        elif role in self.max:
            self.max.remove(role)
