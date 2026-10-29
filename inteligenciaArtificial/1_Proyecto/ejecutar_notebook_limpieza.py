#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecuta el notebook de limpieza en local (para verificar que funciona y para
guardar las salidas de ejemplo) y deja los archivos generados en data/.

El notebook sigue siendo 100% ejecutable en Google Colab: aqui solo se
sustituye la subida de archivo por la copia local de archive.zip.
"""

import os
import shutil
import subprocess
import sys
import tempfile

from nbclient import NotebookClient
from nbformat import read

BASE = os.path.dirname(os.path.abspath(__file__))
NB = os.path.join(BASE, "Limpieza_FIFA2026_Colab.ipynb")
ZIP_ORIGEN = "/home/eynor/Downloads/archive.zip"
DATA = os.path.join(BASE, "data")


def main():
    tmp = tempfile.mkdtemp(prefix="limpieza_")
    shutil.copyfile(ZIP_ORIGEN, os.path.join(tmp, "archive.zip"))
    nb = read(NB, as_version=4)

    cliente = NotebookClient(
        nb,
        timeout=300,
        kernel_name="python3",
        resources={"metadata": {"path": tmp}},
    )
    cliente.execute()

    with open(NB, "w", encoding="utf8") as f:
        import nbformat
        nbformat.write(nb, f)

    os.makedirs(DATA, exist_ok=True)
    shutil.copyfile(ZIP_ORIGEN, os.path.join(DATA, "archive.zip"))
    for f in ("teams_limpio.csv", "variables_modelo.csv", "codigos_equipos.csv"):
        origen = os.path.join(tmp, f)
        if os.path.exists(origen):
            shutil.copyfile(origen, os.path.join(DATA, f))
            print("generado:", f)
        else:
            print("NO se genero:", f)

    print("\n--- salidas del notebook ---")
    for celda in nb.cells:
        if celda.cell_type != "code":
            continue
        for salida in celda.get("outputs", []):
            if salida.output_type == "stream":
                print(salida.text.rstrip())
            elif salida.output_type in ("execute_result", "display_data"):
                print(salida.get("data", {}).get("text/plain", "")[:2000])
            elif salida.output_type == "error":
                print("ERROR:", salida.ename, salida.evalue)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
