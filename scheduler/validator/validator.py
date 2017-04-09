def is_valid(volunteer, constraints):
    return all(constraint(volunteer) for constraint in constraints)
