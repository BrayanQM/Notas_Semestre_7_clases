#!/usr/bin/env bash
# Uso: capture_browser.sh "salida.png" "comando que abre el navegador" [espera_seg]
OUT="$1"
CMD="$2"
ESPERA="${3:-14}"

export DISPLAY=:1
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000

bash -lc "$CMD" >/dev/null 2>&1 </dev/null &
PID=$!

sleep "$ESPERA"
spectacle -b -n -o "$OUT" >/dev/null 2>&1 </dev/null
# Espera a que el script termine (guarda su propia captura del navegador).
wait "$PID" 2>/dev/null
pkill -f "selenium_login_demo" 2>/dev/null
pkill -f "brave-origin-nightly" 2>/dev/null
echo "captura guardada: $OUT"
