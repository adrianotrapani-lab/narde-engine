// Call undo endpoint and update dice UI and board
async function undoLastMoves(steps = 1) {
  try {
    const resp = await fetch('/api/undo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ steps })
    });
    const data = await resp.json();

    if (!data.valid) {
      console.warn('Undo rejected:', data.reason);
      // show user-friendly message in UI
      showToast(data.reason || 'Undo failed');
      return;
    }

    // Example server response fields used:
    // data.restored_consumed_die_indices -> [0,1,...]
    // data.used -> [bool,bool]
    // data.board -> new board state
    // data.move_reverted -> last move object

    // 1) Update local used array from server (authoritative)
    if (Array.isArray(data.used)) {
      window.gameState = window.gameState || {};
      window.gameState.used = data.used.slice();
    }

    // 2) Re-enable dice by index (server returned indices that were re-enabled)
    const restored = Array.isArray(data.restored_consumed_die_indices) ? data.restored_consumed_die_indices : [];
    restored.forEach(idx => {
      // defensive: ignore out-of-range indices
      if (typeof idx !== 'number') return;
      setDieEnabled(idx, true);
    });

    // 3) Also ensure UI reflects the authoritative used array
    if (window.gameState && Array.isArray(window.gameState.used)) {
      window.gameState.used.forEach((u, i) => setDieEnabled(i, !u));
    }

    // 4) Update board UI with server-provided board snapshot
    if (data.board) {
      renderBoard(data.board);
    }

    // 5) Optionally show which move was reverted
    if (data.move_reverted) {
      showToast('Undid move: ' + formatMove(data.move_reverted));
    } else {
      showToast('Undo successful');
    }
  } catch (err) {
    console.error('Undo request failed', err);
    showToast('Network error while undoing move');
  }
}

// Helper: enable or disable a die element by index
function setDieEnabled(index, enabled) {
  const el = document.getElementById(`die-${index}`);
  if (!el) return;
  if (enabled) {
    el.classList.remove('die-disabled');
    el.removeAttribute('aria-disabled');
  } else {
    el.classList.add('die-disabled');
    el.setAttribute('aria-disabled', 'true');
  }
}

// Helper: render board (replace with your renderer)
function renderBoard(board) {
  // Example: update a JSON debug area or call your existing renderer
  const el = document.getElementById('board-json');
  if (el) el.textContent = JSON.stringify(board);
  // If you have a full renderer, call it here instead
  // myBoardRenderer.update(board);
}

// Small UI helpers
function showToast(msg) {
  // Replace with your toast/notification system
  console.info('TOAST:', msg);
}
function formatMove(m) {
  return `${m.from.r},${m.from.c} → ${m.to.r},${m.to.c}`;
}
