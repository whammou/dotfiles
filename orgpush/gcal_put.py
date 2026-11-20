#!/usr/bin/env python3
"""Push khal .ics items to Google Calendar through the Calendar v3 API.

vdirsyncer stays the sync engine, but a single `vdirsyncer sync <collection>`
has to discover the collection on Google before it can copy anything: about 2s
on this account even when nothing changed, up to 9s when it has an item to
upload. One `events.patch` or `events.import` is a single request (~0.5s), which
is what makes an org edit appear on the calendar promptly.

The remote event is matched by iCalUID - the UID khalorg already wrote - so no
second id mapping is introduced. orgpush records the collection and lets
vdirsyncer reconcile it on a later run, after the user-visible push is done.

Credentials are read from the vdirsyncer config at runtime, exactly like
gcal_delete.py, so nothing is stored here.
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

import icalendar

API = "https://www.googleapis.com/calendar/v3"


def config_value(section_text, key):
    match = re.search(rf'{key}\s*=\s*"([^"]+)"', section_text)
    if not match:
        raise SystemExit(f"missing {key} in vdirsyncer config")
    return match.group(1)


def access_token():
    home = os.path.expanduser("~")
    with open(os.path.join(home, ".config/vdirsyncer/config")) as handle:
        config = handle.read()
    section = config.split("[storage gcal_remote]")[1].split("\n[")[0]
    with open(os.path.join(home, ".local/share/vdirsyncer/google_token.json")) as handle:
        token = json.load(handle)
    body = urllib.parse.urlencode(
        {
            "client_id": config_value(section, "client_id"),
            "client_secret": config_value(section, "client_secret"),
            "refresh_token": token["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode()
    request = urllib.request.Request("https://oauth2.googleapis.com/token", data=body)
    return json.load(urllib.request.urlopen(request))["access_token"]


def call(url, token, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(request))


def moment(prop):
    value = prop.dt
    if isinstance(value, datetime.datetime):
        result = {"dateTime": value.isoformat()}
        zone = prop.params.get("TZID")
        if zone is not None:
            result["timeZone"] = str(zone)
        return result
    return {"date": value.isoformat()}


def recurrence(vevent):
    lines = []
    for name in ("RRULE", "RDATE", "EXDATE"):
        if name not in vevent:
            continue
        props = vevent[name] if isinstance(vevent[name], list) else [vevent[name]]
        for prop in props:
            zone = prop.params.get("TZID")
            prefix = f"{name};TZID={zone}:" if zone is not None else f"{name}:"
            lines.append(prefix + prop.to_ical().decode().strip())
    return lines


def event_body(path):
    with open(path, "rb") as handle:
        calendar = icalendar.Calendar.from_ical(handle.read())
    masters = [item for item in calendar.walk("VEVENT") if "RECURRENCE-ID" not in item]
    if not masters:
        raise SystemExit(f"no master VEVENT in {path}")
    vevent = masters[0]
    if "UID" not in vevent or "DTSTART" not in vevent:
        raise SystemExit(f"missing UID/DTSTART in {path}")

    body = {
        "iCalUID": str(vevent["UID"]),
        "start": moment(vevent["DTSTART"]),
        "end": moment(vevent["DTEND"]) if "DTEND" in vevent else moment(vevent["DTSTART"]),
    }
    for key, field in (
        ("SUMMARY", "summary"),
        ("DESCRIPTION", "description"),
        ("LOCATION", "location"),
    ):
        if key in vevent:
            body[field] = str(vevent[key])
    if "STATUS" in vevent:
        status = str(vevent["STATUS"]).lower()
        if status in ("confirmed", "tentative", "cancelled"):
            body["status"] = status
    if "TRANSP" in vevent:
        body["transparency"] = (
            "transparent" if str(vevent["TRANSP"]).upper() == "TRANSPARENT" else "opaque"
        )
    rules = recurrence(vevent)
    if rules:
        body["recurrence"] = rules
    return body


def push(token, collection, path, dry_run):
    body = event_body(path)
    base = f"{API}/calendars/{urllib.parse.quote(collection, safe='')}/events"
    uid = urllib.parse.quote(body["iCalUID"], safe="")
    found = call(f"{base}?iCalUID={uid}&singleEvents=false", token).get("items", [])

    if not found:
        if dry_run:
            print(json.dumps({"op": "import", "body": body}, indent=2))
            return
        created = call(f"{base}/import", token, method="POST", body=body)
        print(f"created\t{body['iCalUID']}\t{created.get('id')}")
        return

    target = f"{base}/{urllib.parse.quote(found[0]['id'], safe='')}"
    # iCalUID is output-only on update, and a stale SEQUENCE is rejected as
    # non-monotonic, so both are left for Google to keep on its side.
    patch = {key: value for key, value in body.items() if key not in ("iCalUID",)}
    if dry_run:
        print(json.dumps({"op": "patch", "url": target, "body": patch}, indent=2))
        return
    call(target, token, method="PATCH", body=patch)
    print(f"updated\t{body['iCalUID']}\t{found[0]['id']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", required=True, help="Google calendar id")
    parser.add_argument("--dry-run", action="store_true", help="print the request, send nothing")
    parser.add_argument("files", nargs="+", help=".ics files khalorg just wrote")
    args = parser.parse_args()

    # dry-run keeps the read-only lookup so the chosen branch is proven, writes are skipped.
    token = access_token()
    failed = 0
    for path in args.files:
        try:
            push(token, args.collection, path, args.dry_run)
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            print(f"failed\t{os.path.basename(path)}\t{error.code}\t{detail}", file=sys.stderr)
            failed = 1
        except (OSError, ValueError, SystemExit) as error:
            print(f"failed\t{os.path.basename(path)}\t{error}", file=sys.stderr)
            failed = 1
    return failed


if __name__ == "__main__":
    sys.exit(main())
