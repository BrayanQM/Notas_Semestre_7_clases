#!/usr/bin/env bash
# Uso: capture_vscodium.sh "salida.png" "ruta/archivo" [espera_seg]
OUT="$1"
FILE="$2"
ESPERA="${3:-14}"

export DISPLAY=:1
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000

codium --user-data-dir /tmp/opencode/vscodium-profile \
  --disable-extensions --new-window "$FILE" >/dev/null 2>&1 </dev/null &
PID=$!

sleep "$ESPERA"
spectacle -b -n -o "$OUT" >/dev/null 2>&1 </dev/null
sleep 1
kill "$PID" 2>/dev/null
pkill -f "vscodium-profile" 2>/dev/null
echo "captura guardada: $OUT"
