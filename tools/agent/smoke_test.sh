#!/usr/bin/env bash
set -euo pipefail

# Simple smoke test for the model selector / local runner.
# - Checks local runner health at http://localhost:8000/health
# - If healthy, posts a short prompt to /infer and verifies a non-empty response
# - If local runner unavailable, verifies presence of cloud adapter file as a fallback

HEALTH_URL="http://localhost:8000/health"
INFER_URL="http://localhost:8000/infer"
PROMPT="Smoke test: please reply OK."

echo "Starting model selector smoke test..."

# Check local runner health
if curl -sSf "$HEALTH_URL" >/dev/null 2>&1; then
  echo "Local runner health check passed at $HEALTH_URL"
  echo "Calling local infer endpoint..."
  RESP=$(curl -sSf -X POST -H "Content-Type: application/json" \
    -d "{\"prompt\":\"$PROMPT\",\"max_tokens\":16}" "$INFER_URL" || true)

  if [ -z "$RESP" ]; then
    echo "ERROR: Empty response from local runner"
    exit 1
  fi

  echo "Local runner returned a response (truncated):"
  echo "${RESP:0:300}"
  echo "Smoke test: SUCCESS (local)"
  exit 0
else
  echo "Local runner not available at $HEALTH_URL"
  # Fallback smoke check: verify cloud adapter exists in repo
  if [ -f tools/agent/adapters/cloud_adapter.js ]; then
    echo "Found cloud adapter at tools/agent/adapters/cloud_adapter.js"
    echo "Smoke test: SUCCESS (cloud adapter present)"
    exit 0
  else
    echo "ERROR: No local runner and no cloud adapter found."
    exit 1
  fi
fi
