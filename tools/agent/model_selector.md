Model selector design

Purpose
- Provide a single, simple contract for routing model calls between local and cloud inference.
- Keep adapters small and replaceable so local experiments and cloud APIs can be swapped without changing callers.

API contract
- callModel(prompt, opts)
  - Behavior: attempt local runner first; if unavailable or fails, fall back to cloud once.
  - Returns: { text: string, model: string, latency_ms: number, source: "local"|"cloud" }

Local runner
- Endpoint: http://localhost:8000/infer
- Expected request: { prompt: string, max_tokens?: number, options?: {} }
- Expected response: { text: string, model: string, duration_ms: number }
- Health check: GET http://localhost:8000/health -> { ok: true }

Cloud adapter
- Implement a thin wrapper at /tools/agent/adapters/cloud_adapter.js
- Responsibilities: rate limiting, retries (1 retry), exponential backoff, and cost logging
- Config: read API keys from environment or repo secrets (do not commit keys)

Logging and audit
- Log each call to /logs/agent_actions.log with timestamp, prompt hash, model used, latency, and outcome
- Do not log full sensitive prompts; store a short hash and metadata only

Fallback and routing policy
- Default: local preferred for routine/low‑quality tasks; cloud preferred for high‑quality outputs
- Implement a simple selector config file: tools/agent/selector_config.json
  - Example:
    {
      "local_preferred": true,
      "local_models": ["local-7b", "local-13b"],
      "cloud_models": ["gpt-4o", "gpt-4o-mini"]
    }

Testing and smoke checks
- Add a smoke test script tools/agent/smoke_test.sh that:
  1) checks local runner health (if configured)
  2) calls callModel with a short prompt and verifies a non-empty response
- CI: run smoke_test only on main before deploy; keep it optional during rapid iteration

Notes
- Keep the model selector minimal and well documented so it can be extended to support routing by cost, latency, or quality later.
- This file is a design contract; implement adapters and the selector in small, testable steps under /tools/agent/.
