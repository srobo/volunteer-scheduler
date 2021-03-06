from scheduler.validator.validator import is_valid


class MatchMakingException(Exception):
    pass


class MatchMaker:
    def __init__(self, volunteers, constraints_by_role):
        self.volunteers = {k: v for k, v in volunteers.items()}
        self.constraints = constraints_by_role

    def remove_volunteer(self, name):
        if name in self.volunteers.keys():
            del self.volunteers[name]

    def suggest_volunteer_for_role(self, role):
        relevant_constraints = self.constraints.get(role, [])
        able_volunteers = [name for name, attributes in self.volunteers.items()
                           if is_valid(attributes, relevant_constraints)]

        if not able_volunteers:
            raise MatchMakingException('No volunteers can fill the role [{}]'.format(role))

        return able_volunteers[0]

    def number_of_available_volunteers(self):
        return len(self.volunteers.keys())
