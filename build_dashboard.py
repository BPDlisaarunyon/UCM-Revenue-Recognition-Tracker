import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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
  .rrt-select { font-size: 12.5px; padding: 6px 10px; border: 1px solid #d5d5d5; border-radius: 6px; background: #fff; }
  .rrt-flag { background: #fff8e1; border: 1px solid #f0d878; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; font-size: 13px; }
  .rrt-flag b { display: block; margin-bottom: 3px; }
  .gridjs-wrapper { border-radius: 8px !important; }
  .gridjs-th { font-size: 12px !important; background: #f5f5f5 !important; }
  .gridjs-td { font-size: 12.5px !important; }
  .rrt-status-select { font-size: 12px; padding: 3px 6px; border-radius: 5px; border: 1px solid #ccc; }
  .rrt-note { font-size: 11.5px; color: #888; margin-top: 8px; }
</style>

<div class="rrt-wrap">
  <div class="rrt-h1">Revenue recognition dashboard</div>
  <p class="rrt-sub">Snapshot from Revenue Recognition Tracker.xlsx. Not connected to the workbook &mdash; refresh this artifact after you update the file to see new numbers.</p>

  <div class="rrt-kpis" id="kpis"></div>

  <div class="rrt-section">
    <h2>Budget, earned, and open by campaign</h2>
    <p class="desc">Bars show total budget, revenue earned to date, and revenue still open per campaign.</p>
    <div style="position: relative; width: 100%; height: 320px;">
      <canvas id="campaignChart" role="img" aria-label="Grouped bar chart of budget, earned, and open revenue for each campaign"></canvas>
    </div>
  </div>

  <div class="rrt-section">
    <h2>Campaigns &mdash; flex availability</h2>
    <p class="desc">Available to Reallocate is budget minus everything already allocated to that campaign's sub-projects. $0 means the flex pool is fully committed.</p>
    <div id="campaignsGrid"></div>
  </div>

  <div class="rrt-section">
    <h2>Sub-projects (SOWs)</h2>
    <p class="desc">Filter to one campaign to see its sub-project breakdown.</p>
    <div class="rrt-controls">
      <select class="rrt-select" id="campaignFilter"></select>
    </div>
    <div id="subGrid"></div>
  </div>

  <div class="rrt-section">
    <h2>Invoices &mdash; Finance</h2>
    <p class="desc">What to hand to Finance. Status changes here are saved locally in this dashboard for your own tracking &mdash; they do not update the Excel file.</p>
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

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gridjs@5.0.2/dist/theme/mermaid.min.css" />
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js" integrity="sha384-iU8HYtnGQ8Cy4zl7gbNMOhsDTTKX02BTXptVP/vqAWIaTfM7isw76iyZCsjL2eVi" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gridjs@5.0.2/dist/gridjs.umd.js" integrity="sha384-/XXDzxe4FsGiAe50i/u9pY/Vy/uX654MHB1xoc1BJNnH1WXHhqHga9g3q5tF4gj7" crossorigin="anonymous"></script>
<script>
(function() {
  var DATA = __DATA_JSON__;

  function fmt(n) {
    if (n === null || n === undefined || n === '') return '-';
    var num = Number(n);
    if (isNaN(num)) return n;
    return num.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  }

  var campaigns = DATA.campaigns;
  var subprojects = DATA.subprojects;
  var monthly = DATA.monthly;
  var invoices = DATA.invoices;

  var totalBudget = campaigns.reduce(function(s,c){ return s + (c['Revised Budget']||0); }, 0);
  var totalEarned = campaigns.reduce(function(s,c){ return s + (c['Total Earned']||0); }, 0);
  var totalOpen = campaigns.reduce(function(s,c){ return s + (c['Total Open']||0); }, 0);
  var totalFlex = campaigns.reduce(function(s,c){ return s + (c['Available to Reallocate (Flex)']||0); }, 0);
  var unassigned = monthly.filter(function(m){ return m['Invoice #'] === 'Not yet assigned'; })
                           .reduce(function(s,m){ return s + (m['Amount']||0); }, 0);
  var notYetSent = invoices.filter(function(i){ return i['Status'] === 'Not Yet Sent'; }).length;

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

  new Chart(document.getElementById('campaignChart'), {
    type: 'bar',
    data: {
      labels: campaigns.map(function(c){ return c['Campaign ID']; }),
      datasets: [
        { label: 'Budget', data: campaigns.map(function(c){ return Math.round(c['Revised Budget']||0); }), backgroundColor: '#2a78d6' },
        { label: 'Earned', data: campaigns.map(function(c){ return Math.round(c['Total Earned']||0); }), backgroundColor: '#008300' },
        { label: 'Open', data: campaigns.map(function(c){ return Math.round(c['Total Open']||0); }), backgroundColor: '#eda100' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { y: { ticks: { callback: function(v){ return fmt(v); } } } },
      plugins: { legend: { display: true, position: 'top', labels: { boxWidth: 10 } },
                 tooltip: { callbacks: { label: function(ctx){ return ctx.dataset.label + ': ' + fmt(ctx.parsed.y); } } } }
    }
  });

  new gridjs.Grid({
    columns: [
      { name: 'Campaign ID', width: '90px' },
      { name: 'Campaign Name' },
      { name: 'Revised Budget', formatter: (c) => fmt(c) },
      { name: 'Allocated to Sub-Projects', formatter: (c) => fmt(c) },
      { name: 'Available to Reallocate (Flex)', formatter: (c) => fmt(c) },
      { name: 'Total Earned', formatter: (c) => fmt(c) },
      { name: 'Total Open', formatter: (c) => fmt(c) }
    ],
    data: campaigns.map(function(c){
      return [c['Campaign ID'], c['Campaign Name'], c['Revised Budget'], c['Allocated to Sub-Projects'],
              c['Available to Reallocate (Flex)'], c['Total Earned'], c['Total Open']];
    }),
    sort: true, search: true, resizable: true,
    style: { table: { fontSize: '12.5px' } }
  }).render(document.getElementById('campaignsGrid'));

  var campaignFilter = document.getElementById('campaignFilter');
  var options = ['All campaigns'].concat(campaigns.map(function(c){ return c['Campaign ID'] + ' - ' + c['Campaign Name']; }));
  campaignFilter.innerHTML = options.map(function(o,i){ return '<option value="' + (i===0 ? 'All' : campaigns[i-1]['Campaign ID']) + '">' + o + '</option>'; }).join('');

  var subGridInstance = null;
  function renderSubGrid(filterId) {
    var rows = subprojects.filter(function(s){ return filterId === 'All' || s['Campaign ID'] === filterId; });
    var el = document.getElementById('subGrid');
    el.innerHTML = '';
    subGridInstance = new gridjs.Grid({
      columns: [
        { name: 'SOW/Task ID', width: '110px' },
        { name: 'Campaign ID', width: '90px' },
        { name: 'Description' },
        { name: 'Revised Budget', formatter: (c) => fmt(c) },
        { name: 'Earned to Date', formatter: (c) => fmt(c) },
        { name: 'Open', formatter: (c) => fmt(c) },
        { name: 'Status', width: '100px' }
      ],
      data: rows.map(function(s){
        return [s['SOW/Task ID'], s['Campaign ID'], s['Description'], s['Revised Budget'], s['Earned to Date'], s['Open'], s['Status']];
      }),
      sort: true, search: true, resizable: true,
      style: { table: { fontSize: '12.5px' } }
    });
    subGridInstance.render(el);
  }
  renderSubGrid('All');
  campaignFilter.addEventListener('change', function(e){ renderSubGrid(e.target.value); });

  var STATUS_KEY = 'rrt_invoice_status_overrides';
  var overrides = {};
  try { overrides = JSON.parse(localStorage.getItem(STATUS_KEY) || '{}'); } catch(e) {}

  var currentFilter = 'All';
  function renderInvoices() {
    var rows = invoices.filter(function(i){
      var status = overrides[i['Invoice #']] || i['Status'];
      return currentFilter === 'All' || status === currentFilter;
    });
    var el = document.getElementById('invoicesGrid');
    el.innerHTML = '';
    new gridjs.Grid({
      columns: [
        { name: 'Invoice #', width: '120px' },
        { name: 'Campaign' },
        { name: 'SOW/Task ID(s)', width: '110px' },
        { name: 'Period', width: '110px' },
        { name: 'Amount', formatter: (c) => fmt(c) },
        {
          name: 'Status', width: '150px',
          formatter: (_, row) => {
            var invNum = row.cells[0].data;
            var status = overrides[invNum] || row.cells[5].data;
            var select = gridjs.h('select', {
              className: 'rrt-status-select',
              onchange: (e) => {
                overrides[invNum] = e.target.value;
                localStorage.setItem(STATUS_KEY, JSON.stringify(overrides));
              }
            }, ['Not Yet Sent', 'Sent to Finance', 'Confirmed by Finance'].map(function(opt){
              return gridjs.h('option', { value: opt, selected: opt === status }, opt);
            }));
            return select;
          }
        }
      ],
      data: rows.map(function(i){
        return [i['Invoice #'], i['Campaign'], i['SOW/Task ID(s)'], i['Period'], i['Amount'], overrides[i['Invoice #']] || i['Status']];
      }),
      sort: true, search: true, resizable: true,
      style: { table: { fontSize: '12.5px' } }
    }).render(el);
  }
  renderInvoices();

  document.querySelectorAll('.rrt-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      document.querySelectorAll('.rrt-btn').forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      currentFilter = btn.getAttribute('data-filter');
      renderInvoices();
    });
  });

  document.getElementById('unassignedTotal').textContent = fmt(unassigned);

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
})();
</script>
"""

html = html.replace("__DATA_JSON__", data_json)

out_path = os.path.join(SCRIPT_DIR, "revenue_recognition_dashboard.html")
with open(out_path, 'w') as f:
    f.write(html)

print("written", len(html), "bytes to", out_path)
