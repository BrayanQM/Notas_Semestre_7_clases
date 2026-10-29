#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recalcula los numeros de pagina del indice (campo TOC) del documento .docx.

El indice del documento original conservaba numeros de pagina de una version
anterior (por ejemplo "CAPITULO 2 ... 1"), por lo que no coincidian con la
paginacion real. Este script:

  1. Convierte el .docx a PDF con LibreOffice.
  2. Localiza en que pagina real aparece cada titulo del indice.
  3. Reescribe el valor cacheado de cada entrada del TOC (campo PAGEREF).
  4. Vuelve a generar el PDF final con el indice ya corregido.

La numeracion sigue el esquema que el propio documento usa: cada capitulo
arranca en 1 (capitulo 1 -> paginas 1..n, capitulo 2 -> paginas 1..m).

Uso:  python3 ajustar_indice.py
"""

import copy
import os
import re
import shutil
import subprocess
import sys
import tempfile

from docx import Document
from docx.oxml.ns import qn

BASE = os.path.dirname(os.path.abspath(__file__))
DOCX = os.path.join(BASE, "perfil-proyecto-fifa-2026-v3.docx")
PDF = os.path.join(BASE, "perfil-proyecto-fifa-2026-v3.pdf")

CAPITULO_RE = re.compile(r"^CAP[ÍI]TULO\s+(\d+)")


def convertir_a_pdf(docx, destino):
    """LibreOffice headless: docx -> pdf."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["soffice", "--headless", "--norestore", "--convert-to", "pdf",
             "--outdir", tmp, docx],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=300,
        )
        generado = os.path.join(
            tmp, os.path.splitext(os.path.basename(docx))[0] + ".pdf")
        shutil.copyfile(generado, destino)


def paginas_pdf(pdf):
    """Devuelve la lista de textos de cada pagina del PDF."""
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                         check=True, capture_output=True, text=True).stdout
    return txt.split("\f")


def indice_por_pagina(docx):
    """Devuelve la lista [(titulo, parrafo_elemento)] del indice."""
    doc = Document(docx)
    entradas = []
    for p in doc.paragraphs:
        if p.style.name.startswith("toc "):
            textos = p._p.findall(".//" + qn("w:t"))
            if len(textos) >= 2:
                titulo = textos[0].text.strip()
                entradas.append((titulo, p._p))
    return entradas


def paginas_por_titulo(entradas, paginas):
    """Ubica cada titulo del indice en la pagina real del PDF."""
    # pagina de inicio de cada capitulo (para la numeracion por capitulo)
    inicio_capitulo = {}
    for i, texto in enumerate(paginas, start=1):
        for linea in texto.splitlines():
            linea = linea.strip()
            m = CAPITULO_RE.match(linea)
            if m and i > 2 and m.group(1) not in inicio_capitulo:
                inicio_capitulo[m.group(1)] = i

    resultado = {}
    for titulo, _ in entradas:
        pagina = None
        for i, texto in enumerate(paginas, start=1):
            if i <= 2:  # caratula e indice: no cuentan
                continue
            if titulo in texto:
                pagina = i
                break
        if pagina is None:
            continue
        # capitulo al que pertenece el titulo
        capitulo = "1"
        for num, ini in inicio_capitulo.items():
            if ini <= pagina:
                capitulo = num
        base = inicio_capitulo.get(capitulo, 3)
        resultado[titulo] = pagina - base + 1
    return resultado, inicio_capitulo


def escribir_numeros(docx, numeros):
    doc = Document(docx)
    cambiados = 0
    for p in doc.paragraphs:
        if not p.style.name.startswith("toc "):
            continue
        textos = p._p.findall(".//" + qn("w:t"))
        if len(textos) < 2:
            continue
        titulo = textos[0].text.strip()
        if titulo in numeros:
            textos[-1].text = str(numeros[titulo])
            cambiados += 1
    doc.save(docx)
    return cambiados


def main():
    if not os.path.exists(DOCX):
        raise SystemExit("No existe: {}".format(DOCX))

    print("[1/4] PDF provisional...")
    tmp_pdf = PDF + ".tmp.pdf"
    convertir_a_pdf(DOCX, tmp_pdf)
    paginas = paginas_pdf(tmp_pdf)

    entradas = indice_por_pagina(DOCX)
    numeros, inicio_cap = paginas_por_titulo(entradas, paginas)
    print("      inicio de capitulo (pagina PDF):", inicio_cap)
    for titulo, _ in entradas:
        print("      {:60s} -> {}".format(titulo, numeros.get(titulo, "?")))

    print("[2/4] Actualizando numeros del indice...")
    n = escribir_numeros(DOCX, numeros)
    print("      entradas actualizadas:", n)

    print("[3/4] PDF final...")
    convertir_a_pdf(DOCX, PDF)
    os.remove(tmp_pdf)

    print("[4/4] Verificacion...")
    paginas = paginas_pdf(PDF)
    for i, texto in enumerate(paginas, start=1):
        lineas = [l.strip() for l in texto.splitlines() if l.strip()]
        if lineas:
            print("      pagina {:2d}: {}".format(i, " | ".join(lineas[:2])[:90]))
    print("PDF generado:", PDF)


if __name__ == "__main__":
    main()
