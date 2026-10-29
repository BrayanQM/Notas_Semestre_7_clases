import re
from urllib.parse import urlparse

import pytest
import requests


BASE_URL = "https://kqrcxvlm-5000.brs.devtunnels.ms"
CORREO = "brayan.quispe.2@gmail.com"
CONTRASENA = "bolivia123"


def test_comprador_no_puede_registrar_venta():
    with requests.Session() as cliente:
        pagina = cliente.get(f"{BASE_URL}/", timeout=20)
        cookie_tunel = re.search(
            r"setCookie\('tunnel_phishing_protection','([^;']+)",
            pagina.text,
        )
        if cookie_tunel:
            cliente.cookies.set(
                "tunnel_phishing_protection",
                cookie_tunel.group(1),
                domain=urlparse(BASE_URL).hostname,
                path="/",
            )

        login = cliente.post(
            f"{BASE_URL}/api/sesion",
            json={"correo": CORREO, "contrasena": CONTRASENA},
            timeout=20,
        )
        assert login.status_code == 200, (
            f"No se pudo iniciar sesión: HTTP {login.status_code}"
        )
        assert login.json()["rol"] == "compras", (
            "La cuenta usada para esta prueba no tiene rol compras."
        )

        # IDs negativos no corresponden a registros: el intento no debe crear una venta.
        respuesta = cliente.post(
            f"{BASE_URL}/api/ventas",
            json={
                "producto_id": -1,
                "comprador_id": -1,
                "cantidad": 1,
            },
            timeout=20,
        )

    assert respuesta.status_code == 403, (
        f"Se esperaba HTTP 403 para un comprador, se recibió "
        f"HTTP {respuesta.status_code}: {respuesta.text}"
    )
