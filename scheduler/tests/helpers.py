def can_cook(volunteer):
    return volunteer['can_cook']


def can_deliver(volunteer):
    return volunteer['can_deliver']


def can_critique(volunteer):
    return volunteer['can_critique']


def build_role(min, ideal, max):
    return {
        'min': min,
        'ideal': ideal,
        'max': max
    }


def create_volunteer(name, can_cook, can_deliver, can_critique):
    return {
        name: name,
        'can_cook': can_cook,
        'can_deliver': can_deliver,
        'can_critique': can_critique
    }


def create_chef(name):
    return create_volunteer(
        name,
        can_cook=True,
        can_deliver=False,
        can_critique=False
    )


def create_delivery_driver(name):
    return create_volunteer(
        name,
        can_cook=False,
        can_deliver=True,
        can_critique=False
    )


def create_food_critic(name):
    return create_volunteer(
        name,
        can_cook=False,
        can_deliver=False,
        can_critique=True
    )