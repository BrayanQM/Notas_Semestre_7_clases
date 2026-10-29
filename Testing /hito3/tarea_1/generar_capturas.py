# -*- coding: utf-8 -*-
"""Genera las capturas de la ejecucion real de pytest para el informe."""
import os

from render_terminal import ejecutar, renderizar

AQUI = os.path.dirname(os.path.abspath(__file__))
PYTHON = "/tmp/opencode/venv_tarea1/bin/python"
CAPTURAS = os.path.join(AQUI, "capturas")

CASOS = [
    ("captura_01_suite_completa.png", "Unit Tests - Suite completa (25 casos)",
     "", ""),
    ("captura_02_validar_precio.png", "validar_precio() - 5 casos",
     "-k", "validar_precio"),
    ("captura_03_validar_cantidad.png", "validar_cantidad() - 5 casos",
     "-k", "validar_cantidad"),
    ("captura_04_venta_registrar.png", "VentaRepository.registrar() - 5 casos",
     "-k", "venta_registrar"),
    ("captura_05_iniciar_sesion.png", "app.iniciar_sesion() - 5 casos",
     "-k", "iniciar_sesion"),
    ("captura_06_requiere_rol.png", "app.requiere_rol() - 5 casos",
     "-k", "requiere_rol"),
]


def main():
    os.makedirs(CAPTURAS, exist_ok=True)
    for archivo, titulo, bandera, valor in CASOS:
        comando = f"{PYTHON} -m pytest test_funciones_criticas.py -v --color=yes"
        if bandera:
            comando += f" {bandera} {valor}"
        salida = ejecutar(comando, AQUI)
        ruta = os.path.join(CAPTURAS, archivo)
        renderizar(salida, titulo, ruta)
        print("Generada:", ruta)


if __name__ == "__main__":
    main()
