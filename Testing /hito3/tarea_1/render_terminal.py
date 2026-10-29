# -*- coding: utf-8 -*-
"""Renderiza la salida real de pytest como una captura tipo terminal (PNG)."""
import re
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

FUENTE = "/usr/share/fonts/TTF/DejaVuSansMono.ttf"
FUENTE_BOLD = "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf"
TAM_FUENTE = 14
ESCALA = 2

COLOR_FONDO = (30, 30, 46)
COLOR_BARRA = (60, 60, 78)
COLOR_TEXTO = (220, 220, 230)

PALETA = {
    30: (85, 85, 85), 31: (255, 95, 95), 32: (120, 200, 90), 33: (230, 210, 100),
    34: (100, 160, 240), 35: (210, 120, 220), 36: (90, 210, 210), 37: (220, 220, 230),
    90: (130, 130, 140), 91: (255, 120, 120), 92: (150, 230, 120), 93: (240, 225, 130),
    94: (130, 180, 255), 95: (225, 150, 235), 96: (120, 225, 225), 97: (245, 245, 245),
    39: COLOR_TEXTO,
}

PATRON_ANSI = re.compile(r"\x1b\[([0-9;]*)m")


def parsear_ansi(texto):
    """Convierte texto con codigos ANSI en una lista de (segmento, color, bold)."""
    lineas = []
    color_actual = COLOR_TEXTO
    bold = False
    for linea in texto.split("\n"):
        segmentos = []
        posicion = 0
        for coincidencia in PATRON_ANSI.finditer(linea):
            if coincidencia.start() > posicion:
                segmentos.append((linea[posicion:coincidencia.start()], color_actual, bold))
            codigos = [int(c) for c in coincidencia.group(1).split(";") if c != ""] or [0]
            for codigo in codigos:
                if codigo == 0:
                    color_actual, bold = COLOR_TEXTO, False
                elif codigo == 1:
                    bold = True
                elif codigo == 22:
                    bold = False
                elif codigo in PALETA:
                    color_actual = PALETA[codigo]
            posicion = coincidencia.end()
        if posicion < len(linea):
            segmentos.append((linea[posicion:], color_actual, bold))
        lineas.append(segmentos)
    return lineas


def ejecutar(comando, cwd):
    proceso = subprocess.run(
        comando, cwd=cwd, shell=True, capture_output=True, text=True,
        env={"TERM": "xterm-256color", "COLUMNS": "120", "PATH": "/usr/bin:/bin"},
    )
    return proceso.stdout + proceso.stderr


def medir_ancho(lineas):
    ancho = 0
    for segmentos in lineas:
        largo = sum(len(s) for s, _, _ in segmentos)
        ancho = max(ancho, largo)
    return ancho


def renderizar(texto, titulo, salida):
    fuente = ImageFont.truetype(FUENTE, TAM_FUENTE * ESCALA)
    fuente_bold = ImageFont.truetype(FUENTE_BOLD, TAM_FUENTE * ESCALA)
    lineas = parsear_ansi(texto.rstrip("\n"))

    caracteres = medir_ancho(lineas)
    caja = fuente.getbbox("M")
    ancho_caracter = caja[2] - caja[0]
    alto_linea = int((TAM_FUENTE * 1.5) * ESCALA)

    margen = 16 * ESCALA
    alto_barra = 34 * ESCALA
    ancho = margen * 2 + ancho_caracter * max(caracteres, 40) + 8 * ESCALA
    alto = alto_barra + margen + alto_linea * max(len(lineas), 1) + margen

    imagen = Image.new("RGB", (ancho, alto), COLOR_FONDO)
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([0, 0, ancho, alto_barra], fill=COLOR_BARRA)
    for indice, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = (20 + indice * 22) * ESCALA
        cy = alto_barra // 2
        r = 6 * ESCALA
        dibujo.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    dibujo.text((100 * ESCALA, alto_barra // 2), titulo, font=fuente,
                fill=(230, 230, 235), anchor="lm")

    y = alto_barra + margen
    for segmentos in lineas:
        x = margen
        for segmento, color, bold in segmentos:
            f = fuente_bold if bold else fuente
            dibujo.text((x, y), segmento, font=f, fill=color)
            x += ancho_caracter * len(segmento)
        y += alto_linea

    imagen.save(salida)
    return salida
