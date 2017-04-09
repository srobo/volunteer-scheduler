def can_cook(volunteer):
    return volunteer['can_cook']


def can_ride_a_bike(volunteer):
    return volunteer['rides_a_bike']


def can_eat(volunteer):
    return volunteer['can_eat']


def create_chef(name):
    return {
        'name': name,
        'can_cook': True,
        'rides_a_bike': False,
        'can_eat': False
    }


def create_delivery_driver(name):
    return {
        'name': name,
        'can_cook': False,
        'rides_a_bike': True,
        'can_eat': False
    }


def create_food_critic(name):
    return {
        'name': name,
        'can_cook': False,
        'rides_a_bike': False,
        'can_eat': True
    }