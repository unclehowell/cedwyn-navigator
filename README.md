# Cedwyn navigator (webapp 60)

The landing page and shared header of bucklerfamily.estate as its own repository: it loads each of the 59 webapps,
one at a time, inside a single frame, with previous / next (a loop: → on 59 opens 1, ← on 1 opens 59) and a menu ("NN of 59").

- The numbers are the site's own. They come from the same registry every webapp page reads (`/areas.json` "nav", built by
  unclehowell/cedwyn `tools/site.py`; rules in its docs/NAV.md). On bucklerfamily.estate the page reads `/areas.json` itself
  when it carries all 59 slots once each; anywhere else, or before then, it reads `apps.json`.
- `apps.json` is built by `tools/build_apps.py` (live `/areas.json` + `themes.json` slots + `data/coming-soon.json` +
  `split-repos.json` at a cedwyn ref). Every webapp loads from its path on bucklerfamily.estate (paths, never subdomains).
  Each row shows whether the webapp has its own repository and its own data store (a derived copy of what it needs from the
  central catalogue, refreshed on a schedule), or that it needs none because it cites no catalogue records.
  Repositories with no slot yet are listed under `unregistered`; they get a number only through the site's registry.
- Rebuild: `python3 tools/build_apps.py --ref <cedwyn ref>` (keeps the store fields of the previous apps.json;
  `--status file.json` replaces them). It refuses to write unless slots 1–59 are each taken exactly once.

Plan: issue #188 on unclehowell/cedwyn. Never force-push.
