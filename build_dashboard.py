import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Update these if the repo is ever renamed / forked.
REPO_OWNER = "BPDlisaarunyon"
REPO_NAME = "UCM-Revenue-Recognition-Tracker"
REPO_BRANCH = "main"
DATA_PATH = "dashboard_data.json"

with open(os.path.join(SCRIPT_DIR, "dashboard_data.json")) as f:
    data = json.load(f)

data_json = json.dumps(data)

html = """<div style="color-scheme: light;">
<style>
  :root { color-scheme: light; }
  .rrt-wrap { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color: #1a1a1a; max-width: 1180px; margin: 0 auto; padding: 20px 24px 48px; background: #fafafa; }
  .rrt-h1 { font-size: 20px; font-weight: 600; margin: 0 0 4px; }
  .rrt-sub { font-size: 13px; color: #666; margin: 0 0 20px; }
  .rrt-kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 24px; }
  .rrt-kpi { background: #fff; border: 1px solid #e2e2e2; border-radius: 10px; padding: 14px 16px; }
  .rrt-kpi-label { font-size: 12px; color: #666; margin-bottom: 6px; }
  .rrt-kpi-val { font-size: 22px; font-weight: 600; }
  .rrt-section { background: #fff; border: 1px solid #e2e2e2; border-radius: 10px; padding: 18px 20px; margin-bottom: 20px; }
  .rrt-section h2 { font-size: 15px; font-weight: 600; margin: 0 0 4px; }
  .rrt-section p.desc { font-size: 12.5px; color: #666; margin: 0 0 14px; }
  .rrt-controls { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; align-items: center; }
  .rrt-btn { font-size: 12.5px; padding: 6px 12px; border: 1px solid #d5d5d5; border-radius: 999px; background: #fff; cursor: pointer; color: #333; }
  .rrt-btn.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
  .rrt-btn.primary { background: #1a6ee0; color: #fff; border-color: #1a6ee0; }
  .rrt-select, .rrt-date { font-size: 12.5px; padding: 6px 10px; border: 1px solid #d5d5d5; border-radius: 6px; background: #fff; }
  .rrt-flag { background: #fff8e1; border: 1px solid #f0d878; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; font-size: 13px; }
  .rrt-flag b { display: block; margin-bottom: 3px; }
  .gridjs-wrapper { border-radius: 8px !important; }
  .gridjs-th { font-size: 12px !important; background: #f5f5f5 !important; }
  .gridjs-td { font-size: 12.5px !important; }
  .rrt-cell-input { font-size: 12.5px; padding: 3px 6px; border-radius: 5px; border: 1px solid #ccc; width: 100%; box-sizing: border-box; }
  .rrt-cell-input.num { text-align: right; }
  .rrt-note { font-size: 11.5px; color: #888; margin-top: 8px; }
  .rrt-banner { background: #e6f1fb; border: 1px solid #b5d4f4; border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; font-size: 12.5px; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
  .rrt-banner.history { background: #faeeda; border-color: #efc978; }
  .rrt-diff-item { font-size: 12.5px; padding: 6px 0; border-bottom: 1px solid #eee; }
  .rrt-diff-item .field { color: #666; }
  .rrt-status-msg { font-size: 12px; color: #888; margin-top: 6px; }
</style>

<div class="rrt-wrap">
  <div class="rrt-h1">Revenue recognition dashboard</div>
  <p class="rrt-sub">Edit values directly in the tables below, then use "Save changes" to download an updated data file and re-upload it to GitHub &mdash; that upload becomes a new version you (or the calendar below) can look back on.</p>

  <div id="editBanner"></div>

  <div class="rrt-kpis" id="kpis"></div>

  <div class="rrt-section">
    <h2>Budget, earned, and open by campaign</h2>
    <p class="desc">Bars show total budget, revenue earned to date, and revenue still open per campaign.</p>
    <div style="position: relative; width: 100%; height: 320px;">
      <canvas id="campaignChart" role="img" aria-label="Grouped bar chart of budget, earned, and open revenue for each campaign"></canvas>
    </div>
  </div>

  <div class="rrt-section">
    <h2>Save your changes</h2>
    <p class="desc">Edits here live in this browser only until you save. Saving downloads a data file &mdash; re-upload it to the repo (Add file &rarr; Upload files &rarr; drag in the downloaded file &rarr; Commit) to make it permanent and give the history calendar a new date to show.</p>
    <div class="rrt-controls">
      <button class="rrt-btn primary" id="downloadBtn">Download updated dashboard_data.json</button>
      <button class="rrt-btn" id="copyBtn">Copy JSON to clipboard</button>
      <button class="rrt-btn" id="discardBtn">Discard my local edits</button>
    </div>
    <p class="rrt-status-msg" id="saveStatus"></p>
  </div>

  <div class="rrt-section">
    <h2>History &mdash; view a previous day</h2>
    <p class="desc">Reads this repo's GitHub commit history for <code>dashboard_data.json</code>. Only works when this page is opened on GitHub Pages (or as a local file) &mdash; it's blocked inside embedded previews/sandboxes.</p>
    <div class="rrt-controls">
      <input type="date" class="rrt-date" id="historyDate" />
      <button class="rrt-btn" id="viewHistoryBtn">View full dashboard as of this date</button>
      <button class="rrt-btn" id="diffHistoryBtn">Show what changed since this date</button>
      <button class="rrt-btn" id="returnLiveBtn" style="display:none;">Return to live data</button>
    </div>
    <p class="rrt-status-msg" id="historyStatus"></p>
    <div id="diffResults"></div>
  </div>

  <div class="rrt-section">
    <h2>Campaigns &mdash; flex availability</h2>
    <p class="desc">Available to Reallocate is budget minus everything already allocated to that campaign's sub-projects. Edit Revised Budget, Flex, or Notes directly in the table.</p>
    <div id="campaignsGrid"></div>
  </div>

  <div class="rrt-section">
    <h2>Sub-projects (SOWs)</h2>
    <p class="desc">Filter to one campaign, or reassign a sub-project's Campaign ID to model moving budget between campaigns.</p>
    <div class="rrt-controls">
      <select class="rrt-select" id="campaignFilter"></select>
    </div>
    <div id="subGrid"></div>
  </div>

  <div class="rrt-section">
    <h2>Monthly recognition</h2>
    <p class="desc">One row per SOW per month. Editing Amount here recalculates earned/open everywhere above.</p>
    <div class="rrt-controls">
      <select class="rrt-select" id="monthlyFilter"></select>
    </div>
    <div id="monthlyGrid"></div>
  </div>

  <div class="rrt-section">
    <h2>Invoices &mdash; Finance</h2>
    <p class="desc">What to hand to Finance. Amount is calculated from Monthly Recognition rows tagged with this invoice number.</p>
    <div class="rrt-controls">
      <button class="rrt-btn active" data-filter="All">All</button>
      <button class="rrt-btn" data-filter="Not Yet Sent">Not yet sent</button>
      <button class="rrt-btn" data-filter="Sent to Finance">Sent to Finance</button>
      <button class="rrt-btn" data-filter="Confirmed by Finance">Confirmed</button>
    </div>
    <div id="invoicesGrid"></div>
    <p class="rrt-note">Revenue not yet tied to an invoice number, across all campaigns: <strong id="unassignedTotal"></strong></p>
  </div>

  <div class="rrt-section">
    <h2>Data-quality flags from the original file</h2>
    <p class="desc">Carried over from the Read Me tab in the workbook &mdash; worth resolving before relying on the totals above.</p>
    <div id="flags"></div>
  </div>
</div>
</div>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gridjs@5.0.2/dist/theme/mermaid.min.css" integrity="sha384-jZvDSsmGB9oGGT/4l9bHXGoAv1OxvG/cFmSo0dZaSqmBgvQTKDBFAMftlXTmMbNW" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js" integrity="sha384-iU8HYtnGQ8Cy4zl7gbNMOhsDTTKX02BTXptVP/vqAWIaTfM7isw76iyZCsjL2eVi" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gridjs@5.0.2/dist/gridjs.umd.js" integrity="sha384-/XXDzxe4FsGiAe50i/u9pY/Vy/uX654MHB1xoc1BJNnH1WXHhqHga9g3q5tF4gj7" crossorigin="anonymous"></script>
<script>
(function() {
  var EMBEDDED_DATA = __DATA_JSON__;
  var REPO_OWNER = "__REPO_OWNER__";
  var REPO_NAME = "__REPO_NAME__";
  var REPO_BRANCH = "__REPO_BRANCH__";
  var DATA_PATH = "__DATA_PATH__";
  var STORAGE_KEY = "rrt_state_v2";

  function fmt(n) {
    if (n === null || n === undefined || n === '') return '-';
    var num = Number(n);
    if (isNaN(num)) return n;
    return num.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  }
  function num(n) { var v = Number(n); return isNaN(v) ? 0 : v; }
  function deepClone(o) { return JSON.parse(JSON.stringify(o)); }

  var chartInstance = null;
  var viewingHistory = false;
  var historySnapshot = null;
  var state = null;

  function loadInitialState() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved) return { data: JSON.parse(saved), hadLocalEdits: true };
    } catch (e) {}
    return { data: deepClone(EMBEDDED_DATA), hadLocalEdits: false };
  }

  function saveState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
  }

  function recompute(d) {
    d.subprojects.forEach(function(sp) {
      var earned = d.monthly.filter(function(m){ return m['SOW/Task ID'] === sp['SOW/Task ID']; })
                             .reduce(function(s,m){ return s + num(m.Amount); }, 0);
      sp['Earned to Date'] = earned;
      sp['Open'] = num(sp['Revised Budget']) - earned;
    });
    d.campaigns.forEach(function(c) {
      var subs = d.subprojects.filter(function(s){ return s['Campaign ID'] === c['Campaign ID']; });
      var allocated = subs.reduce(function(s,x){ return s + num(x['Revised Budget']); }, 0);
      var earned = subs.reduce(function(s,x){ return s + num(x['Earned to Date']); }, 0);
      c['Allocated to Sub-Projects'] = allocated;
      c['Available to Reallocate (Flex)'] = num(c['Revised Budget']) - allocated;
      c['Total Earned'] = earned;
      c['Total Open'] = num(c['Revised Budget']) - earned;
    });
    d.invoices.forEach(function(inv) {
      inv['Amount'] = d.monthly.filter(function(m){ return m['Invoice #'] === inv['Invoice #']; })
                                .reduce(function(s,m){ return s + num(m.Amount); }, 0);
    });
  }

  function onEdit() {
    recompute(state);
    saveState();
    renderAll();
  }

  // ---------- KPIs + chart ----------
  function renderKpis(d) {
    var totalBudget = d.campaigns.reduce(function(s,c){ return s + num(c['Revised Budget']); }, 0);
    var totalEarned = d.campaigns.reduce(function(s,c){ return s + num(c['Total Earned']); }, 0);
    var totalOpen = d.campaigns.reduce(function(s,c){ return s + num(c['Total Open']); }, 0);
    var totalFlex = d.campaigns.reduce(function(s,c){ return s + num(c['Available to Reallocate (Flex)']); }, 0);
    var unassigned = d.monthly.filter(function(m){ return m['Invoice #'] === 'Not yet assigned'; })
                               .reduce(function(s,m){ return s + num(m.Amount); }, 0);
    var notYetSent = d.invoices.filter(function(i){ return i['Status'] === 'Not Yet Sent'; }).length;

    var kpiData = [
      { label: 'Total budget across campaigns', val: fmt(totalBudget) },
      { label: 'Total earned to date', val: fmt(totalEarned) },
      { label: 'Total open', val: fmt(totalOpen) },
      { label: 'Available to reallocate (flex)', val: fmt(totalFlex) },
      { label: 'Invoices not yet sent to Finance', val: notYetSent }
    ];
    document.getElementById('kpis').innerHTML = kpiData.map(function(k) {
      return '<div class="rrt-kpi"><div class="rrt-kpi-label">' + k.label + '</div><div class="rrt-kpi-val">' + k.val + '</div></div>';
    }).join('');
    document.getElementById('unassignedTotal').textContent = fmt(unassigned);
  }

  function renderChart(d) {
    if (chartInstance) { chartInstance.destroy(); }
    chartInstance = new Chart(document.getElementById('campaignChart'), {
      type: 'bar',
      data: {
        labels: d.campaigns.map(function(c){ return c['Campaign ID']; }),
        datasets: [
          { label: 'Budget', data: d.campaigns.map(function(c){ return Math.round(num(c['Revised Budget'])); }), backgroundColor: '#2a78d6' },
          { label: 'Earned', data: d.campaigns.map(function(c){ return Math.round(num(c['Total Earned'])); }), backgroundColor: '#008300' },
          { label: 'Open', data: d.campaigns.map(function(c){ return Math.round(num(c['Total Open'])); }), backgroundColor: '#eda100' }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: { y: { ticks: { callback: function(v){ return fmt(v); } } } },
        plugins: { legend: { display: true, position: 'top', labels: { boxWidth: 10 } },
                   tooltip: { callbacks: { label: function(ctx){ return ctx.dataset.label + ': ' + fmt(ctx.parsed.y); } } } }
      }
    });
  }

  // ---------- editable cell helpers ----------
  function textInput(value, onCommit, opts) {
    opts = opts || {};
    return gridjs.h('input', {
      className: 'rrt-cell-input' + (opts.numeric ? ' num' : ''),
      type: opts.numeric ? 'number' : 'text',
      step: opts.numeric ? '0.01' : undefined,
      value: value === null || value === undefined ? '' : value,
      disabled: viewingHistory,
      onchange: function(e) { onCommit(opts.numeric ? Number(e.target.value) : e.target.value); }
    });
  }
  function selectInput(value, options, onCommit) {
    return gridjs.h('select', {
      className: 'rrt-cell-input',
      disabled: viewingHistory,
      onchange: function(e) { onCommit(e.target.value); }
    }, options.map(function(opt){
      return gridjs.h('option', { value: opt, selected: opt === value }, opt);
    }));
  }

  // ---------- grids ----------
  function renderCampaignsGrid(d) {
    var el = document.getElementById('campaignsGrid');
    el.innerHTML = '';
    new gridjs.Grid({
      columns: [
        { name: 'Campaign ID', width: '90px' },
        { name: 'Campaign Name', formatter: (_, row) => viewingHistory ? row.cells[1].data :
            textInput(row.cells[1].data, function(v){
              var c = state.campaigns.find(function(x){ return x['Campaign ID'] === row.cells[0].data; });
              c['Campaign Name'] = v; onEdit();
            }) },
        { name: 'Flex?', width: '70px', formatter: (_, row) => viewingHistory ? row.cells[2].data :
            selectInput(row.cells[2].data, ['Y','N'], function(v){
              var c = state.campaigns.find(function(x){ return x['Campaign ID'] === row.cells[0].data; });
              c['Flex?'] = v; onEdit();
            }) },
        { name: 'Revised Budget', formatter: (_, row) => viewingHistory ? fmt(row.cells[3].data) :
            textInput(row.cells[3].data, function(v){
              var c = state.campaigns.find(function(x){ return x['Campaign ID'] === row.cells[0].data; });
              c['Revised Budget'] = v; onEdit();
            }, { numeric: true }) },
        { name: 'Allocated to Sub-Projects', formatter: (c) => fmt(c) },
        { name: 'Available to Reallocate (Flex)', formatter: (c) => fmt(c) },
        { name: 'Total Earned', formatter: (c) => fmt(c) },
        { name: 'Total Open', formatter: (c) => fmt(c) },
        { name: 'Notes', formatter: (_, row) => viewingHistory ? (row.cells[8].data || '') :
            textInput(row.cells[8].data, function(v){
              var c = state.campaigns.find(function(x){ return x['Campaign ID'] === row.cells[0].data; });
              c['Notes'] = v; onEdit();
            }) }
      ],
      data: d.campaigns.map(function(c){
        return [c['Campaign ID'], c['Campaign Name'], c['Flex?'], c['Revised Budget'], c['Allocated to Sub-Projects'],
                c['Available to Reallocate (Flex)'], c['Total Earned'], c['Total Open'], c['Notes'] || ''];
      }),
      sort: true, search: true, resizable: true,
      style: { table: { fontSize: '12.5px' } }
    }).render(el);
  }

  function renderSubGrid(d, filterId) {
    var rows = d.subprojects.filter(function(s){ return filterId === 'All' || s['Campaign ID'] === filterId; });
    var el = document.getElementById('subGrid');
    el.innerHTML = '';
    var campaignIds = d.campaigns.map(function(c){ return c['Campaign ID']; });
    new gridjs.Grid({
      columns: [
        { name: 'SOW/Task ID', width: '110px' },
        { name: 'Campaign ID', width: '100px', formatter: (_, row) => viewingHistory ? row.cells[1].data :
            selectInput(row.cells[1].data, campaignIds, function(v){
              var s = state.subprojects.find(function(x){ return x['SOW/Task ID'] === row.cells[0].data; });
              s['Campaign ID'] = v; onEdit();
            }) },
        { name: 'Description', formatter: (_, row) => viewingHistory ? row.cells[2].data :
            textInput(row.cells[2].data, function(v){
              var s = state.subprojects.find(function(x){ return x['SOW/Task ID'] === row.cells[0].data; });
              s['Description'] = v; onEdit();
            }) },
        { name: 'Revised Budget', formatter: (_, row) => viewingHistory ? fmt(row.cells[3].data) :
            textInput(row.cells[3].data, function(v){
              var s = state.subprojects.find(function(x){ return x['SOW/Task ID'] === row.cells[0].data; });
              s['Revised Budget'] = v; onEdit();
            }, { numeric: true }) },
        { name: 'Earned to Date', formatter: (c) => fmt(c) },
        { name: 'Open', formatter: (c) => fmt(c) },
        { name: 'Status', width: '110px', formatter: (_, row) => viewingHistory ? row.cells[6].data :
            selectInput(row.cells[6].data, ['Not Started','In Progress','Complete'], function(v){
              var s = state.subprojects.find(function(x){ return x['SOW/Task ID'] === row.cells[0].data; });
              s['Status'] = v; onEdit();
            }) }
      ],
      data: rows.map(function(s){
        return [s['SOW/Task ID'], s['Campaign ID'], s['Description'], s['Revised Budget'], s['Earned to Date'], s['Open'], s['Status']];
      }),
      sort: true, search: true, resizable: true,
      style: { table: { fontSize: '12.5px' } }
    }).render(el);
  }

  function renderMonthlyGrid(d, filterId) {
    var rows = d.monthly.filter(function(m){ return filterId === 'All' || m['SOW/Task ID'] === filterId; });
    var el = document.getElementById('monthlyGrid');
    el.innerHTML = '';
    new gridjs.Grid({
      columns: [
        { name: 'id', hidden: true },
        { name: 'SOW/Task ID', width: '110px' },
        { name: 'Month', width: '80px' },
        { name: 'Type', width: '90px', formatter: (_, row) => viewingHistory ? row.cells[3].data :
            selectInput(row.cells[3].data, ['Fee','Expense'], function(v){
              var m = state.monthly.find(function(x){ return x.id === row.cells[0].data; });
              m['Type'] = v; onEdit();
            }) },
        { name: 'Amount', formatter: (_, row) => viewingHistory ? fmt(row.cells[4].data) :
            textInput(row.cells[4].data, function(v){
              var m = state.monthly.find(function(x){ return x.id === row.cells[0].data; });
              m['Amount'] = v; onEdit();
            }, { numeric: true }) },
        { name: 'Invoice #', formatter: (_, row) => viewingHistory ? row.cells[5].data :
            textInput(row.cells[5].data, function(v){
              var m = state.monthly.find(function(x){ return x.id === row.cells[0].data; });
              m['Invoice #'] = v; onEdit();
            }) },
        { name: 'Notes', formatter: (_, row) => viewingHistory ? (row.cells[6].data || '') :
            textInput(row.cells[6].data, function(v){
              var m = state.monthly.find(function(x){ return x.id === row.cells[0].data; });
              m['Notes'] = v; onEdit();
            }) }
      ],
      data: rows.map(function(m){
        return [m.id, m['SOW/Task ID'], m['Month'], m['Type'], m['Amount'], m['Invoice #'], m['Notes'] || ''];
      }),
      sort: true, search: true, resizable: true,
      style: { table: { fontSize: '12.5px' } }
    }).render(el);
  }

  var invoiceStatusFilter = 'All';
  function renderInvoicesGrid(d) {
    var rows = d.invoices.filter(function(i){ return invoiceStatusFilter === 'All' || i['Status'] === invoiceStatusFilter; });
    var el = document.getElementById('invoicesGrid');
    el.innerHTML = '';
    new gridjs.Grid({
      columns: [
        { name: 'Invoice #', width: '120px' },
        { name: 'Campaign' },
        { name: 'SOW/Task ID(s)', width: '110px' },
        { name: 'Period', width: '110px', formatter: (_, row) => viewingHistory ? row.cells[3].data :
            textInput(row.cells[3].data, function(v){
              var i = state.invoices.find(function(x){ return x['Invoice #'] === row.cells[0].data; });
              i['Period'] = v; onEdit();
            }) },
        { name: 'Amount', formatter: (c) => fmt(c) },
        { name: 'Status', width: '150px', formatter: (_, row) => viewingHistory ? row.cells[5].data :
            selectInput(row.cells[5].data, ['Not Yet Sent', 'Sent to Finance', 'Confirmed by Finance'], function(v){
              var i = state.invoices.find(function(x){ return x['Invoice #'] === row.cells[0].data; });
              i['Status'] = v; onEdit();
            }) }
      ],
      data: rows.map(function(i){
        return [i['Invoice #'], i['Campaign'], i['SOW/Task ID(s)'], i['Period'], i['Amount'], i['Status']];
      }),
      sort: true, search: true, resizable: true,
      style: { table: { fontSize: '12.5px' } }
    }).render(el);
  }

  function renderFlags() {
    var flags = [
      ['Duplicate Campaign ID', '\\u201cCampaign UCMC-010\\u201d was used for both Strategic Counsel & Advisory Support and Comms AOR in the source file. Split into CMP-06 and CMP-07 here.'],
      ['Comms AOR budget reconstructed', 'No top-level budget existed in the source file; the $255,153.50 total shown here is backed into from known invoices. Confirm the real contracted amount.'],
      ['Cancer Center Pavilion budget reconstructed', 'The original Revised Budget cell had a broken reference (#REF!) error. The $2,215,000 shown here is the sum of its sub-projects.'],
      ['Landing Page Design has no budget', 'SOW 26-UCMC-050 has $1,032.50 earned but no Original Budget was ever entered.'],
      ['Most revenue has no invoice number', 'Only Haas F1 Partnership and Comms AOR had invoice numbers captured in the source file. See the unassigned total above.'],
      ['Service Line Campaigns is empty', 'This campaign exists with a $0 budget and no sub-projects were ever itemized under it.']
    ];
    document.getElementById('flags').innerHTML = flags.map(function(f){
      return '<div class="rrt-flag"><b>' + f[0] + '</b>' + f[1] + '</div>';
    }).join('');
  }

  function renderEditBanner() {
    var el = document.getElementById('editBanner');
    if (viewingHistory) {
      el.innerHTML = '<div class="rrt-banner history"><span>Viewing a past snapshot. Editing is disabled.</span></div>';
      return;
    }
    el.innerHTML = '';
  }

  var currentCampaignFilter = 'All';
  var currentMonthlyFilter = 'All';

  function renderAll() {
    var d = viewingHistory ? historySnapshot : state;
    renderEditBanner();
    renderKpis(d);
    renderChart(d);
    renderCampaignsGrid(d);
    renderSubGrid(d, currentCampaignFilter);
    renderMonthlyGrid(d, currentMonthlyFilter);
    renderInvoicesGrid(d);
    renderFlags();
    document.getElementById('returnLiveBtn').style.display = viewingHistory ? 'inline-block' : 'none';
    document.getElementById('downloadBtn').disabled = viewingHistory;
    document.getElementById('copyBtn').disabled = viewingHistory;
  }

  // ---------- init ----------
  var initial = loadInitialState();
  state = initial.data;
  recompute(state);
  if (initial.hadLocalEdits) {
    document.getElementById('editBanner').innerHTML = '<div class="rrt-banner"><span>Showing your locally-saved edits from this browser.</span><button class="rrt-btn" id="discardBannerBtn">Discard and reload original data</button></div>';
  }

  // filters populated once from the embedded campaign/SOW lists (stable regardless of edits to values)
  var campaignFilterEl = document.getElementById('campaignFilter');
  campaignFilterEl.innerHTML = ['<option value="All">All campaigns</option>'].concat(
    state.campaigns.map(function(c){ return '<option value="' + c['Campaign ID'] + '">' + c['Campaign ID'] + ' - ' + c['Campaign Name'] + '</option>'; })
  ).join('');
  campaignFilterEl.addEventListener('change', function(e){ currentCampaignFilter = e.target.value; renderAll(); });

  var monthlyFilterEl = document.getElementById('monthlyFilter');
  monthlyFilterEl.innerHTML = ['<option value="All">All SOWs</option>'].concat(
    state.subprojects.map(function(s){ return '<option value="' + s['SOW/Task ID'] + '">' + s['SOW/Task ID'] + ' - ' + s['Description'] + '</option>'; })
  ).join('');
  monthlyFilterEl.addEventListener('change', function(e){ currentMonthlyFilter = e.target.value; renderAll(); });

  document.querySelectorAll('[data-filter]').forEach(function(btn){
    btn.addEventListener('click', function(){
      document.querySelectorAll('[data-filter]').forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      invoiceStatusFilter = btn.getAttribute('data-filter');
      renderAll();
    });
  });

  function download(filename, text) {
    var blob = new Blob([text], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  document.getElementById('downloadBtn').addEventListener('click', function(){
    download('dashboard_data.json', JSON.stringify(state, null, 2));
    document.getElementById('saveStatus').textContent = 'Downloaded. Now upload this file to your GitHub repo (Add file \\u2192 Upload files) to make it permanent.';
  });
  document.getElementById('copyBtn').addEventListener('click', function(){
    var text = JSON.stringify(state, null, 2);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function(){
        document.getElementById('saveStatus').textContent = 'Copied to clipboard.';
      }, function(){
        document.getElementById('saveStatus').textContent = 'Could not copy automatically \\u2014 use the download button instead.';
      });
    } else {
      document.getElementById('saveStatus').textContent = 'Clipboard not available in this browser \\u2014 use the download button instead.';
    }
  });
  function discardEdits() {
    try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
    state = deepClone(EMBEDDED_DATA);
    recompute(state);
    document.getElementById('editBanner').innerHTML = '';
    document.getElementById('saveStatus').textContent = 'Local edits discarded.';
    renderAll();
  }
  document.getElementById('discardBtn').addEventListener('click', discardEdits);
  document.body.addEventListener('click', function(e){
    if (e.target && e.target.id === 'discardBannerBtn') discardEdits();
  });

  // ---------- history (GitHub commit API) ----------
  function ghApi(path) {
    return fetch('https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + path, {
      headers: { 'Accept': 'application/vnd.github+json' }
    });
  }

  function fetchSnapshotForDate(dateStr, statusEl) {
    statusEl.textContent = 'Looking up the closest commit on or before ' + dateStr + '\\u2026';
    var until = dateStr + 'T23:59:59Z';
    return ghApi('/commits?path=' + encodeURIComponent(DATA_PATH) + '&sha=' + REPO_BRANCH + '&until=' + until + '&per_page=1')
      .then(function(res){
        if (!res.ok) throw new Error('GitHub API returned ' + res.status);
        return res.json();
      })
      .then(function(commits){
        if (!commits.length) throw new Error('No commit found on or before that date.');
        var sha = commits[0].sha;
        var commitDate = commits[0].commit.author.date;
        statusEl.textContent = 'Found commit ' + sha.slice(0,7) + ' from ' + new Date(commitDate).toLocaleString() + '. Fetching data\\u2026';
        return ghApi('/contents/' + encodeURIComponent(DATA_PATH) + '?ref=' + sha).then(function(res){
          if (!res.ok) throw new Error('Could not fetch file at that commit (status ' + res.status + ').');
          return res.json();
        }).then(function(fileInfo){
          var jsonText = decodeURIComponent(escape(atob(fileInfo.content.replace(/\\n/g, ''))));
          var snapshot = JSON.parse(jsonText);
          statusEl.textContent = 'Showing snapshot from commit ' + sha.slice(0,7) + ' (' + new Date(commitDate).toLocaleString() + ').';
          return snapshot;
        });
      });
  }

  document.getElementById('viewHistoryBtn').addEventListener('click', function(){
    var dateStr = document.getElementById('historyDate').value;
    var statusEl = document.getElementById('historyStatus');
    document.getElementById('diffResults').innerHTML = '';
    if (!dateStr) { statusEl.textContent = 'Pick a date first.'; return; }
    fetchSnapshotForDate(dateStr, statusEl).then(function(snapshot){
      historySnapshot = snapshot;
      recompute(historySnapshot);
      viewingHistory = true;
      renderAll();
    }).catch(function(err){
      statusEl.textContent = 'Could not load history: ' + err.message + '. This feature requires the page to be hosted on GitHub Pages (not an embedded preview), and at least one commit to dashboard_data.json before the selected date.';
    });
  });

  document.getElementById('diffHistoryBtn').addEventListener('click', function(){
    var dateStr = document.getElementById('historyDate').value;
    var statusEl = document.getElementById('historyStatus');
    if (!dateStr) { statusEl.textContent = 'Pick a date first.'; return; }
    fetchSnapshotForDate(dateStr, statusEl).then(function(snapshot){
      recompute(snapshot);
      var diffs = [];
      function diffCollection(label, oldArr, newArr, keyField) {
        var oldMap = {}; oldArr.forEach(function(r){ oldMap[r[keyField]] = r; });
        var newMap = {}; newArr.forEach(function(r){ newMap[r[keyField]] = r; });
        Object.keys(newMap).forEach(function(k){
          if (!oldMap[k]) { diffs.push({ label: label, key: k, kind: 'added' }); return; }
          var o = oldMap[k], n = newMap[k];
          Object.keys(n).forEach(function(f){
            if (f === keyField) return;
            if (String(o[f] == null ? '' : o[f]) !== String(n[f] == null ? '' : n[f])) {
              diffs.push({ label: label, key: k, field: f, from: o[f], to: n[f], kind: 'changed' });
            }
          });
        });
        Object.keys(oldMap).forEach(function(k){ if (!newMap[k]) diffs.push({ label: label, key: k, kind: 'removed' }); });
      }
      diffCollection('Campaign', snapshot.campaigns, state.campaigns, 'Campaign ID');
      diffCollection('Sub-project', snapshot.subprojects, state.subprojects, 'SOW/Task ID');
      diffCollection('Monthly row', snapshot.monthly, state.monthly, 'id');
      diffCollection('Invoice', snapshot.invoices, state.invoices, 'Invoice #');

      var el = document.getElementById('diffResults');
      if (!diffs.length) {
        el.innerHTML = '<p class="rrt-status-msg">No differences between that date and the current live data.</p>';
      } else {
        el.innerHTML = diffs.map(function(d){
          if (d.kind === 'added') return '<div class="rrt-diff-item"><b>' + d.label + ' ' + d.key + '</b> was added since then.</div>';
          if (d.kind === 'removed') return '<div class="rrt-diff-item"><b>' + d.label + ' ' + d.key + '</b> no longer exists (existed back then).</div>';
          var fromVal = (typeof d.from === 'number') ? fmt(d.from) : d.from;
          var toVal = (typeof d.to === 'number') ? fmt(d.to) : d.to;
          return '<div class="rrt-diff-item"><b>' + d.label + ' ' + d.key + '</b> <span class="field">' + d.field + '</span>: ' + fromVal + ' &rarr; ' + toVal + '</div>';
        }).join('');
      }
    }).catch(function(err){
      statusEl.textContent = 'Could not load history: ' + err.message + '. This feature requires the page to be hosted on GitHub Pages (not an embedded preview), and at least one commit to dashboard_data.json before the selected date.';
    });
  });

  document.getElementById('returnLiveBtn').addEventListener('click', function(){
    viewingHistory = false;
    historySnapshot = null;
    document.getElementById('historyStatus').textContent = '';
    document.getElementById('diffResults').innerHTML = '';
    renderAll();
  });

  renderAll();
})();
</script>
"""

html = html.replace("__DATA_JSON__", data_json)
html = html.replace("__REPO_OWNER__", REPO_OWNER)
html = html.replace("__REPO_NAME__", REPO_NAME)
html = html.replace("__REPO_BRANCH__", REPO_BRANCH)
html = html.replace("__DATA_PATH__", DATA_PATH)

out_path = os.path.join(SCRIPT_DIR, "revenue_recognition_dashboard.html")
with open(out_path, 'w') as f:
    f.write(html)

print("written", len(html), "bytes to", out_path)
