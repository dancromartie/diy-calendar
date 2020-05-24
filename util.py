import copy
from datetime import datetime, timedelta
import os
import re

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
EVENTS_DIR = os.path.join(THIS_DIR, "events")
DATE_FORMAT = "%Y-%m-%d"

if not os.path.isdir(EVENTS_DIR):
    os.mkdir(EVENTS_DIR)


def load_event_from_file(event_name):
    assert re.match(r"^\w+$", event_name)

    event_text = open(THIS_DIR + "/events/" + event_name).read()
    keys_vals = re.findall(r"^(\w+): (.*?)$", event_text, flags=re.MULTILINE|re.DOTALL)
    event = dict(keys_vals)
    add_extra_date_info(event)
    event["notes"] = event["notes"].replace("NEWLINE", "\n")
    return event


def add_extra_date_info(event):
    date_obj = datetime.strptime(event["date"], DATE_FORMAT)
    event["day_of_week"] = date_obj.strftime("%a")
    event["days_until"] = round((date_obj - datetime.today()).total_seconds() / 86400, 0)


def load_events(expand=True):
    orig_events = []
    for event_name in os.listdir(THIS_DIR + "/events"):
        orig_events.append(load_event_from_file(event_name))

    additional_events = []
    if expand:
        for event in orig_events:
            additional_events += expand_event(event)

    return orig_events + additional_events


def print_oneline(events):
    for e in events:
        print(
            f"%s (%s), %s, %s (in %d days)" % (
                e["date"], e["day_of_week"], e["start_time"], e["name"], e["days_until"]))


def expand_event(event):
    """Apply recurring info to get copies of the event on other days"""
    if not event.get("recurs"):
        return []

    additional_events = []
    recurs = event["recurs"]
    start_date = datetime.strptime(event["date"], DATE_FORMAT)
    stop_date = datetime.strptime(event["recurs_until"], DATE_FORMAT)

    date_step = start_date
    while date_step < stop_date:
        date_step += timedelta(days=1)
        date_match = False
        if recurs == "annually":
            if date_step.month == start_date.month and date_step.day == start_date.day:
                date_match = True
        elif recurs == "monthly":
            if date_step.day == start_date.day:
                date_match = True
        elif recurs == "weekly":
            if date_step.weekday() == start_date.weekday():
                date_match = True

        if date_match:
            event_copy = copy.deepcopy(event) 
            event_copy["date"] = date_step.strftime(DATE_FORMAT)
            add_extra_date_info(event_copy)
            additional_events.append(event_copy)

    return additional_events
                
        


if __name__ == "__main__":
    pass
