# Revenue Recognition Tracker

Tools for tracking campaign revenue recognition across SOWs, sub-projects, and Finance invoices.

## Files

- `build_workbook.py` — generates `Revenue Recognition Tracker.xlsx` (Campaigns, Sub-Projects, Monthly Recognition, Invoices - Finance, and Read Me tabs). Requires `openpyxl`.
- `Revenue Recognition Tracker.xlsx` — the generated workbook.
- `Revenue Recognition - Recommendations.md` — write-up of the structural changes made and data-quality issues found in the original source file.
- `dashboard_data.json` — the workbook's data (campaigns, sub-projects, monthly recognition, invoices) exported as JSON, consumed by `build_dashboard.py`.
- `build_dashboard.py` — generates `revenue_recognition_dashboard.html`, a self-contained interactive dashboard (Chart.js + Grid.js, no build step, no server) reading from `dashboard_data.json`.
- `revenue_recognition_dashboard.html` — the generated dashboard. Open directly in a browser.

## Regenerating

```bash
pip install openpyxl
python3 build_workbook.py      # -> Revenue Recognition Tracker.xlsx
python3 build_dashboard.py     # -> revenue_recognition_dashboard.html (reads dashboard_data.json)
```

To refresh the dashboard with new numbers: re-export `dashboard_data.json` from the workbook (one row per record per tab: Campaigns, Sub-Projects (SOWs), Monthly Recognition, Invoices - Finance), then re-run `build_dashboard.py`.

## Editing in the dashboard

Campaign, sub-project, monthly recognition, and invoice fields are inline-editable directly in the dashboard's tables. Edits recalculate earned/open/flex rollups automatically and are saved to the browser's `localStorage` as you go — but that's local to your browser only.

To make an edit permanent and visible to others: click **Download updated dashboard_data.json** in the dashboard, then upload that file to this repo (**Add file → Upload files**, drag it in, commit). GitHub will prompt to replace the existing file since the name matches. Each commit becomes a new version.

## History (past versions)

The dashboard's History section reads this repo's GitHub commit log for `dashboard_data.json` (via the public GitHub API — no auth needed since the repo is public) and can:
- show the full dashboard as it looked as of any past commit date, or
- diff what changed between a past date and the current live data.

This only works when the page is actually hosted on GitHub Pages (or opened as a local file) — GitHub's API calls are blocked inside embedded previews/sandboxes. It also depends on you periodically re-uploading `dashboard_data.json` (see above) so there's commit history to look back on. If the repo is ever renamed or forked, update `REPO_OWNER` / `REPO_NAME` / `REPO_BRANCH` at the top of `build_dashboard.py` and regenerate.

## Notes

- Recalculating the workbook's formulas requires LibreOffice (`soffice`) on the machine running it; see the xlsx skill's `recalc.py` pattern if you wire this into CI.
- This data includes real client budget and invoice figures. Keep that in mind if this repo is public.
