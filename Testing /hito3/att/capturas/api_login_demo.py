import json

import requests

BASE = "http://127.0.0.1:5000"
CORREO = "pedrito@gmail.com"
CONTRASENA = "bolivia123"

print("=" * 62)
print("  PRUEBA DE LOGIN VIA API  -  POST /api/sesion")
print("=" * 62)

cliente = requests.Session()
respuesta = cliente.post(
    f"{BASE}/api/sesion",
    json={"correo": CORREO, "contrasena": CONTRASENA},
)

print(f"URL:     {BASE}/api/sesion")
print(f"Payload: {{'correo': '{CORREO}', 'contrasena': '{CONTRASENA}'}}")
print(f"Status:  {respuesta.status_code}")
print("Respuesta:")
print(json.dumps(respuesta.json(), indent=2, ensure_ascii=False))

verificacion = cliente.get(f"{BASE}/api/sesion")
print("-" * 62)
print(f"GET /api/sesion (sesion activa) -> {verificacion.status_code}")
print(json.dumps(verificacion.json(), indent=2, ensure_ascii=False))

assert respuesta.status_code == 200
assert respuesta.json()["perfil"] == "Gerente"
print("=" * 62)
print("  RESULTADO: LOGIN EXITOSO  (pedrito@gmail.com -> Gerente)")
print("=" * 62)
