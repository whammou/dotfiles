#!/usr/bin/env python3
"""Delete khal events whose org heading (and therefore :ID:) is gone.

khalorg maps org-ID -> khal UID per calendar, but a sync run only sees one org
file, so it cannot tell a deleted heading from a heading living in a sibling
file. Four empty strings keep that from wiping a calendar: the ID has to be
absent from every .org file under --root, only the calendars named with
--calendar are considered, the scan has to look plausible, and nothing happens
without --apply.
"""

import argparse
import glob
import json
import os
import re
import sys

ID_RE = re.compile(r":ID:\s*(\S+)")


def org_ids(root):
    ids, files = set(), 0
    for dirpath, _, filenames in os.walk(root, followlinks=True):
        for name in filenames:
            if not name.endswith(".org"):
                continue
            try:
                text = open(os.path.join(dirpath, name), errors="replace").read()
            except OSError:
                continue
            files += 1
            ids.update(ID_RE.findall(text))
    return ids, files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--khalorg-dir", default="~/.local/share/khalorg")
    parser.add_argument("--calendar", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = os.path.expanduser(args.root)
    khalorg_dir = os.path.expanduser(args.khalorg_dir)
    ids, files = org_ids(root)
    if files < 10 or len(ids) < 5:
        print(f"refusing: scanned {files} org files, {len(ids)} ids", file=sys.stderr)
        return 2

    maps = sorted(glob.glob(os.path.join(khalorg_dir, "*.map.json")))
    if args.calendar:
        wanted = {f"{name}.map.json" for name in args.calendar}
        maps = [m for m in maps if os.path.basename(m) in wanted]

    deleted = []
    for path in maps:
        calendar = os.path.basename(path)[: -len(".map.json")]
        mapping = json.load(open(path))
        orphans = {oid: uid for oid, uid in mapping.items() if oid not in ids}
        if not orphans:
            continue
        for oid, uid in orphans.items():
            print(f"orphan\t{calendar}\t{oid}\t{uid}")
        if not args.apply:
            continue
        from khalorg.khal.calendar import Calendar

        khal_cal = Calendar(calendar)
        for org_id, uid in orphans.items():
            events = khal_cal.get_events(uid)
            for event in events:
                khal_cal.collection.delete(event.href, event.etag, event.calendar)
            if events:
                print(f"deleted\t{calendar}\t{uid}")
        khal_cal.collection.update_db()
        for oid in orphans:
            del mapping[oid]
        with open(path, "w") as handle:
            json.dump(mapping, handle, indent=2, sort_keys=True)
            handle.write("\n")
        deleted.append(calendar)

    for calendar in deleted:
        print(f"deleted-in\t{calendar}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
