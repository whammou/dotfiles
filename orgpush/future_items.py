#!/usr/bin/env python3
"""Decide whether an org file still schedules something today or later.

orgpush hands a file to khalorg only when this returns 0. A heading counts on a
planning line (SCHEDULED, DEADLINE) or on an active timestamp, and a range
counts by its last day, so a span that is already over is skipped while one that
covers today is not. Inactive timestamps are ignored, as org's agenda ignores
them.

A file the parser cannot read counts as a hit: a parser regression then falls
back to khalorg's own filtering instead of silently dropping an event.
"""

import sys
from datetime import date, datetime

import orgparse


def stamps(node):
    """Return planning and active timestamps of a single heading."""
    found = list(node.get_timestamps(active=True, inactive=False, range=True, point=True))
    for planning in (node.scheduled, node.deadline):
        if planning is not None and planning.start is not None:
            found.append(planning)
    return found


def last_day(stamp):
    """Return the last calendar day a timestamp touches."""
    value = stamp.end or stamp.start
    if value is None:
        return None
    return value.date() if isinstance(value, datetime) else value


def headings(node):
    """Yield every heading below the root, depth first."""
    for child in node.children:
        yield child
        yield from headings(child)


def schedules_future(path, today=None):
    """Return True when any heading reaches today or later."""
    today = today or date.today()
    for node in headings(orgparse.load(path)):
        for stamp in stamps(node):
            day = last_day(stamp)
            if day is not None and day >= today:
                return True
    return False


def main(argv):
    if len(argv) != 2:
        print("usage: future_items.py <org file>", file=sys.stderr)
        return 2
    try:
        return 0 if schedules_future(argv[1]) else 1
    except Exception as error:  # a parse failure must not drop an event
        print(f"future_items: {argv[1]}: {error}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
