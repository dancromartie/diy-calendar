#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta

import util


def main(show_all_events=False, search_name_for=""):
    events = util.load_events()
    events.sort(key=lambda x: x["date"])
    
    # Apply user search in event name
    events = [e for e in events if search_name_for in e["name"].lower()]

    # Don't show dates that are unreasonably far, or before today
    years_from_now = (datetime.now() + timedelta(days=365*2)).strftime(util.DATE_FORMAT)
    today = datetime.now().strftime(util.DATE_FORMAT)
    events = [e for e in events if e["date"] < years_from_now]
    events = [e for e in events if e["date"] >= today]

    if show_all_events:
        util.print_oneline(events)
    else:
        util.print_oneline(events[:10])


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-a", action="store_true", help="print *a*ll events")
    argument_parser.add_argument("-s", default="", help="*s*earch for this in event name")
    cli_args = argument_parser.parse_args()
    main(cli_args.a, cli_args.s)

