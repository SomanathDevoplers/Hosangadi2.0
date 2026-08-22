#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKFLOW="$SCRIPT_DIR/backend/printer_server/gstMonthlyWorkflow.js"

if ! command -v node >/dev/null 2>&1; then
  echo "FAILED: Node.js is not available on PATH." >&2
  exit 127
fi

echo "Starting the GST monthly workflow..."
node "$WORKFLOW" --manual "$@"
EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 0 ]; then
  echo "GST monthly workflow finished successfully."
else
  echo "GST monthly workflow failed with exit code $EXIT_CODE." >&2
fi

exit "$EXIT_CODE"
