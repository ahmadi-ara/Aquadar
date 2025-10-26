// External dependencies (load these in your HTML, not here):
// <script src="https://cdn.jsdelivr.net/npm/bootstrap@5/dist/js/bootstrap.bundle.min.js"></script>
// <script src="https://cdn.jsdelivr.net/npm/jalaali-js/dist/jalaali.min.js"></script>

// Translated labels passed from template
const T = window.dashboardConfig.labels;

// Filter anomalies
document.getElementById("filter-anomalies").addEventListener("click", () => {
  document.querySelectorAll("tbody tr").forEach(row => {
    if (!row.classList.contains("table-danger")) {
      row.classList.toggle("d-none");
    }
  });
});

// --- Jalali conversion helper ---
function toJalaliString(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  const gYear = d.getFullYear();
  const gMonth = d.getMonth() + 1;
  const gDay = d.getDate();
  const j = jalaali.toJalaali(gYear, gMonth, gDay);

  const hh = String(d.getHours()).padStart(2, "0");
  const mm = String(d.getMinutes()).padStart(2, "0");
  const ss = String(d.getSeconds()).padStart(2, "0");

  return `${j.jy}/${String(j.jm).padStart(2,"0")}/${String(j.jd).padStart(2,"0")} ${hh}:${mm}:${ss}`;
}

// Initialize existing timers (using shared helpers from timers.js)
document.querySelectorAll(".timer").forEach(el => {
  const runId = el.dataset.runid;
  const elapsed = parseInt(el.dataset.elapsed, 10) || 0;
  const running = el.dataset.running === "true";
  el.textContent = formatTime(elapsed);
  if (running) startTimerFor(el, runId, elapsed);
});

// Render anomaly badges
function renderAnomalyCell(cell, run) {
  let html = "";
  if (run.is_anomalous_short) html += `<span class="badge bg-danger">${T.short}</span> `;
  if (run.is_anomalous_long) html += `<span class="badge bg-danger">${T.long}</span> `;
  if (!run.is_anomalous_short && !run.is_anomalous_long) html += `<span class="badge bg-success">${T.normal}</span>`;
  cell.innerHTML = html;
}

// Find the correct plot tbody for a run
function getPlotTbody(run) {
  return document.querySelector(`#plot-body-${run.outlet.plot}`);
}

// Upsert (insert or update) a run row
function upsertRunRow(run) {
  const rowId = `run-row-${run.id}`;
  let row = document.getElementById(rowId);

  if (!row) {
    const tbody = getPlotTbody(run);
    if (!tbody) return;

    row = document.createElement("tr");
    row.id = rowId;
    row.className = (run.is_anomalous_short || run.is_anomalous_long)
      ? "table-danger"
      : "table-success";

    row.innerHTML = `
      <td data-outlet-number>${run.outlet.number}</td>
      <td data-started-at>${toJalaliString(run.started_at)}</td>
      <td data-temperature>${run.temperature_c ?? ""}°C</td>
      <td data-duration>${run.duration_seconds ? run.duration_seconds + "s" : ""}</td>
      <td><span class="timer" id="timer-${run.id}" data-runid="${run.id}"></span></td>
      <td id="anomaly-${run.id}" data-anomaly-cell></td>
    `;
    tbody.prepend(row);
  }

  // --- Update existing row ---
  row.className = (run.is_anomalous_short || run.is_anomalous_long)
    ? "table-danger"
    : "table-success";

  const startedAtCell = row.querySelector("[data-started-at]");
  const tempCell = row.querySelector("[data-temperature]");
  const durationCell = row.querySelector("[data-duration]");
  const anomalyCell = row.querySelector("[data-anomaly-cell]");
  const timerEl = document.getElementById(`timer-${run.id}`);

  if (startedAtCell) startedAtCell.textContent = toJalaliString(run.started_at);
  if (tempCell) tempCell.textContent = run.temperature_c ? `${run.temperature_c}°C` : "";
  if (durationCell) durationCell.textContent = run.duration_seconds ? (run.duration_seconds + "s") : "";

  renderAnomalyCell(anomalyCell, run);

  // --- Timer logic (using shared helpers) ---
  if (run.ended_at) {
    stopTimerFor(run.id, timerEl, run.duration_seconds || 0);
  } else {
    const initialElapsed = run.elapsed_seconds ?? 0;
    startTimerFor(timerEl, run.id, initialElapsed);
  }
}

// Polling: fetch runs and upsert rows
async function refreshRuns() {
  try {
    const resp = await fetch("/api/runs/");
    if (!resp.ok) return;
    const runs = await resp.json();
    runs.forEach(run => upsertRunRow(run));
  } catch (err) {
    console.error("Polling error", err);
  }
}

setInterval(refreshRuns, 10000);

// Persist active tabs
document.querySelectorAll('button[data-bs-toggle="tab"]').forEach(tab => {
  tab.addEventListener("shown.bs.tab", e => {
    localStorage.setItem("activeTabId", e.target.id);
  });
});

const activeTabId = localStorage.getItem("activeTabId");
if (activeTabId) {
  const tab = document.getElementById(activeTabId);
  if (tab) {
    const bsTab = new bootstrap.Tab(tab);
    bsTab.show();
  }
}
