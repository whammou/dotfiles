# khalorg local fixes

Applies to `khalorg` 0.2.1 (PyPI), run from the pipx venv
`~/.local/share/pipx/venvs/khalorg`. Reinstalling or upgrading khalorg wipes
these patches; reapplying is one command (see below).

## Behavior after this patch

- The org file is **never written**: no format normalization, so TODO keywords,
  tags and `#+TODO:` / `#+OPTIONS:` / `#+FILETAGS:` headers survive a sync.
- Nothing from khal/CalDAV is appended to the org file; the sync is one-way
  (org -> calendar).
- Headings without `SCHEDULED` / `DEADLINE` are skipped (logged at DEBUG)
  instead of aborting the whole run with `InvalidOrgItemError`.
- `SCHEDULED:` / `DEADLINE:` dates are read. orgparse keeps the planning line
  out of the node body and `get_timestamps()` only scans body text, so without
  this patch every planning-dated item looked undated.
- Items dated before today are skipped at DEBUG instead of failing the whole run
  with `Agenda item date not in the future`; today still counts as future. The
  skip only applies to items with no event yet (see the update rule below).
- Identity is the org `:ID:` property. Every run merges a cumulative
  `org-ID -> khal UID` map into `~/.local/share/khalorg/<calendar>.map.json`, so
  renaming or re-dating a heading updates that same event through `khal edit`
  instead of creating a second one. Items without `:ID:` fall back to the old
  title + first-date match against the state file.
- Events whose UID is known but which fall outside the `khal list` window are
  loaded by UID, so items scheduled beyond the window are updated, not cloned.
- Re-dating an overdue item works. `Calendar.edit` no longer filters candidates
  by `is_future` when the UID is known: a UID is an identity, so the event is
  found and updated even though its stored end is in the past. The filter stays
  for UID-less lookups, where summary plus dates is the only handle and a past
  event is not a candidate.
- Date/end changes are applied only when the run passes `--edit-dates`
  (`orgpush` always does).
- A past start only blocks **creation**. Once the org `:ID:` maps to an event,
  the item is an update, so it is still pushed after its start time passed:
  editing the duration of an event that started earlier today works, and so does
  re-dating an overdue one. `khalorg edit` drops the same future check for the
  same reason.
- Durations come from the timestamp, because org has no duration syntax.
  `SCHEDULED: <2026-11-15 Sun 16:00-18:00>` is a 2h event;
  `<2026-11-15 Sun 16:00 +2h>` is a **repeater** and becomes a 1h event with
  `RRULE:FREQ=HOURLY;INTERVAL=2`.

## Deletion

`khalorg` never deletes; `orgpush` decides deletion itself, after the push loop:

- `orgpush/delete_orphans.py` scans **every** `.org` file under the org root for
  `:ID:` properties and compares them with `<calendar>.map.json`. A mapped ID
  that no longer appears anywhere is an orphan: its khal event is deleted
  through khal's collection API, the map entry is pruned, and the helper prints
  `orphan` / `deleted` / `deleted-in` TSV lines.
- For each affected calendar, `orgpush/gcal_delete.py` deletes the UID from
  Google (`events?iCalUID=` lookup, then `DELETE events/{id}`), the local `.ics`
  is removed, then `vdirsyncer sync gcal/<id>` reconciles its status file. The
  remote delete goes first on purpose: `vdirsyncer` reads a missing local file
  as "not downloaded yet" and fetches it back, and a locally emptied collection
  trips `Storage ... was completely emptied`.
- The pass runs when an `.org` file **or a directory** under the root is newer
  than the last run, so deleting the last dated heading of a file (khalorg then
  has nothing to push) and deleting a whole file both trigger it. A full scan
  costs ~1.3 s over ~300 files, hence a trigger instead of every run.
- Safety: the helper refuses to run on fewer than 10 `.org` files or fewer than
  5 known IDs, and it writes nothing without `--apply`.

## Limitations

- Deletions are not propagated by khalorg itself: it is fed one org file per
  run, so a heading missing from that file is indistinguishable from a heading
  living in a sibling file, and `--delete-on-sync` would wipe whole calendars.
  `orgpush` handles deletion instead (see "Deletion" below).
- Events edited or deleted in Google Calendar are not pulled into org. The org
  file stays the source of truth, so the next org edit overwrites them.
- The UID map is machine-local and per calendar
  (`<calendar>.map.json`). Only the machine named in `orgpush` writes to the
  calendar; the other machines run no push at all.
- Moving an event to a different calendar keeps its UID, but the target
  calendar's map has to be seeded, otherwise khalorg treats the item as new and
  creates a second event.
- `vdirsyncer` for the `gcal` pair must use `conflict_resolution = "a wins"`
  (local wins). With `"b wins"` a remote copy silently overwrites an
  org-driven local edit on conflict.
- State file `~/.local/share/khalorg/<calendar>.org` is still written for
  compatibility, but identity no longer depends on it being complete.

## Apply

```sh
S=~/.local/share/pipx/venvs/khalorg/lib/python3.14/site-packages
patch -p1 -d "$S" < ~/dotfiles/patches/khalorg-local-fixes.patch
```

## Runner

`~/dotfiles/orgpush/orgpush` plus `orgpush.service` / `orgpush.timer` in
`~/dotfiles/systemd/user/` push org edits to Google Calendar:

- timer fires every minute; the script exits immediately on any host other than
  `homelab` (single writer), takes a `flock`, and reads only `*.org` files newer
  than `~/.local/state/orgpush/last-run`
- a file is handed to `khalorg sync --edit-dates` only if it still schedules
  something today or later
- each file goes to the calendar of its top-level area, read from
  `~/dotfiles/orgpush/calendars.tsv` (one khal calendar per area; areas without
  a row fall back to `gcal`)
- `vdirsyncer sync gcal/<collection>` runs only for the collections khalorg
  actually rewrote in that run; syncing the whole pair walks all 25 calendars
  and costs about a second per calendar
- the stamp is set to the run's start time, so edits made during a run are
  picked up by the next one
- log: `~/.local/state/orgpush/log`

## Dependency note

khalorg pins `orgparse~=0.4`, which also admits 0.5.x, and pipx picks the newest.
0.5 moved planning timestamps further out of reach, so this venv is pinned:

```sh
~/.local/share/pipx/venvs/khalorg/bin/python -m pip install "orgparse<0.5"
```
