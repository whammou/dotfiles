#!/usr/bin/env python3
"""Delete events on Google Calendar by iCalUID.

Needed when a khal collection becomes empty: vdirsyncer refuses to mirror an
empty local storage ("Storage was completely emptied"), so the remote copy has
to go first. Credentials are read from the vdirsyncer config at runtime and
never stored here.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/calendar/v3"


def config_value(section_text, key):
    match = re.search(rf'{key}\s*=\s*"([^"]+)"', section_text)
    if not match:
        raise SystemExit(f"missing {key} in vdirsyncer config")
    return match.group(1)


def access_token():
    home = os.path.expanduser("~")
    config = open(os.path.join(home, ".config/vdirsyncer/config")).read()
    section = config.split("[storage gcal_remote]")[1].split("\n[")[0]
    token = json.load(open(os.path.join(home, ".local/share/vdirsyncer/google_token.json")))
    body = urllib.parse.urlencode({
        "client_id": config_value(section, "client_id"),
        "client_secret": config_value(section, "client_secret"),
        "refresh_token": token["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    request = urllib.request.Request("https://oauth2.googleapis.com/token", data=body)
    return json.load(urllib.request.urlopen(request))["access_token"]


def call(url, token, method="GET"):
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"}, method=method)
    return urllib.request.urlopen(request)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", required=True)
    parser.add_argument("--uid", action="append", required=True)
    args = parser.parse_args()

    token = access_token()
    base = f"{API}/calendars/{urllib.parse.quote(args.collection, safe='')}/events"
    for uid in args.uid:
        lookup = f"{base}?iCalUID={urllib.parse.quote(uid)}&singleEvents=false"
        items = json.load(call(lookup, token)).get("items", [])
        if not items:
            print(f"already absent\t{uid}")
            continue
        for item in items:
            target = f"{base}/{urllib.parse.quote(item['id'], safe='')}"
            try:
                call(target, token, method="DELETE")
                print(f"deleted\t{uid}\t{item.get('summary')}")
            except urllib.error.HTTPError as error:
                print(f"failed\t{uid}\t{error}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
