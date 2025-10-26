// water/static/water/js/control.js

// --- State ---
let currentRunId = null;

// --- GPS helper ---
async function getGPS() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Geolocation not supported"));
    }
    navigator.geolocation.getCurrentPosition(
      pos => resolve({
        lat: pos.coords.latitude,
        lng: pos.coords.longitude
      }),
      err => reject(err),
      { enableHighAccuracy: true, timeout: 10000 }
    );
  });
}

// --- CSRF helper (for Django) ---
function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let c of cookies) {
    const cookie = c.trim();
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return "";
}

// --- API helper ---
const api = {
  async post(url, data) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      credentials: "include",
      body: JSON.stringify(data)
    });
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return response.json();
  }
};

// --- Run control ---
async function startRun(outletId) {
  try {
    const pos = await getGPS();
    const payload = {
      outlet_id: outletId,
      gps_lat_start: pos.lat,
      gps_lng_start: pos.lng
    };
    const run = await api.post("/api/runs/", payload);
    showCurrentRun(run.id, outletId, pos, run.started_at);
  } catch (err) {
    console.error("Failed to start run:", err);
    alert("Could not start run. Please try again.");
  }
}

async function stopRun(runId, temperatureC) {
  try {
    const pos = await getGPS();
    const payload = {
      gps_lat_end: pos.lat,
      gps_lng_end: pos.lng
    };
    if (temperatureC !== undefined) {
      payload.temperature_c = temperatureC;
    }

    const resp = await fetch(`/api/runs/${runId}/stop/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      credentials: "include",
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      console.error("Stop run failed", resp.status);
      alert("⚠️ Could not stop run. Please try again.");
      return;
    }

    const data = await resp.json();
    finishCurrentRun(data);
  } catch (err) {
    console.error("Failed to stop run:", err);
    alert("⚠️ Could not stop run. Please try again.");
  }
}

// --- UI updates ---
function showCurrentRun(runId, outletId, pos, startedAt) {
  currentRunId = runId;

  // Toggle UI
  const idle = document.getElementById("idle-state");
  const active = document.getElementById("active-state");
  if (idle) idle.classList.add("d-none");
  if (active) active.classList.remove("d-none");

  // Update outlet label
  const outletLabel = document.getElementById("outlet-label");
  if (outletLabel) outletLabel.innerText = `Outlet #${outletId}`;

  // Start timer using shared helper
  const timerEl = document.getElementById("timer");
  if (timerEl) {
    const started = startedAt ? new Date(startedAt) : new Date();
    const initialElapsed = Math.floor((Date.now() - started.getTime()) / 1000);
    startTimerFor(timerEl, runId, initialElapsed);
  }

  console.log("Run started:", runId, "Outlet:", outletId, "GPS:", pos);
}

function finishCurrentRun(result) {
  // Stop timer using shared helper
  const timerEl = document.getElementById("timer");
  if (timerEl) {
    stopTimerFor(currentRunId, timerEl, result.duration_seconds || 0);
  }

  currentRunId = null;

  // Reset UI
  const active = document.getElementById("active-state");
  const idle = document.getElementById("idle-state");
  if (active) active.classList.add("d-none");
  if (idle) idle.classList.remove("d-none");

  console.log("Run stopped:", result);
}

// --- Wire up buttons after DOM loads ---
document.addEventListener("DOMContentLoaded", () => {
  const stopBtn = document.getElementById("stop-btn");
  if (stopBtn) {
    stopBtn.addEventListener("click", () => {
      if (currentRunId) {
        stopRun(currentRunId, 28); // Replace 28 with actual sensor reading
      }
    });
  }

  const pickOutlet = document.getElementById("pick-outlet");
  if (pickOutlet) {
    pickOutlet.addEventListener("click", () => {
      startRun(1); // demo: start outlet #1
    });
  }

  const nextBtn = document.getElementById("next");
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      alert("Next outlet queued (demo)");
    });
  }
});
