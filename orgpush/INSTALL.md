# orgpush install (fresh Arch machine)

Org agenda items are pushed from org files to khal and then to Google Calendar,
one calendar per top-level area directory. This file rebuilds that pipeline on a
new Arch box.

It is not one package. Four layers, two of which are **not** in this repository:

| Layer | Location | In git? |
|---|---|---|
| `khal`, `vdirsyncer`, `python`, `python-pipx`, `stow`, `git`, editor | system | installed |
| pipx venv: `khalorg 0.2.1` + `orgparse<0.5` + `patches/khalorg-local-fixes.patch` | `~/.local/share/pipx/venvs/khalorg` | patch only |
| `~/.config/khal/config` (26 calendars), `~/.config/vdirsyncer/config` (25 collections + OAuth client) | home | **no** |
| Org tree, not a git repo (about 46 MB) | `/home/homelab/.local/share/orgmode`, symlinked from `~/.local/share/orgmode` | **no** |
| Runner and calendar map | `dotfiles/orgpush/` | yes |
| systemd units (plain copies, not symlinks) | `dotfiles/systemd/user/` | yes |
| nvim config (including the parallel-pull wrapper), `secrets.lua` | `dotfiles/nvim-lazy/` (stow), secrets untracked | mostly |

Order matters: packages -> pipx + patch -> copy configs -> `discover` -> sync ->
runner -> nvim.

## 1. Packages

```sh
sudo pacman -S --needed khal vdirsyncer python python-pipx stow git neovim
```

## 2. Decide the host's role

`orgpush` exits immediately unless `/etc/hostname` is `homelab` (single-writer
rule; the other machine is read-only). On the new box:

- read-only client: leave the hostname alone and skip the timer in step 7;
- new primary writer: `hostnamectl set-hostname homelab`, retire the old writer,
  or edit the check at the top of `orgpush`.

## 3. dotfiles

```sh
git clone git@github.com:whammou/dotfiles ~/dotfiles
cd ~/dotfiles && ./bootstrap.sh          # stow bash gtk qt kvantum
stow -R -t ~ nvim-lazy                   # ~/.config/nvim -> ~/dotfiles/nvim-lazy/.config/nvim
```

`bootstrap.sh` covers only the theme packages. `nvim-lazy` is stowed by hand.
`systemd/user/*` is not a stow target: the units are copied in step 7.

## 4. Copy the home-only state

These hold the 24 Google collection IDs and the OAuth client; regenerating them
by hand means creating 24 calendars and a new Google Cloud client.

```sh
# on the old machine
rsync -a ~/.config/khal/         new:~/.config/khal/
rsync -a ~/.config/vdirsyncer/   new:~/.config/vdirsyncer/
rsync -a /home/homelab/.local/share/orgmode/ new:/home/homelab/.local/share/orgmode/
```

On the new machine:

```sh
ln -s /home/homelab/.local/share/orgmode ~/.local/share/orgmode
chmod 600 ~/.config/vdirsyncer/config
```

If the username or the org path differs, change `ORG_ROOT`, `HOME` and `PATH` at
the top of `orgpush` to match.

## 5. khalorg and the local patch

```sh
pipx install khalorg==0.2.1
~/.local/share/pipx/venvs/khalorg/bin/python -m pip install "orgparse<0.5"
S=~/.local/share/pipx/venvs/khalorg/lib/python3.14/site-packages
patch -p1 -d "$S" < ~/dotfiles/patches/khalorg-local-fixes.patch
```

The `orgparse` pin is not optional: khalorg declares `orgparse~=0.4`, pipx picks
0.5.x, and 0.5 breaks planning-line reading, which is what makes `SCHEDULED:`
and `DEADLINE:` work at all.

Check the version directory before patching (`ls
~/.local/share/pipx/venvs/khalorg/lib/`); the path above hardcodes `python3.14`.
Details of what the patch changes: `patches/khalorg-local-fixes.md`.

## 6. vdirsyncer: OAuth, then first sync

```sh
vdirsyncer discover gcal     # prints a verification URL; approve with the Google account
vdirsyncer sync gcal         # first run pulls all 25 collections, takes minutes
```

`discover` creates `~/.local/share/vdirsyncer/google_token.json` and the 25
collection directories under `~/.local/share/khal/calendars/`.

`[pair gcal]` must keep `conflict_resolution = "a wins"` (local wins). With
`"b wins"` a remote copy silently overwrites an org-driven local edit on
conflict.

## 7. Runner and timer

```sh
cp ~/dotfiles/systemd/user/orgpush.service ~/.config/systemd/user/
cp ~/dotfiles/systemd/user/orgpush.timer   ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now orgpush.timer
loginctl enable-linger "$USER"      # run the timer without a login session
```

The units are plain copies: editing `dotfiles/systemd/user/*` changes nothing
until they are copied again and `daemon-reload` runs.

`orgpush` exports `HOME=/home/whammou` and an explicit `PATH` because the systemd
user manager starts with a different `HOME`. Adjust both if the new box differs,
and `KHALORG_PY` if the pipx layout differs.

Do not enable `orgpush.timer` and a `minutely@orgpush.timer` on the same host:
the `flock` prevents overlap, but the cadence doubles and the log becomes
misleading.

`orgmode.service` / `orgmode.timer` are a different job (desktop notifications
via `require("partials.org_cron")`). Copy them only if the notification path is
wanted too.

## 8. nvim side

```sh
nvim --headless "+Lazy! sync" +qa
cp ~/.config/nvim/lua/config/secrets.example.lua ~/.config/nvim/lua/config/secrets.lua
$EDITOR ~/.config/nvim/lua/config/secrets.lua   # google.email, client_id, client_secret
```

`secrets.lua` stays untracked (the repo is public). Without it `sync.enabled` is
false: bloocky renders and edits locally, nothing is pushed. The first
`<leader>oBy` runs the plugin's own OAuth flow and stores its token.

Nothing under `~/.local/share/nvim/lazy/bloocky` is patched. The parallel pull
lives in `lua/config/bloocky_parallel.lua` and is applied by the bloocky spec's
`config` function, so `:Lazy update` cannot undo it; see
`patches/bloocky-parallel-pull.md` for how the wrapper works and how to re-check
it after an update (26 calendars should sync in about 2 s, not 13 s).

## 9. Verification

```sh
khal printcalendars | wc -l        # 26
khal list today 7d | head          # real dates, not an empty list
vdirsyncer sync gcal && echo OK
~/.local/share/pipx/venvs/khalorg/bin/python \
  ~/dotfiles/orgpush/delete_orphans.py --root /home/homelab/.local/share/orgmode
bash ~/dotfiles/orgpush/orgpush && tail -20 ~/.local/state/orgpush/log
```

Expected: 26 calendars; a second `orgpush` run finishes in about 80 ms with an
empty log section; the orphan dry run lists nothing. In nvim one `BloockySync`
takes about 2 s with 26 calendars.

End-to-end check: add a heading with `:ID:` and `SCHEDULED:` for tomorrow, run
`orgpush`, confirm the event in `khal list` and in Google Calendar, delete the
heading, run `orgpush` again, confirm the event is gone in both.

## Failure modes seen on this setup

| Symptom | Cause | Fix |
|---|---|---|
| `Storage ... was completely emptied` | vdirsyncer refuses to delete the last item of a collection | delete the event through the API first (`gcal_delete.py`), remove the local `.ics`, then sync that collection |
| Deleted event comes back after sync | vdirsyncer reads a missing local file as "not downloaded yet" | same order: remote delete, local delete, then sync |
| `number of events found ... was not 1 but: 0` | `Calendar.edit` filtered candidates by `is_future` | apply `patches/khalorg-local-fixes.patch` (re-dating fix) |
| `Agenda item date not in the future` aborts a run | unpatched khalorg | same patch |
| orgpush does nothing, log empty | hostname is not `homelab`, or no file is newer than `last-run` | check `/etc/hostname` and `~/.local/state/orgpush/last-run` |
| khalorg cannot find `khal`/`vdirsyncer` under systemd | user manager `HOME` differs | `PATH`/`HOME` exports at the top of `orgpush` |
| bloocky sync slow again | wrapper not applied, or the provider interface changed | confirm `config.bloocky_parallel` runs from the spec; see `patches/bloocky-parallel-pull.md` |

## Known gaps

- Events edited or deleted in Google are not pulled into org. The org file stays
  the source of truth.
- Calendars are synced only when their area's org files change. Phone-side edits
  reach khal on the next org edit in that area, not within the minute.
- Moving a heading between two areas keeps its `:ID:`; the target calendar
  creates a second event and the old one is left behind (not an orphan, since
  the ID still exists).
- `~/.local/share/khalorg/gcal.map.json` keeps 17 stale entries from before the
  per-area split, kept deliberately for rollback.
