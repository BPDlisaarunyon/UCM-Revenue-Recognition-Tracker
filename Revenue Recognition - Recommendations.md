# Revenue Recognition: Recommendations

Your current sheet mixes three different things in one wide grid: the campaign budget, the SOW/task budgets under it, and 20 columns of Fee/Expense by month. That structure is why it's hard to see flex availability or hand a clean list to Finance — every answer requires scanning across the whole row. The attached workbook (`Revenue Recognition Tracker.xlsx`) splits those into four linked tabs.

## The core change: separate the three layers

**Campaigns** (the flex pool) — one row per campaign, showing total budget, how much is allocated to sub-projects, and — critically — **Available to Reallocate**, calculated automatically as budget minus allocated. Right now this number doesn't exist anywhere in your file; you'd have to add up every SOW under a campaign by hand to know if you have room to move funds. In the new tab it's a live formula.

**Sub-Projects (SOWs)** — one row per SOW/task, tied to its campaign by ID. Earned-to-date pulls automatically from the monthly data instead of being typed in.

**Monthly Recognition** — this is the biggest structural change. Instead of 20 wide columns (Nov Fee, Nov Expense, Dec Fee, Dec Expense...), it's one row per SOW per month. Adding a new month means adding rows, not inserting columns across every campaign block — which is almost certainly why your original file has missing formulas and #REF! errors in several spots (a column insert upstream breaks a hardcoded reference downstream).

**Invoices - Finance** — a dedicated list of invoice numbers, the campaign/SOW they tie to, the amount, and a status flag (Not Yet Sent / Sent / Confirmed). This is the page you hand to Finance each period — filter to "Not Yet Sent" and that's your to-do list.

## What this fixes for your three stated problems

**Tracking sub-projects within a campaign budget:** the Campaigns tab rolls up every SOW automatically — no manual re-totaling when a new SOW gets added.

**Seeing flex availability:** "Available to Reallocate" is a formula, not something you calculate mentally. If a campaign is fully allocated, it shows $0; if there's room, the number is right there.

**Communicating to Finance:** the Invoices - Finance tab is the one artifact you send them — it's not buried in a 50-column spreadsheet.

## What I found while rebuilding it

Going through your file to reorganize it surfaced a few things worth your attention (all flagged in yellow in the workbook's Read Me tab):

Only 2 of your 7 campaigns (Haas F1 Partnership and Comms AOR) have invoice numbers tied to the revenue at all. Everywhere else — Brand Campaign Creative, Cancer Center Pavilion, U.S. News, Strategic Counsel — the monthly fee/expense numbers exist but were never linked to an invoice #. That's likely the single biggest reason it's hard to tell Finance what to apply revenue to: for most of your campaigns, that link was never captured in the first place, not just poorly organized.

"Campaign UCMC-010" is used as the ID for two different campaigns (Strategic Counsel & Advisory Support, and Comms AOR). I split them into separate IDs (CMP-06, CMP-07) — worth confirming whether that was a typo or whether those two are actually meant to share one flex pool.

Cancer Center Pavilion and Haas F1 Partnership had broken-reference (#REF!) errors in the Revised Budget cells of your original file — those totals were effectively gone. I rebuilt Cancer Center Pavilion's total as the sum of its sub-projects ($2,215,000); worth confirming that matches the actual approved budget.

The Landing Page Design SOW (26-UCMC-050) has revenue earned ($1,032.50) but no budget was ever entered for it.

Comms AOR's campaign-level budget was never set in the source file — I reconstructed $255,153.50 from the known monthly invoices, but you should confirm the real contracted number with the SOW.

## Suggested next steps

Open the Read Me tab first — it's a legend plus the full list of flags above. Then spend a few minutes confirming the reconstructed budgets (Cancer Center Pavilion, Comms AOR, Landing Page Design) and assigning invoice numbers to the revenue currently marked "Not yet assigned" in Monthly Recognition. Once those are cleaned up, updating the workbook each month is just adding new rows to Monthly Recognition — everything else recalculates on its own.
