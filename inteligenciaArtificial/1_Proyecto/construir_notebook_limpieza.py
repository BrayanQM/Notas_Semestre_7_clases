#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construye el notebook de Google Colab para la limpieza del dataset FIFA 2026.

Estructura y estilo calcados del notebook de referencia "Limpieza.ipynb"
(celdas de codigo con comentarios "## Parte N ..."), pero aplicados al
dataset "FIFA World Cup 2026 Team Data" (teams.csv) que viene dentro del
archivo comprimido archive.zip.

Salida: Limpieza_FIFA2026_Colab.ipynb
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Limpieza_FIFA2026_Colab.ipynb")

MD = "markdown"
CODE = "code"


def md(source):
    return {"cell_type": MD, "metadata": {}, "source": source.strip("\n").splitlines(keepends=True)}


def code(source):
    return {
        "cell_type": CODE,
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source.strip("\n").splitlines(keepends=True),
    }


CELLS = [
    md("""
# Limpieza de datos — Simulador de Enfrentamiento Directo FIFA 2026

Notebook de **limpieza y preparacion del dataset** del proyecto *"Simulador de
Enfrentamiento Directo entre Selecciones de la Copa Mundial de la FIFA 2026 Basado en
Red Neuronal"*.

Esta preparado para **Google Colab**: se ejecuta celda por celda con el boton
*Ejecutar todo*. Toma el archivo comprimido `archive.zip` (descarga de Kaggle:
*FIFA World Cup 2026 Team Data*), verifica su contenido, diagnostica los problemas de
calidad del CSV y aplica las tareas de limpieza documentadas en el apartado **2.3
Limpieza de datos** del documento del proyecto.

**Resultado:** `teams_limpio.csv` (dataset depurado), `variables_modelo.csv`
(variables de entrada del simulador) y `codigos_equipos.csv` (diccionario de
equivalencias). Los dos primeros archivos no contienen ninguna letra: las
variables categoricas quedan codificadas como numeros enteros. Ambos alimentan el
pipeline de entrenamiento descrito en el apartado 2.2 del documento.
"""),
    code("""
## Parte 1. Carga del paquete comprimido descargado de Kaggle
import os
import zipfile
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 60)
pd.set_option('display.width', 220)

ZIP_NAME = "archive.zip"
# En Google Colab los archivos viven en /content; en local se usa la carpeta de trabajo.
ZIP_PATH = os.path.join("/content", ZIP_NAME) if os.path.isdir("/content") else ZIP_NAME

if not os.path.exists(ZIP_PATH):
    from google.colab import files
    print("Selecciona el archivo archive.zip en el dialogo que se abrira...")
    uploaded = files.upload()
    with open(ZIP_PATH, "wb") as f:
        f.write(uploaded[ZIP_NAME])

# Inventario del contenido del ZIP
with zipfile.ZipFile(ZIP_PATH) as z:
    archivos = z.namelist()
    print("Archivos contenidos en", ZIP_NAME, ":", archivos)
    z.extractall("data")

# Se lee el archivo CSV contenido en el paquete
CSV_NAME = [a for a in archivos if a.lower().endswith(".csv")][0]
df = pd.read_csv(os.path.join("data", CSV_NAME))

print("Archivo cargado:", CSV_NAME)
print("Forma del dataset (filas x columnas):", df.shape)
df.head()
"""),
    code("""
## Parte 1 (alternativa). Descarga directa desde Kaggle con kagglehub
# Alternativa al paso anterior: en lugar de subir el archivo, se descarga de Kaggle.
# Se deja comentada porque necesita la cuenta de Kaggle configurada en el entorno.
#
# !pip -q install kagglehub
# import kagglehub
# ruta = kagglehub.dataset_download("swaptr/fifa-wc-2026-teams")
# print("Dataset descargado en:", ruta)
print("Alternativa disponible: descomentar las lineas de kagglehub.")
"""),
    code("""
## Parte 1.1 / Conocer los datos
from pandas.api.types import is_string_dtype

print("Filas (selecciones):", df.shape[0])
print("Columnas (variables):", df.shape[1])
print("Variables de texto:", [c for c in df.columns if is_string_dtype(df[c])])
print("Variables numericas:", df.shape[1] - len([c for c in df.columns if is_string_dtype(df[c])]))

df[["team", "team_country", "games", "goals", "possession", "shots_on_target", "avg_age"]].head()
"""),
    code("""
## Parte 2. Diagnostico de la calidad de los datos
hallazgos = []

# 2.1 Valores nulos por variable
nulos = df.isna().sum()
cols_nulos = nulos[nulos > 0]
hallazgos.append(("Variables con valores nulos", len(cols_nulos), ", ".join(cols_nulos.index)))

# 2.2 Variables constantes o totalmente vacias
constantes = [c for c in df.columns if df[c].nunique(dropna=True) <= 1]
hallazgos.append(("Variables constantes o vacias", len(constantes), ", ".join(constantes)))

# 2.3 Duplicados
hallazgos.append(("Filas duplicadas", int(df.duplicated().sum()), "-"))
hallazgos.append(("Selecciones duplicadas", int(df["team"].duplicated().sum()), "-"))

# 2.4 Grupos de variables con valores identicos
numericas = df.select_dtypes(include=[np.number])
grupos = {}
for c in numericas.columns:
    clave = tuple(numericas[c].fillna(-999).round(6).tolist())
    grupos.setdefault(clave, []).append(c)
duplicadas = [g for g in grupos.values() if len(g) > 1]
hallazgos.append(("Grupos de variables duplicadas", len(duplicadas),
                  " | ".join(" = ".join(g) for g in duplicadas[:4]) + " | ..."))

# 2.5 Desbalance de partidos disputados
hallazgos.append(("Partidos disputados por seleccion",
                  f"{int(df['games'].min())} - {int(df['games'].max())}",
                  f"correlacion goals-games = {df['goals'].corr(df['games']):.2f}"))

diagnostico = pd.DataFrame(hallazgos, columns=["Hallazgo", "Cantidad", "Detalle"])
diagnostico
"""),
    code("""
## Parte 3. Limpieza de datos
df_clean = df.copy()

# 3.1 Eliminacion de variables constantes o totalmente vacias
constantes = [c for c in df_clean.columns if df_clean[c].nunique(dropna=True) <= 1]
df_clean = df_clean.drop(columns=constantes)
print("3.1 Tras eliminar constantes/vacias:", df_clean.shape)

# 3.2 Eliminacion de variables duplicadas (se conserva la primera de cada grupo)
numericas = df_clean.select_dtypes(include=[np.number])
grupos = {}
for c in numericas.columns:
    clave = tuple(numericas[c].fillna(-999).round(6).tolist())
    grupos.setdefault(clave, []).append(c)
a_eliminar = []
for g in grupos.values():
    if len(g) > 1:
        a_eliminar.extend(g[1:])          # se conserva la primera del grupo
df_clean = df_clean.drop(columns=[c for c in a_eliminar if c in df_clean.columns])
print("3.2 Tras eliminar duplicadas:", df_clean.shape)

# 3.3 Eliminacion de team_country (alias de team en 5 selecciones)
df_clean = df_clean.drop(columns=["team_country"])
print("3.3 Tras eliminar team_country:", df_clean.shape)

# 3.4 Imputacion de los valores nulos restantes con la mediana
nulos = df_clean.isna().sum()
cols_nulos = nulos[nulos > 0].index.tolist()
for c in cols_nulos:
    df_clean[c] = df_clean[c].fillna(df_clean[c].median())
print("3.4 Variables imputadas:", cols_nulos)
print("Valores nulos restantes:", int(df_clean.isna().sum().sum()))
"""),
    code("""
## Parte 3.1 / Normalizacion por cantidad de partidos disputados
# Cada seleccion disputo entre 3 y 8 partidos, por lo que las metricas acumuladas
# no son comparables: se calculan ratios por partido y por 90 minutos.
df_clean["goals_per_game"] = (df_clean["goals"] / df_clean["games"]).round(3)
df_clean["shots_on_target_per_game"] = (df_clean["shots_on_target"] / df_clean["games"]).round(3)

comparacion = pd.DataFrame({
    "equipo": df_clean["team"],
    "goles (acumulado)": df_clean["goals"],
    "goles por partido": df_clean["goals_per_game"],
    "disparos a puerta (acumulado)": df_clean["shots_on_target"],
    "disparos por partido": df_clean["shots_on_target_per_game"],
})
comparacion.sort_values("goles por partido", ascending=False).head(10)
"""),
    code("""
## Parte 4. Codificacion de variables categoricas
# Tras la limpieza solo queda una variable de texto: el nombre de la seleccion.
# El modelo no admite letras, por lo que cada nombre se sustituye por un codigo
# entero y el diccionario de equivalencias se conserva en un archivo aparte.
codigos = {nombre: i + 1 for i, nombre in enumerate(sorted(df_clean["team"].unique()))}
df_clean["team_codigo"] = df_clean["team"].map(codigos)

diccionario = pd.DataFrame(sorted(codigos.items()), columns=["team", "team_codigo"])
print("Codigos generados:", len(codigos))
diccionario.head(10)
"""),
    code("""
## Parte 4.1 / One-hot encoding y eliminacion del texto
# One-hot encoding: se agregan columnas binarias (0/1) para las categoricas con
# pocos valores distintos. Tras la limpieza no queda ninguna ademas del nombre
# de la seleccion, que se mantiene codificado y no expandido para no crear 48
# columnas adicionales.
bajas = [c for c in df_clean.columns
         if is_string_dtype(df_clean[c]) and c != "team" and df_clean[c].nunique() <= 20]
if bajas:
    df_clean = pd.get_dummies(df_clean, columns=bajas, drop_first=True)
    print("Variables codificadas en one-hot:", bajas)
else:
    print("No quedan categoricas de baja cardinalidad: no se aplica one-hot.")

# El nombre de la seleccion ya esta codificado, asi que se retira del dataset
df_clean = df_clean.drop(columns=["team"])
df_clean = df_clean[["team_codigo"] + [c for c in df_clean.columns if c != "team_codigo"]]

restantes = [c for c in df_clean.columns if is_string_dtype(df_clean[c])]
print("Variables de texto en el dataset depurado:", restantes)
print("Forma del dataset depurado:", df_clean.shape)
"""),
    code("""
## Parte 5. Seleccion de variables para el simulador de enfrentamiento directo
# Las cuatro variables del vector de diferencias: goles, posesion, disparos a puerta
# y edad promedio del plantel.
FEATURES = ["goals", "possession", "shots_on_target", "avg_age"]

variables = ["team_codigo", "games"] + FEATURES + ["goals_per_game", "shots_on_target_per_game"]
df_modelo = df_clean[[v for v in variables if v in df_clean.columns]].copy()
df_modelo = df_modelo.sort_values("team_codigo").reset_index(drop=True)

print("Dataset para el modelo:", df_modelo.shape)
print("Variables de texto en el CSV del modelo:",
      [c for c in df_modelo.columns if is_string_dtype(df_modelo[c])])
print("Nulos:", int(df_modelo.isna().sum().sum()), "| Selecciones unicas:", df_modelo["team_codigo"].nunique())
df_modelo.head(10)
"""),
    code("""
## Parte 6. Exportacion de los datasets limpios
# Los archivos de datos no contienen ninguna letra: el unico archivo con texto
# es el diccionario de equivalencias, que sirve para interpretar los codigos.
df_clean.to_csv("teams_limpio.csv", index=False)
df_modelo.to_csv("variables_modelo.csv", index=False)
diccionario.to_csv("codigos_equipos.csv", index=False)

print("Archivos generados:")
for f in ["teams_limpio.csv", "variables_modelo.csv", "codigos_equipos.csv"]:
    print(" -", f, os.path.getsize(f), "bytes")
"""),
    code("""
## Parte 7. Resumen de la limpieza aplicada
resumen = pd.DataFrame([
    ["Variables del CSV original", df.shape[1], "-"],
    ["Variables del dataset depurado", df_clean.shape[1], "se conservan todas las utiles"],
    ["Variables del modelo", df_modelo.shape[1], ", ".join(df_modelo.columns)],
    ["Selecciones (filas)", df.shape[0], df_modelo.shape[0]],
    ["Valores nulos", int(df.isna().sum().sum()), int(df_modelo.isna().sum().sum())],
    ["Variables constantes o vacias", len(constantes), "eliminadas"],
    ["Variables duplicadas", len(set(a_eliminar)), "eliminadas"],
    ["Variables con nulos imputados", len(cols_nulos), ", ".join(cols_nulos)],
    ["Variables de texto", 1, "0 (el nombre queda como codigo entero)"],
], columns=["Aspecto", "Antes", "Despues"])
resumen
"""),
    md("""
### Criterio de limpieza aplicado

1. **Eliminar** toda variable constante o totalmente vacia, porque no aporta
   informacion y sesga el analisis descriptivo.
2. **Eliminar** las variables duplicadas, conservando la primera de cada grupo, para
   trabajar con un archivo sin redundancias.
3. **Eliminar** `team_country`, que solo repite el nombre de la seleccion con otra
   grafia (5 de las 48 selecciones usan un alias distinto).
4. **Imputar** con la mediana los valores nulos de las variables de penaltis del
   portero, que no tienen registro en 33 de las 48 selecciones.
5. **Normalizar** por cantidad de partidos disputados, porque las selecciones jugaron
   entre 3 y 8 partidos y las metricas acumuladas no son comparables entre si.
6. **Codificar** las variables categoricas: el nombre de la seleccion se sustituye
   por un codigo entero (`team_codigo`) y la equivalencia se guarda en
   `codigos_equipos.csv`, de modo que ni el dataset depurado ni el archivo del
   modelo contengan letras.
7. **Seleccionar** las cuatro variables del vector de diferencias (`goals`,
   `possession`, `shots_on_target`, `avg_age`) para el simulador de enfrentamiento
   directo descrito en el apartado 2.2 del documento.
"""),
]


def construir():
    notebook = {
        "cells": CELLS,
        "metadata": {
            "colab": {
                "name": "Limpieza_FIFA2026_Colab.ipynb",
                "provenance": [],
                "toc_visible": True,
            },
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }
    with open(OUT, "w", encoding="utf8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    print("Notebook construido:", OUT)


if __name__ == "__main__":
    construir()
