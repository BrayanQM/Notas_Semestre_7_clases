#!/usr/bin/env bash
# Uso: capture_terminal.sh "TITULO" "salida.png" "comando a ejecutar en la terminal"
TITLE="$1"
OUT="$2"
CMD="$3"

export DISPLAY=:1
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000

kitty --start-as=fullscreen \
  -o background_opacity=1.0 \
  -o dynamic_background_opacity=no \
  -o background=#101010 \
  -o foreground=#f0f0f0 \
  -o font_size=15 \
  --title "$TITLE" \
  -e bash -lc "$CMD; echo; echo '  ------------------------------------------------------------------'; echo '  [captura de resultados - hito 3 testing]'; sleep 45" >/dev/null 2>&1 </dev/null &
KPID=$!

sleep 8
spectacle -b -n -o "$OUT" >/dev/null 2>&1 </dev/null
sleep 1
kill "$KPID" 2>/dev/null
pkill -f "$TITLE" 2>/dev/null
echo "captura guardada: $OUT"
