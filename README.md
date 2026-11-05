# Cedwyn navigator (webapp 60)

The landing page and shared header of cedwyn.bucklerfamily.estate as its own repository: it loads each of the 59 webapps,
one at a time, inside a single frame, with previous / next and a menu ("NN of 59").

- `apps.json` is the manifest: slot, id, title, the webapp's own repository and the URL the frame loads. A webapp that has
  moved to its own repository (`unclehowell/cedwyn-<id>`) loads from its Cloudflare Pages preview; the rest load their live
  page until they move. The migration updates this file on every run.
- Phase 2 brings the central catalogue database (branch `catalogue-db` on unclehowell/cedwyn) and display settings in here;
  then this becomes the apex landing page.

Preview: https://cedwyn-navigator.sites.tab.bot/ · Plan: issue #188 on unclehowell/cedwyn. Never force-push.
