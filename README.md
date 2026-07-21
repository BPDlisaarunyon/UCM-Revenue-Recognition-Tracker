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

## Notes

- The dashboard is a static snapshot — it has no live connection to the `.xlsx` file. Re-run `build_dashboard.py` after updating the data to refresh it.
- Invoice status changes made inside the dashboard (Not Yet Sent / Sent to Finance / Confirmed) are saved to the browser's `localStorage` only — they don't write back to `dashboard_data.json` or the workbook.
- Recalculating the workbook's formulas requires LibreOffice (`soffice`) on the machine running it; see the xlsx skill's `recalc.py` pattern if you wire this into CI.
