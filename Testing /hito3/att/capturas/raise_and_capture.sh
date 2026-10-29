#!/usr/bin/env bash
# Uso: raise_and_capture.sh "ruta/archivo" "salida.png" [espera_seg]
FILE="$1"
OUT="$2"
ESPERA="${3:-25}"
BASE="$(basename "$FILE")"

export DISPLAY=:1
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000

setsid codium --user-data-dir /tmp/opencode/vscodium-profile \
  --disable-extensions --new-window "$FILE" >/dev/null 2>&1 </dev/null &

sleep "$ESPERA"

# Script de KWin para traer al frente la ventana cuyo titulo contiene el archivo.
cat > /tmp/opencode/raise.js <<JS
const clients = workspace.windowList ? workspace.windowList() : workspace.clientList();
for (let i = 0; i < clients.length; i++) {
    const c = clients[i];
    const cap = ((c.caption || "") + "").toString();
    if (cap.indexOf("$BASE") >= 0) {
        c.keepAbove = true;
        workspace.activeWindow = c;
    }
}
JS

qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript \
  /tmp/opencode/raise.js ocraise >/dev/null 2>&1
qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.start >/dev/null 2>&1
sleep 3

spectacle -b -n -o "$OUT" >/dev/null 2>&1 </dev/null
sleep 1

qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript \
  ocraise >/dev/null 2>&1
pkill -f "vscodium-profile" 2>/dev/null
echo "captura guardada: $OUT"
