#!/bin/zsh
set -e

cd "$(dirname "$0")"

PORT="${PORT:-5174}"
while lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; do
  PORT=$((PORT + 1))
done

echo "Starting local preview at http://localhost:${PORT}/"
python3 -m http.server "$PORT" --bind 127.0.0.1 &
SERVER_PID=$!

sleep 1
open "http://localhost:${PORT}/"

echo ""
echo "Preview is running. Close this Terminal window or press Ctrl+C to stop."
trap 'kill "$SERVER_PID" >/dev/null 2>&1 || true' INT TERM EXIT
wait "$SERVER_PID"
