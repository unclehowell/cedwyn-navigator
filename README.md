# Cedwyn navigator

The apex landing page and shared webapp navigator for bucklerfamily.estate.

- The landing page opens on a compact dashboard built from the site's live /areas.json registry.
- Gauges show the registry's area, webapp and Worker counts. The bar chart groups webapps by registry category; the scatter plot maps slot to category.
- Selecting any gauge, bar or scatter point opens a Docs modal with the fixed address https://bucklerfamily.estate/docs/.
- The app selector and previous / next controls keep the 1–59 navigation loop available. The selected webapp opens in the frame; Dashboard returns to the control panel.
- The live registry is fetched from https://bucklerfamily.estate/areas.json. registry-snapshot.json is a preview/offline fallback only.
- apps.json is retained as the earlier migration manifest; it is not used for dashboard metrics or the live navigation list.

The dashboard visualises the public navigation registry only. The central evidence catalogue database is not yet wired into this repository, so no evidence-record totals or research metrics are presented here.

Preview: https://cedwyn-navigator.sites.tab.bot/ · Plan: issue #188 on unclehowell/cedwyn. Never force-push.
