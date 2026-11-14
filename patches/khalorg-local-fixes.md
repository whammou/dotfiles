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
  with `Agenda item date not in the future`; today still counts as future.
- Identity is the org `:ID:` property. Every run merges a cumulative
  `org-ID -> khal UID` map into `~/.local/share/khalorg/<calendar>.map.json`, so
  renaming or re-dating a heading updates that same event through `khal edit`
  instead of creating a second one. Items without `:ID:` fall back to the old
  title + first-date match against the state file.
- Events whose UID is known but which fall outside the `khal list` window are
  loaded by UID, so items scheduled beyond the window are updated, not cloned.
- Date/end changes are applied only when the run passes `--edit-dates`
  (`orgpush` always does).

## Limitations

- Deletions are not propagated: deleting a heading leaves the event in Google
  Calendar (delete it there, or drop the UID from the map and delete the event).
- Events edited or deleted in Google Calendar are not pulled into org. The org
  file stays the source of truth, so the next org edit overwrites them.
- The UID map is machine-local. Only the machine named in `orgpush` writes to
  the calendar; the other machines run no push at all.
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
- `vdirsyncer sync gcal` runs only when khalorg actually rewrote an `.ics`
- the stamp is set to the run's start time, so edits made during a run are
  picked up by the next one
- log: `~/.local/state/orgpush/log`

## Dependency note

khalorg pins `orgparse~=0.4`, which also admits 0.5.x, and pipx picks the newest.
0.5 moved planning timestamps further out of reach, so this venv is pinned:

```sh
~/.local/share/pipx/venvs/khalorg/bin/python -m pip install "orgparse<0.5"
```
