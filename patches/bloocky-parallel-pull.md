# bloocky parallel pull patch

Applies to the plugin checkout at `~/.local/share/nvim/lazy/bloocky`
(`lua/bloocky/sync/init.lua`). The checkout is not a git repo, so this file plus
`bloocky-parallel-pull.patch` are the only record of the change. `:Lazy update`
replaces the file and silently drops the patch: sync still works, it just costs
about half a second per subscribed calendar again.

## Why

Every subscribed calendar is one network round trip in the pull phase, and the
pull loop was sequential. With 26 calendars (24 org areas plus Timeblocks and
the primary calendar) a sync took 12-13 s, all of it waiting.

## Behavior after this patch

- The pull phase fetches all calendars concurrently, then applies the results
  sequentially in configuration order. State writes (`apply_remote`, blocks,
  mapping, cursors) are untouched by the concurrency: only the fetches overlap.
- Each calendar keeps its own error slot. One calendar failing is reported
  against its name and does not abort or skip the others; a calendar whose
  fetch never completes is reported instead of being silently dropped.
- A Google token refresh happens once before the fan-out, because refreshing is
  a write and 26 calendars racing it would spend the same refresh token in
  parallel.
- Push order is unchanged: the whole push phase still runs before any pull.

## Reapply

```sh
cd ~/.local/share/nvim/lazy/bloocky
patch -p1 < ~/dotfiles/patches/bloocky-parallel-pull.patch
```

Patch and re-verify after any bloocky update: the suite must report
`396 passed, 0 failed`, and a sync with 26 calendars should finish in about
2 s instead of 13 s. If the update touched `sync/init.lua`, the patch may need
rebasing against the new file.

## Numbers on this machine

- Sequential: 12.2 s, 12.8 s, 13.3 s over three runs.
- Parallel: 1.5-1.9 s over five runs, 26 calendars, 26 cursors persisted,
  no errors, no conflicts.
- Correctness spot check: a summary change made on Google landed in the block
  title after one sync (1 updated, same block id) and reverted cleanly on the
  next, with the mapping etag and `SUMMARY` line updating in place and no
  duplicate block or mapping created.
