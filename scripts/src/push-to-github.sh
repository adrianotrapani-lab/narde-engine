#!/bin/sh
set -e

if [ -z "$GITHUB_TOKEN" ]; then
  echo "ERROR: GITHUB_TOKEN secret not found"
  exit 1
fi

cd /home/runner/workspace

echo "Pushing to github.com/adrianotrapani-lab/narde-engine on branch replit-workspace..."

GIT_TERMINAL_PROMPT=0 git push \
  "https://adrianotrapani-lab:${GITHUB_TOKEN}@github.com/adrianotrapani-lab/narde-engine.git" \
  main:replit-workspace \
  --force

echo "Done! Visit: https://github.com/adrianotrapani-lab/narde-engine/tree/replit-workspace"
