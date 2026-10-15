#!/usr/bin/env bash
# Stop the VM when the GPU has been idle for IDLE_MINUTES (default 30) and no `pu` job is running.
# Protects the GCP credit from a forgotten GPU VM. Install (as root) with:
#   (crontab -l 2>/dev/null; echo "* * * * * /opt/policy-updates/scripts/idle_shutdown.sh") | crontab -
set -euo pipefail

IDLE_MINUTES="${IDLE_MINUTES:-30}"
STATE_FILE="${STATE_FILE:-/var/tmp/pu_idle_minutes}"

busy=0
if pgrep -f "pu (run|histories)" >/dev/null 2>&1; then busy=1; fi
if command -v nvidia-smi >/dev/null 2>&1; then
  util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | sort -n | tail -1)
  if [ "${util:-0}" -gt 5 ]; then busy=1; fi
fi

if [ "$busy" -eq 1 ]; then
  echo 0 > "$STATE_FILE"
  exit 0
fi

idle=$(( $(cat "$STATE_FILE" 2>/dev/null || echo 0) + 1 ))
echo "$idle" > "$STATE_FILE"
if [ "$idle" -ge "$IDLE_MINUTES" ]; then
  logger "idle_shutdown: GPU idle for ${idle} min, shutting down"
  echo 0 > "$STATE_FILE"
  shutdown -h now
fi
