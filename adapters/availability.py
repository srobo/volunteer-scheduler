import csv
import sys
import yaml

AVAILABLE_SLOTS = [
    'saturday-0830-1100',
    'saturday-1100-1300',
    'saturday-1300-1500',
    'saturday-1500-1730',
    'sunday-0830-1100',
    'sunday-1100-1300',
    'sunday-1300-1500',
    'sunday-1500-1730'
]

ARRIVAL_MAPPINGS = {
    'Saturday, 1st April - by 8:30 AM': 'saturday-0830-1100',
    'Saturday, 1st April - by 11:45 AM': 'saturday-1300-1500',
    'Saturday, 1st April - later than 11:45 AM': 'saturday-1500-1730',
    'Sunday, 2nd April - by 8:30 AM': 'sunday-0830-1100',
    'Sunday, 2nd April - by 11:45 AM': 'sunday-1300-1500'
}

LEAVING_MAPPINGS = {
    'Saturday, 1st April - before 11:45': 'saturday-0830-1100',
    'Saturday, 1st April - before 17:30': 'saturday-1300-1500',
    'Saturday, 1st April - after 17:30': 'saturday-1500-1730',
    'Sunday, 2nd April - before 11:45': 'sunday-0830-1100',
    'Sunday, 2nd April - before 18:00': 'sunday-1500-1730',
    'Sunday, 2nd April - before 20:00': 'sunday-1500-1730',
    'I am able to stay at the venue until it is cleared': 'sunday-1500-1730'
}

def get_first_slot(arrival_time):
    if 'Thursday' in arrival_time or 'Friday' in arrival_time:
        return 'saturday-0830-1100'

    return ARRIVAL_MAPPINGS[arrival_time]


def get_last_slot(leaving_time):
    return LEAVING_MAPPINGS[leaving_time]


def get_slots(arrival_time, leaving_time):
    first_slot = get_first_slot(arrival_time)
    last_slot = get_last_slot(leaving_time)

    return AVAILABLE_SLOTS[AVAILABLE_SLOTS.index(first_slot):AVAILABLE_SLOTS.index(last_slot) + 1]


def is_rookie(response):
    return response != 'Yes, as a volunteer'


def is_yes(response):
    return 'Yes' in response


def get_name(response):
    parts = response.strip().lower().split(' ', 2)
    surname = ''.join([i for i in parts[1] if i.isalpha()])

    return "{}{}".format(parts[0][0], surname)


def convert_to_volunteer(row):
    return {
        'name': get_name(row['What is your full name?']),
        'is_rookie': is_rookie(row['Have you attended an SR competition previously?']),
        'slots': get_slots(
            arrival_time=row['When will you be arriving at the competition venue?'],
            leaving_time=row['What time will you be leaving the competition?']
        ),
        'can_speak': is_yes(row['Are you comfortable speaking in front of an audience?']),
        'can_lift': is_yes(row['Are you prepared to be involved in tasks that involve physical exertion (e.g. moving tables around)?']),
        'is_technical': is_yes(row['Do you feel able to help teams with technical problems?']),
        'can_setup': is_yes(row['Do you feel able to help with technical set-up and maintenance?']),
        'can_move': is_yes(row['Are you OK to stand and/or walk around for long periods of time?'])
    }


def get_available_volunteers(slot, volunteers):
    return [v['name'] for v in volunteers if slot in v['slots']]


args = sys.argv[1:]

with open(args[0], 'r') as f:
    reader = csv.DictReader(f)

    volunteers = [convert_to_volunteer(v) for v in reader]

    people_by_slot = {slot: get_available_volunteers(slot, volunteers) for slot in AVAILABLE_SLOTS}

    result = {
        'volunteers': {v['name']: v for v in volunteers},
        'slots': people_by_slot
    }

    print(yaml.dump(result, default_flow_style=False))
