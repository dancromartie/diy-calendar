#!/usr/bin/env python3

import argparse
import os
import re
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def add_event(
        name, date, start_time, duration_minutes, no_confirm=False, notes="",
        recurs=None, recurs_until=None):
    assert re.match(r"^\w+$", name)
    assert re.match(r"^\d\d\d\d-\d\d-\d\d$", date)
    assert re.match(r"^\d\d:\d\d", start_time)
    assert duration_minutes.isdigit()

    if recurs:
        assert recurs.lower() in ("weekly", "monthly", "annually")
    if recurs_until:
        assert re.match(r"^\d\d\d\d-\d\d-\d\d$", recurs_until)

    to_write = f"""
        name: {name}
        date: {date}
        start_time: {start_time}
        duration_minutes: {duration_minutes}
        notes: {notes}
    """
    to_write = re.sub(r"^\s+", "", to_write, flags=re.MULTILINE)

    if recurs:
        assert recurs_until
        to_write += "recurs: %s\n" % recurs
    if recurs_until:
        assert recurs
        to_write += "recurs_until: %s\n" % recurs_until

    if not no_confirm:
        print("Your event will look like this:")
        print(to_write)
        user_confirmation = input("Proceed? (y/n)")

        if user_confirmation.lower() != "y":
            print("aborting due to user request")
            sys.exit(0)
        
    output_path = THIS_DIR + "/events/" + name
    if os.path.exists(output_path):
        print("That event already exists. Please give it a unique name.")
        sys.exit(1)

    with open(output_path, "w") as event_f_out:
        event_f_out.write(to_write)
        print("event writen to %s" % output_path)
        


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--name", required=True)
    argument_parser.add_argument("--date", required=True)
    argument_parser.add_argument("--start-time", required=True)
    argument_parser.add_argument("--duration-minutes", required=True)
    argument_parser.add_argument("--notes", default="")
    argument_parser.add_argument("--recurs")
    argument_parser.add_argument("--recurs-until")
    argument_parser.add_argument("--no-confirm", action="store_true")
    cli_args = argument_parser.parse_args()
    add_event(
        cli_args.name,
        cli_args.date,
        cli_args.start_time,
        cli_args.duration_minutes,
        recurs=cli_args.recurs,
        recurs_until=cli_args.recurs_until,
        notes=cli_args.notes)
    

if __name__ == "__main__":
    main()

