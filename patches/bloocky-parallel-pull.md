# bloocky parallel pull (config module, no source patch)

Implemented in `nvim-lazy/.config/nvim/lua/config/bloocky_parallel.lua` and
applied from the bloocky spec's `config` function in
`nvim-lazy/.config/nvim/lua/plugins/extras/orgmode.lua`. Nothing under
`~/.local/share/nvim/lazy/bloocky` is modified: `:Lazy update` replaces the
plugin and the wrapper is still applied on the next start.

## Why

Every subscribed calendar is one network round trip in the pull phase, and the
plugin pulls them sequentially. With 26 calendars (24 org areas plus Timeblocks
and the primary calendar) that was 12-13 s of waiting.

## How it works

The wrapper sits on the provider interface the orchestrator already calls:

- `discover` is wrapped to remember the calendars the server reported, and to
  reset the per-run cache.
- `fetch` is wrapped so the **first** call of a run starts every subscribed
  calendar at once (one coroutine each), waits for all of them, and caches the
  results. The plugin's sequential loop then serves each following calendar
  from that cache in 0 ms.
- The Google access token is refreshed once before the fan-out: the token call
  is awaitable, and 26 calendars racing it would spend the same refresh token
  in parallel.
- Each calendar keeps its own result slot, including its own error, so the
  plugin's per-calendar reporting is unchanged: one failed calendar is reported
  against its name and does not abort the others.
- Push order is untouched. The fan-out happens at the first pull fetch, after
  the push phase, so no fetched state can be stale with respect to this run's
  own pushes.

## Behavior after the wrapper

- Pull phase: all calendars in parallel, then applied in configuration order.
- State writes (`apply_remote`, blocks, mapping, cursors) stay sequential.
- A calendar the config does not name falls through to the unwrapped `fetch`.

## Numbers on this machine

| | sequential (pristine plugin) | with this wrapper |
|---|---|---|
| 26 calendars, nothing new | 12-13 s | 2.2 s |
| `discover` | 0.6 s | 0.6 s |
| first `fetch` (all 26 calendars) | - | 0.7 s |
| each remaining `fetch` | ~0.5 s | 0 ms |

Measured with `sync.run(nil, done)` in headless nvim while timing
`providers.google.discover` and `providers.google.fetch` individually.

## Re-verify after a plugin update

```sh
nvim --headless -c 'lua dofile("/tmp/bloocky_phase_check.lua")'
```

With the wrapper active: one `fetch` takes a few hundred ms and the remaining
25 take 0 ms. If every `fetch` takes about half a second again, the provider
interface changed: check that `providers.<name>.discover` and `.fetch` still
exist with the same signatures, since that is what this wrapper replaces.

The plugin's own suite still runs against unmodified source
(`396 passed, 0 failed` was the last recorded run).

## History

This used to be a patch against `lua/bloocky/sync/init.lua`
(`bloocky-parallel-pull.patch`, removed). That patch split the pull into
`apply_pull` + `pull_calendars`, which `:Lazy update` silently reverted. The
config module reaches the same effect at the provider layer, which is part of
the plugin's own contract and survives updates.
