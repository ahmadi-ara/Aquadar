// timers.js
// Shared timer utilities for Waterman and Supervisor dashboards

// Global registry of active timer intervals
window.timers = window.timers || {};

/**
 * Format seconds into mm:ss
 */
function formatTime(seconds) {
  const total = Number.isFinite(seconds) ? seconds : 0;
  const mins = String(Math.floor(total / 60)).padStart(2, "0");
  const secs = String(total % 60).padStart(2, "0");
  return `${mins}:${secs}`;
}

/**
 * Start a ticking timer for a run.
 * @param {HTMLElement} el - The span element to update
 * @param {number} runId - The run ID
 * @param {number} startingElapsed - Initial elapsed seconds
 */
function startTimerFor(el, runId, startingElapsed) {
  if (!el) return;

  let elapsed = startingElapsed || 0;

  function render() {
    el.textContent = formatTime(elapsed);
  }

  render();

  // Only start if not already running
  if (!window.timers[runId]) {
    window.timers[runId] = setInterval(() => {
      elapsed += 1;
      render();
    }, 1000);
  }
}

/**
 * Stop a ticking timer and freeze it at the final duration.
 * @param {number} runId - The run ID
 * @param {HTMLElement} el - The span element to update
 * @param {number} finalSeconds - Final duration in seconds
 */
function stopTimerFor(runId, el, finalSeconds) {
  if (window.timers[runId]) {
    clearInterval(window.timers[runId]);
    delete window.timers[runId];
  }

  if (!el) {
    el = document.getElementById(`timer-${runId}`);
  }
  if (!el) return;

  const secs = Number.isFinite(finalSeconds) ? finalSeconds : 0;
  el.textContent = formatTime(secs);
}
