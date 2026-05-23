// DiceUndo.jsx
import React, { useState } from "react";
import "./dice.css"; // includes .die, .die-disabled, .reenabled animation

export default function DiceUndo({ initialUsed = [false, false], onBoardUpdate }) {
  const [used, setUsed] = useState(initialUsed);
  const [busy, setBusy] = useState(false);

  async function undoLastMoves(steps = 1) {
    if (busy) return;
    setBusy(true);
    try {
      const res = await fetch("/api/undo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ steps }),
      });
      const data = await res.json();
      if (!data.valid) {
        console.warn("Undo rejected:", data.reason);
        alert(data.reason || "Undo failed");
        setBusy(false);
        return;
      }

      // 1) Apply authoritative used array
      if (Array.isArray(data.used)) {
        setUsed(data.used.slice());
      }

      // 2) Animate re-enabled dice
      const restored = Array.isArray(data.restored_consumed_die_indices) ? data.restored_consumed_die_indices : [];
      restored.forEach((idx) => animateDieReenable(idx));

      // 3) Update board via callback
      if (data.board && typeof onBoardUpdate === "function") {
        onBoardUpdate(data.board);
      }

      alert(data.move_reverted ? `Undid: ${formatMove(data.move_reverted)}` : "Undo successful");
    } catch (err) {
      console.error("Undo failed", err);
      alert("Network error while undoing move");
    } finally {
      setBusy(false);
    }
  }

  function animateDieReenable(index) {
    const el = document.getElementById(`die-${index}`);
    if (!el) return;
    el.classList.remove("reenabled");
    // ensure reflow
    void el.offsetWidth;
    el.classList.add("reenabled");
    // also ensure the disabled class is removed (server authoritative will set used)
    el.classList.remove("die-disabled");
  }

  function formatMove(m) {
    return `${m.from.r},${m.from.c} → ${m.to.r},${m.to.c}`;
  }

  return (
    <div className="undo-panel">
      <div className="dice-row">
        {[0, 1].map((i) => (
          <div
            key={i}
            id={`die-${i}`}
            className={`die ${used[i] ? "die-disabled" : ""}`}
            aria-disabled={used[i] ? "true" : "false"}
          >
            {/* Replace with your die face renderer */}
            <span className="die-face">D{i}</span>
          </div>
        ))}
      </div>

      <div className="controls">
        <button onClick={() => undoLastMoves(1)} disabled={busy}>
          Undo 1
        </button>
        <button onClick={() => undoLastMoves(2)} disabled={busy}>
          Undo 2
        </button>
      </div>
    </div>
  );
}
