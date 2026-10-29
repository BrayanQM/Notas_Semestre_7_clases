import json
import re
from datetime import datetime
from urllib.parse import urlparse

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    navegador = webdriver.Chrome()
    yield navegador
    navegador.quit()


def test_registrar_producto_cerrar_sesion_y_buscarlo(driver):
    base_url = "https://kqrcxvlm-5000.brs.devtunnels.ms/"
    correo = "brayan.quispe.2@gmail.com"
    contrasena = "bolivia123"
    nombre_completo = "Brayan Quispe"
    espera = WebDriverWait(driver, 20)

    nombre_producto = f"RATON {datetime.now():%Y%m%d%H%M%S}"
    descripcion = f"ESCRITORIO CON ESTILO - {nombre_completo}"

    driver.get(base_url)

    # A developer-tunnel warning may appear in a fresh browser profile.
    if driver.find_elements(By.ID, "continue"):
        espera.until(
            EC.element_to_be_clickable((By.ID, "continue"))
        ).click()

    # Let the page finish its initial session/catalog requests before opening login.
    espera.until(
        lambda navegador: navegador.find_element(
            By.ID, "conteo-productos"
        ).text.strip()
    )

    # Iniciar sesión.
    espera.until(EC.element_to_be_clickable((By.ID, "btn-login-publico"))).click()
    espera.until(
        EC.visibility_of_element_located((By.ID, "correo-login"))
    ).send_keys(correo)
    campo_contrasena = espera.until(
        EC.element_to_be_clickable((By.ID, "contrasena-login"))
    )
    campo_contrasena.send_keys(contrasena)
    driver.find_element(
        By.CSS_SELECTOR, "#form-login button[type='submit']"
    ).click()

    # Reportar el mensaje del sitio si el inicio de sesión no es válido.
    espera.until(
        lambda navegador: navegador.find_element(
            By.ID, "vista-app"
        ).is_displayed()
        or navegador.find_element(By.ID, "error-login").text.strip()
    )
    assert driver.find_element(By.ID, "vista-app").is_displayed(), (
        "No se pudo iniciar sesión: "
        + driver.find_element(By.ID, "error-login").text
    )

    # Registrar el producto y comprobar que aparece en el listado interno.
    espera.until(EC.visibility_of_element_located((By.ID, "nombre"))).send_keys(
        nombre_producto
    )
    driver.find_element(By.ID, "descripcion").send_keys(descripcion)
    driver.find_element(By.ID, "precio").send_keys("1.50")
    driver.find_element(By.ID, "cantidad-stock").send_keys("5")
    driver.find_element(By.ID, "unidad-medida").send_keys("unidad")
    driver.find_element(By.ID, "fecha_vencimiento").send_keys("12-31-2030")
    driver.find_element(By.ID, "btn-guardar").click()

    espera.until(
        lambda navegador: any(
            nombre_producto in fila.text
            for fila in navegador.find_elements(
                By.CSS_SELECTOR, "#tbody-productos tr"
            )
        )
    )

    # Cerrar sesión en la aplicación web.
    espera.until(
        EC.element_to_be_clickable((By.ID, "btn-salir"))
    ).click()
    espera.until(EC.visibility_of_element_located((By.ID, "vista-publica")))

    # Descargar todas las páginas del catálogo y buscar el producto desde Python.
    with requests.Session() as cliente:
        pagina = cliente.get(base_url, timeout=20)
        cookie_tunel = re.search(
            r"setCookie\('tunnel_phishing_protection','([^;']+)",
            pagina.text,
        )
        if cookie_tunel:
            cliente.cookies.set(
                "tunnel_phishing_protection",
                cookie_tunel.group(1),
                domain=urlparse(base_url).hostname,
                path="/",
            )

        url_catalogo = f"{base_url.rstrip('/')}/api/catalogo"
        respuesta = cliente.get(
            url_catalogo, params={"pagina": 1}, timeout=20
        )
        assert respuesta.status_code == 200, (
            f"No se pudo cargar el catálogo: HTTP {respuesta.status_code}"
        )
        datos = respuesta.json()
        productos = datos.get("productos", [])

        for numero_pagina in range(2, datos.get("total_paginas", 1) + 1):
            respuesta = cliente.get(
                url_catalogo,
                params={"pagina": numero_pagina},
                timeout=20,
            )
            assert respuesta.status_code == 200, (
                f"No se pudo cargar la página {numero_pagina}: "
                f"HTTP {respuesta.status_code}"
            )
            productos.extend(respuesta.json().get("productos", []))

        producto_encontrado = next(
            (
                producto
                for producto in productos
                if producto.get("nombre") == nombre_producto
            ),
            None,
        )
        assert producto_encontrado is not None, (
            f"No se encontró {nombre_producto!r} entre los "
            f"{len(productos)} productos del catálogo."
        )
        print(f"\nProducto encontrado entre {len(productos)} productos:")
        print(json.dumps(producto_encontrado, ensure_ascii=False, indent=2))
