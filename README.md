# Volunteer Scheduler

## Requirements

* Python 3.5+
* virtualenv

## Running

To run the scheduler, you need a handful of files in place.

1. tmp/volunteers.yml
2. tmp/availability.yml
3. tmp/constraints.yml
4. tmp/permanent_roles.yml
5. tmp/tentative_schedule.yml

### tmp/volunteers.yml

Contains key value pairs for a given volunteer.

```yml
mary:
  can_lift: true
  can_move: true
  can_setup: true
  can_speak: false
  is_rookie: false
  is_technical: true
  name: Mary
sue:
  can_lift: true
  can_move: true
  can_setup: true
  can_speak: false
  is_rookie: true
  is_technical: true
  name: Sue
alan:
  can_lift: true
  can_move: true
  can_setup: true
  can_speak: true
  is_rookie: false
  is_technical: true
  name: Alan
```

The key corresponds to a given volunteer's "ID", which is what is used in `tmp/availibility.yml`.

### tmp/availability.yml

Contains the list of volunteers available for a given time slot.

```yml
first-slot:
- sue
- mary
second-slot:
- sue
- mary
- alan
third-slot:
- alan
```

### tmp/role_constraints.yml

Contains the list of roles, as well as their limitations, for a given time slot.

```yml
first-slot:
  dj:
    ideal: 1
    max: 1
    min: 1
  security:
    ideal: 3
    max: 5
    min: 0
  bartender:
    ideal: 2
    max: 2
    min: 1
second-slot:
  dj:
    ideal: 1
    max: 1
    min: 1
  security:
    ideal: 3
    max: 5
    min: 3
  bartender:
    ideal: 2
    max: 2
    min: 1
third-slot:
  dj:
    ideal: 1
    max: 1
    min: 1
  security:
    ideal: 3
    max: 5
    min: 3
  bartender:
    ideal: 3
    max: 4
    min: 2
```

### tmp/permanent.yml

Contains a list of people who are doing permanent roles.

```yml
carla: manager
ed: head-of-security
```

## tmp/tentative_schedule.yml

Contains a tentative schedule, meaning you can assign people to roles.

Permanent roles shouldn't be entered in here, as this overwrites their permanent role.

This does however mean you can have someone in a permanent role, except during certain times.

```yml
first-slot:
  sue: dj
  mary: security
second-slot:
  sue: dj
  mary: security
  alan: bartender
third-slot:
  alan: security
```

