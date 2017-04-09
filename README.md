# Volunteer Scheduler

This app will pick out the best schedule it can given some time slots, 
some roles, some volunteers, and some constraints.

The schedule ends up looking something like this:

```yml
schedule:
  first-slot:
    carla: manager
    ed: head-of-security
    sue: dj
    mary: security
  second-slot:
    carla: manager
    ed: head-of-security
    sue: dj
    mary: security
   alan: bartender
  third-slot:
    carla: manager
    ed: head-of-security
    alan: security
winning_seed: 12345
winning_score: 100
```

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

### tmp/tentative_schedule.yml

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

## Constraints

Besides the constraints on the number of people doing a role, as seen in `tmp/role_constraints.yml`, we also
have constraints on who can do what role. A good example of this is in `main.py`, where we have the following:

```python
people_constraints = {
    'intro-briefer': [can_speak, not_a_rookie],
    'commentator': [can_speak, not_a_rookie],
    'refreshments': [can_move_around],
    'robot-inspector': [understands_kit, not_a_rookie],
    'helpdesk-volunteer': [understands_kit],
    'shepherd': [can_move_around],
    'tinker-co-ordinator': [not_a_rookie],
    'roving-helper': [understands_kit, can_move_around],
    'match-scorer': [can_move_around],
    'kit-return': [understands_kit]
}
```

For each role, there are a list of constraints. Constraints take a volunteer profile, and return True
if the volunteer is capable of performing that role, or false if they are not.

## Scoring

Right now the scoring is bundled into the app itself, inside `scorer.py`. The anatomy of a scorer is that it
takes a schedule, and returns a score, it has decided based on some criteria.

In the case of the Student Robotics competition, we penalise schedules which do not offer as much variety to
volunteers. The scoring criteria is as follows:

* if a volunteer is performing the same role _n_ times in a row, 
  we add _(n - 1)_ to the score.
* if a volunteer is performing the same role more than twice 
  throughout the competition, we add _(n - 2)_ to the score