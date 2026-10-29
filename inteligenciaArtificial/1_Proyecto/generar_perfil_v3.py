#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la version 2 del perfil de proyecto FIFA 2026.

Clona el .docx original (perfil-proyecto-fifa-2026.docx) conservando al 100% su
formato, imagenes, estilos, encabezado y numeracion, y agrega:

  1. Capitulo 1 -> se profundiza "1.1. Planteamiento del problema" con la
     estructura de la skill UNIFRANZ/APA 7 (EstructuraIntegrador.md, seccion 7):
        1.1.1. Identificacion de la situacion problemica
        1.1.2. Formulacion del problema
        1.1.3. Problemas especificos
     (el texto original del autor se conserva integro y se complementa)

  2. Capitulo 2 -> nueva subseccion "2.1.1. Verificacion de los archivos CSV
     del ZIP" con la tabla de inventario y los espacios reservados para las
     capturas que deben pegar el autor.

  3. El indice (campo TOC) se actualiza con las entradas nuevas y se marca el
     documento para que Word/LibreOffice recalcule los numeros de pagina.

Uso:  python3 generar_perfil_v2.py
"""

import copy
import os
import shutil

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

BASE = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(BASE, "perfil-proyecto-fifa-2026-v2.docx")
SRC = ORIGEN
DST = os.path.join(BASE, "perfil-proyecto-fifa-2026-v3.docx")

# --------------------------------------------------------------------------
# Texto nuevo
# --------------------------------------------------------------------------

INTRO_1_1 = (
    "Este apartado delimita el problema que el proyecto se propone resolver. El análisis "
    "se organiza en tres niveles: primero se describe la situación problémica en el "
    "contexto del torneo y de los datos disponibles; luego se formula la pregunta central "
    "que orienta el desarrollo; finalmente se desglosan los problemas específicos que el "
    "proyecto se propone atacar y que se convierten, uno a uno, en los objetivos del "
    "apartado 1.2."
)

APERTURA_1_1_1 = (
    "La ampliación del torneo no es un simple ajuste de calendario. Al pasar de 32 a 48 "
    "selecciones, el número de emparejamientos posibles pasa de 496 a 2.256, y con él "
    "crece el número de preguntas que deben responderse antes de la fase de dieciseisavos "
    "de final: ¿con qué probabilidad gana cada cruce? A esa necesidad se suman dos "
    "condiciones: las selecciones son muy distintas entre sí y, por lo tanto, los "
    "enfrentamientos también lo son."
)

SITUACION_A = (
    "Hoy esa pregunta se responde de tres maneras, y ninguna resuelve el problema de forma "
    "satisfactoria para un entorno académico. La primera es la opinión del especialista: "
    "analistas y comentaristas estiman los favoritos a partir de su experiencia, lo cual "
    "aporta contexto pero no es reproducible ni auditable. La segunda son los rankings "
    "oficiales, como los que publica la FIFA, que resumen decenas de variables en un solo "
    "número, pero ocultan el peso de cada una, se actualizan con poca frecuencia y no "
    "responden a un enfrentamiento concreto: dicen qué equipo es mejor en general, no cómo "
    "termina el partido entre dos selecciones específicas. La tercera son las cuotas de "
    "las casas de apuestas, que sí incorporan información estadística, pero responden también "
    "a factores de mercado, a la liquidez de la apuesta y al riesgo que asume el operador, "
    "por lo que no pueden usarse como referencia técnica."
)

SITUACION_B = (
    "El dataset publicado en Kaggle aporta el material cuantitativo para construir una "
    "respuesta propia. Sin embargo, su análisis descriptivo revela que la información es "
    "agregada por selección y no por partido: cada fila resume la actuación global de un "
    "plantel en un torneo, sin fecha, sin rival y sin resultado partido a partido. Es decir, "
    "el archivo no contiene confrontaciones directas históricas con un ganador observado, y "
    "por tanto tampoco aporta la etiqueta natural que un modelo de clasificación necesita. "
    "Además, el número de partidos jugados no es igual para todos los equipos, varía entre 3 "
    "y 8, de modo que las métricas acumuladas no son directamente comparables sin una "
    "normalización por cantidad de encuentros; y algunas columnas, sobre todo las relativas "
    "a la actuación de los porteros, presentan valores vacíos. En consecuencia, los datos "
    "disponibles son descriptivos, pero no predictivos por sí solos: falta el procedimiento "
    "que los convierta en una estimación de victoria."
)

SITUACION_C = (
    "Al problema de los datos se suma un problema de método. En el contexto de la materia "
    "de Inteligencia Artificial no basta con obtener una respuesta: es necesario mostrar el "
    "camino completo que va desde la adquisición del dato hasta la entrega de un modelo "
    "evaluado, interpretable y reproducible en un entorno local. Eso implica descomprimir "
    "el archivo comprimido, verificar y documentar cada uno de los archivos CSV que "
    "contiene, construir el conjunto de pares de enfrentamiento, definir la variable de "
    "entrada y la etiqueta, entrenar el modelo y medir su desempeño con métricas "
    "explícitas. Ninguna de estas etapas puede omitirse, porque cada una introduce "
    "decisiones que se reflejan en el resultado final: un error en la selección de "
    "variables, una etiqueta mal definida o un conjunto de entrenamiento mal construido "
    "se propagan hasta la probabilidad que el sistema entrega."
)

FORMULACION_A = (
    "De la situación descrita se deriva la pregunta central del proyecto: ¿cómo puede "
    "estimarse la probabilidad de victoria de una selección A frente a una selección B, a "
    "partir de las estadísticas agregadas disponibles en el dataset de la Copa Mundial de "
    "la FIFA 2026, mediante un modelo de aprendizaje automático interpretable que pueda "
    "entrenarse y ejecutarse íntegramente en un entorno local reproducible?"
)

FORMULACION_B = (
    "La pregunta admite una respuesta acotada y deliberadamente sencilla. En lugar de "
    "recurrir a un modelo de alta complejidad, la estimación se plantea sobre una red "
    "neuronal de una sola neurona con activación sigmoide, es decir, una regresión logística: "
    "la entrada es el vector de diferencias entre las métricas de ambos equipos, la salida "
    "es un valor entre 0 y 1 que se interpreta como probabilidad de victoria del equipo A, y "
    "el resultado se guarda en formato .keras para ser consultado a través de una API. Esta "
    "decisión no es una limitación técnica arbitraria, sino una condición del problema: con "
    "una sola neurona, los pesos aprendidos son legibles y se puede explicar cuánto aporta "
    "cada métrica a la predicción, algo que un modelo de muchas capas no ofrece."
)

INTRO_1_1_3 = (
    "El problema general se descompone en los siguientes problemas específicos, cada uno con "
    "su propio entregable y su propia evidencia de avance:"
)

PROBLEMAS = [
    (
        "Disponibilidad y trazabilidad de los datos.",
        " El dataset se distribuye en un archivo comprimido que debe descomprimirse, "
        "inventariarse y documentarse. Es necesario dejar constancia de qué archivos CSV "
        "contiene, qué información ofrece cada uno y con qué capturas de pantalla se "
        "respalda la revisión, de modo que cualquier lector pueda replicar el análisis.",
    ),
    (
        "Construcción de la variable de entrada.",
        " Los datos disponibles son valores absolutos por selección, mientras que el "
        "enfrentamiento directo exige una medida relativa. Se requiere la definición del "
        "vector de diferencias entre dos equipos y su estandarización, para que las cuatro "
        "variables utilizadas tengan una escala comparable.",
    ),
    (
        "Definición de la etiqueta y del conjunto de entrenamiento.",
        " Como no existen confrontaciones históricas etiquetadas en el archivo, las etiquetas "
        "deben construirse de forma sintética a partir de los pares de selecciones. Eso "
        "exige una regla consistente, una distribución equilibrada de las clases y una "
        "separación explícita entre los datos de entrenamiento y los de validación.",
    ),
    (
        "Entrenamiento y evaluación del modelo.",
        " Se necesita definir la función de pérdida, el optimizador y el número de épocas, y "
        "medir el desempeño con métricas explícitas (exactitud, precisión, exhaustividad y "
        "matriz de confusión) sobre datos que el modelo no haya visto, para no confundir "
        "ajuste con capacidad de generalización.",
    ),
    (
        "Persistencia y disponibilidad del modelo.",
        " El resultado del entrenamiento debe guardarse en un archivo .keras y quedar "
        "disponible para su uso desde una interfaz sencilla, de manera que el pronóstico de "
        "un cruce pueda consultarse en segundos sin tener que repetir el entrenamiento.",
    ),
    (
        "Interpretabilidad del resultado.",
        " La estimación entregada debe poder justificarse: los pesos de la neurona y el "
        "vector de diferencias que produce se convierten en la explicación de por qué un "
        "equipo es considerado favorito, lo que aporta valor didáctico y evita el uso de una "
        "caja negra.",
    ),
    (
        "Documentación y reproducibilidad del proceso.",
        " El notebook, el entorno de trabajo y las decisiones tomadas deben quedar "
        "registrados, junto con las capturas de la revisión de cada archivo del ZIP, para "
        "que el proyecto pueda reproducirse, evaluarse y reutilizarse por un tercero.",
    ),
]

CIERRE_1_1 = (
    "Con esta delimitación quedan planteados la situación problémica, la pregunta central y "
    "los problemas específicos. El apartado 1.2 traduce ese diagnóstico en objetivos "
    "verificables: el objetivo general enuncia el resultado que se persigue y los objetivos "
    "específicos responden, uno a uno, a los problemas específicos aquí identificados."
)

# --- Capitulo 2: verificacion de los CSV del ZIP --------------------------

VERIF_INTRO = (
    "Además del análisis descriptivo, se documenta la revisión completa del paquete de "
    "descarga. El archivo comprimido obtenido de Kaggle se descomprime en la carpeta de "
    "trabajo y su contenido queda registrado en la siguiente tabla, donde se indica, para "
    "cada archivo, qué se verificó y con qué evidencia queda respaldada esa revisión."
)

VERIF_TITULO = "Tabla 2. Inventario de los archivos del ZIP y verificación realizada."

VERIF_FILAS = [
    (
        "Archivo",
        "Contenido verificado",
        "Revisión realizada",
        "Evidencia",
    ),
    (
        "archive.zip",
        "Paquete comprimido descargado de Kaggle con el dataset \"FIFA World Cup 2026 Team "
        "Data\".",
        "Descomprimido en la carpeta de trabajo e inventario de su contenido.",
        "Captura 1",
    ),
    (
        "teams.csv",
        "48 filas (una por selección clasificada) y 136 columnas de métricas ofensivas, "
        "defensivas y de portería.",
        "Recorrido íntegro del archivo: encabezado, primeras 10 filas, valores vacíos y "
        "distribución de partidos por equipo.",
        "Captura 2",
    ),
]

VERIF_NOTA = (
    "Nota: Elaboración propia a partir de la revisión del archivo descargado de Kaggle "
    "(https://www.kaggle.com/datasets/swaptr/fifa-wc-2026-teams)."
)

VERIF_CIERRE = (
    "La verificación confirma que el dataset no incluye información partido a partido ni "
    "archivos adicionales con emparejamientos históricos, lo que confirma la necesidad de "
    "construir las etiquetas de forma sintética descrita en el apartado 1.1.3. A "
    "continuación se insertan las capturas de pantalla correspondientes al contenido del "
    "archivo comprimido y a las primeras filas de cada archivo CSV revisado, de modo que la "
    "verificación quede respaldada visualmente."
)

FIG_CAPTION_1 = "Figura 1. Contenido del archivo comprimido archive.zip."
FIG_CAPTION_2 = "Figura 2. Primeras filas del archivo teams.csv."

# --------------------------------------------------------------------------
# Utilidades de bajo nivel
# --------------------------------------------------------------------------


def _clean_shell(tpl_p):
    """Copia el parrafo plantilla y le quita todo el contenido (deja solo pPr)."""
    nuevo = copy.deepcopy(tpl_p._p)
    for hijo in list(nuevo):
        if hijo.tag != qn("w:pPr"):
            nuevo.remove(hijo)
    return nuevo


def _rpr_de(tpl_p):
    rpr = None
    for run in tpl_p.runs:
        if run._r.rPr is not None:
            rpr = run._r.rPr
            break
    return rpr


def _nueva_parrafo(tpl_p, texto, rpr_extra=None, keep_next=False):
    """Parrafo nuevo con el formato del parrafo plantilla."""
    nuevo = _clean_shell(tpl_p)
    p = Paragraph(nuevo, tpl_p._parent)
    run = p.add_run(texto)
    rpr = _rpr_de(tpl_p)
    if rpr is not None:
        run._r.insert(0, copy.deepcopy(rpr))
    if rpr_extra:
        rpr_extra(run)
    if keep_next:
        _keep_next(nuevo)
    return nuevo


def _keep_next(para_el):
    """Agrega <w:keepNext/> al pPr (respeta el orden del esquema CT_PPr)."""
    pPr = para_el.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        para_el.insert(0, pPr)
    if pPr.find(qn("w:keepNext")) is not None:
        return
    el = OxmlElement("w:keepNext")
    pStyle = pPr.find(qn("w:pStyle"))
    if pStyle is not None:
        pStyle.addnext(el)
    else:
        pPr.insert(0, el)


def _vinieta(tpl_p, etiqueta, texto):
    """Vinieta con encabezado en negrita: '  o  Etiqueta. texto'."""
    nuevo = _clean_shell(tpl_p)
    p = Paragraph(nuevo, tpl_p._parent)
    rpr = _rpr_de(tpl_p)

    r1 = p.add_run("  \u2022  ")
    r2 = p.add_run(etiqueta)
    r3 = p.add_run(texto)
    for run in (r1, r2, r3):
        if rpr is not None:
            run._r.insert(0, copy.deepcopy(rpr))
    r2.bold = True
    return nuevo


def _encabezado(tpl_p, texto, bm_id, bm_nombre):
    """Encabezado (Heading 3) con marcador para el indice."""
    nuevo = _clean_shell(tpl_p)
    p = Paragraph(nuevo, tpl_p._parent)
    rpr = _rpr_de(tpl_p)

    run = p.add_run(texto)
    if rpr is not None:
        run._r.insert(0, copy.deepcopy(rpr))

    inicio = OxmlElement("w:bookmarkStart")
    inicio.set(qn("w:id"), str(bm_id))
    inicio.set(qn("w:name"), bm_nombre)
    fin = OxmlElement("w:bookmarkEnd")
    fin.set(qn("w:id"), str(bm_id))

    pPr = nuevo.find(qn("w:pPr"))
    idx = 1 if pPr is not None else 0
    nuevo.insert(idx, inicio)
    nuevo.insert(idx + 2, fin)
    return nuevo


def _tabla(tpl_tbl, titulo, cabecera, filas, anchos, nota=None):
    """Replica el formato de la Tabla 1 (borde superior/inferior, Arial 10)."""
    tpl_tbl_xml = tpl_tbl._tbl
    tbl = copy.deepcopy(tpl_tbl_xml)

    # Se conserva solo la primera fila (encabezado) como plantilla de formato.
    filas_tpl = tbl.findall(qn("w:tr"))
    fila_enc = filas_tpl[0]
    celdas_enc = fila_enc.findall(qn("w:tc"))

    # Rejilla de columnas
    grid = tbl.find(qn("w:tblGrid"))
    for gc in grid.findall(qn("w:gridCol")):
        grid.remove(gc)
    for ancho in anchos:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(ancho))
        grid.append(gc)

    def _celda(celda_tpl, texto, ancho, encabezado, ultima, mantener_junto=False):
        tc = copy.deepcopy(celda_tpl)
        tcPr = tc.find(qn("w:tcPr"))
        bordes = tcPr.find(qn("w:tcBorders"))
        if bordes is not None:
            tcPr.remove(bordes)
        bordes = OxmlElement("w:tcBorders")
        if encabezado:
            for lado in ("top", "bottom"):
                b = OxmlElement("w:" + lado)
                b.set(qn("w:val"), "single")
                b.set(qn("w:color"), "000000")
                b.set(qn("w:sz"), "6")
                b.set(qn("w:space"), "0")
                bordes.append(b)
        elif ultima:
            b = OxmlElement("w:bottom")
            b.set(qn("w:val"), "single")
            b.set(qn("w:color"), "000000")
            b.set(qn("w:sz"), "6")
            b.set(qn("w:space"), "0")
            bordes.append(b)
        tcPr.append(bordes)
        tcW = tcPr.find(qn("w:tcW"))
        if tcW is None:
            tcW = OxmlElement("w:tcW")
            tcPr.append(tcW)
        tcW.set(qn("w:w"), str(ancho))
        tcW.set(qn("w:type"), "dxa")

        # texto
        p = tc.find(qn("w:p"))
        for run in p.findall(qn("w:r")):
            p.remove(run)
        run = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        for tag, attrs in (
            ("w:rFonts", {"w:ascii": "Arial", "w:hAnsi": "Arial"}),
            ("w:b", {}),
            ("w:color", {"w:val": "000000"}),
            ("w:sz", {"w:val": "20"}),
        ):
            el = OxmlElement(tag)
            for k, v in attrs.items():
                el.set(qn(k), v)
            rpr.append(el)
        run.append(rpr)
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = texto
        run.append(t)
        p.append(run)
        if mantener_junto:
            _keep_next(p)
        return tc

    # reconstruye las filas
    for tr in tbl.findall(qn("w:tr")):
        tbl.remove(tr)

    # la tabla plantilla tiene 2 columnas; se clona la ultima celda para las demas
    n_cols = len(anchos)
    celdas = [celdas_enc[i % len(celdas_enc)] for i in range(n_cols)]

    tr = OxmlElement("w:tr")
    trPr = OxmlElement("w:trPr")
    trPr.append(OxmlElement("w:cantSplit"))
    tr.append(trPr)
    for i, texto in enumerate(cabecera):
        tr.append(_celda(celdas[i], texto, anchos[i], True, False, mantener_junto=True))
    tbl.append(tr)

    for idx_fila, fila in enumerate(filas):
        tr = OxmlElement("w:tr")
        trPr = OxmlElement("w:trPr")
        trPr.append(OxmlElement("w:cantSplit"))
        tr.append(trPr)
        ultima = idx_fila == len(filas) - 1
        for i, texto in enumerate(fila):
            tr.append(_celda(celdas[i], texto, anchos[i], False, ultima,
                             mantener_junto=not ultima))
        tbl.append(tr)

    return tbl


def _entrada_toc(tpl_el, ancla, texto, pagina="1", estilo=None):
    """Clona una entrada del indice y la reescribe (ancla, texto, pagina)."""
    el = copy.deepcopy(tpl_el)
    # paraId duplicado -> Word tolera, pero se elimina para evitar avisos
    for attr in list(el.attrib):
        if attr.endswith("}paraId") or attr.endswith("}textId"):
            del el.attrib[attr]

    pStyle = el.find(qn("w:pPr")).find(qn("w:pStyle"))
    if pStyle is not None:
        pStyle.set(qn("w:val"), estilo if estilo else "191")  # toc 3 por defecto

    link = el.find(qn("w:hyperlink"))
    link.set(qn("w:anchor"), ancla)
    link.set(qn("w:tooltip"), "#" + ancla)

    instr = el.find(".//" + qn("w:instrText"))
    instr.text = "PAGEREF {} \\h".format(ancla)

    textos = el.findall(".//" + qn("w:t"))
    textos[0].text = texto
    textos[-1].text = pagina
    return el


def _actualizar_campos_al_abrir(doc):
    """Marca el documento para que Word/LibreOffice recalculen el indice."""
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is not None:
        return
    el = OxmlElement("w:updateFields")
    el.set(qn("w:val"), "true")
    ancla = None
    for tag in ("w:hdrShapeDefaults", "w:footnotePr", "w:endnotePr", "w:compat", "w:docVars"):
        encontrado = settings.find(qn(tag))
        if encontrado is not None:
            ancla = encontrado
            break
    if ancla is not None:
        ancla.addprevious(el)
    else:
        settings.append(el)


# --------------------------------------------------------------------------
# Apartado 2.3. Limpieza de datos
# --------------------------------------------------------------------------

LIMPIEZA_INTRO = (
    "El archivo teams.csv no puede pasar directamente al entrenamiento del simulador: "
    "antes se requiere una etapa de limpieza que lo deje en condiciones de ser leído por "
    "la red neuronal. Esa etapa se implementa en el notebook de Google Colab "
    "Limpieza_FIFA2026_Colab.ipynb, que acompaña a este documento y ejecuta el mismo "
    "procedimiento sobre el archivo archive.zip descargado de Kaggle. El notebook carga el "
    "paquete comprimido, verifica su contenido, diagnostica los problemas de calidad del "
    "CSV y exporta el resultado depurado en los archivos teams_limpio.csv y "
    "variables_modelo.csv."
)

LIMPIEZA_DIAGNOSTICO = (
    "El diagnóstico del archivo teams.csv, con 48 selecciones y 136 variables, identificó "
    "cinco problemas que fue necesario corregir. Hay variables sin ningún dato registrado: "
    "las cuatro del desempate por penaltis (pens_won, pens_conceded, pens_won_against y "
    "pens_conceded_against) están vacías en las 48 filas. Además, dos variables de porcentaje "
    "de minutos son constantes, 18 grupos de variables contienen información idéntica (por "
    "ejemplo, games coincide con games_against y con gk_games), por lo que 24 variables son "
    "redundantes, y la variable team_country repite el nombre de la selección con otra grafía "
    "en cinco casos. Por último, dos variables de penaltis del portero tienen 33 de 48 valores "
    "nulos. A esto se suma que las selecciones disputaron entre 3 y 8 partidos, de modo que "
    "las métricas acumuladas no son comparables entre equipos: la correlación entre los goles "
    "y los partidos disputados es de 0,89. La Tabla 3 resume el diagnóstico y las decisiones "
    "tomadas en cada caso."
)

LIMPIEZA_TITULO_TABLA = "Tabla 3. Diagnóstico y decisiones de limpieza aplicadas al dataset teams.csv."

LIMPIEZA_ENCABEZADOS = ["Hallazgo", "Variables afectadas", "Acción aplicada", "Resultado"]

LIMPIEZA_FILAS = [
    ["Variables sin datos",
     "pens_won, pens_conceded, pens_won_against, pens_conceded_against (48 de 48 vacías)",
     "Eliminación", "136 a 132 variables"],
    ["Variables constantes",
     "minutes_pct, minutes_pct_against",
     "Eliminación", "132 a 130 variables"],
    ["Variables duplicadas",
     "18 grupos idénticos, 24 variables redundantes (games = games_against = gk_games)",
     "Se conserva la primera de cada grupo", "130 a 106 variables"],
    ["Variable redundante",
     "team_country, alias del nombre de la selección en 5 casos",
     "Eliminación", "106 a 105 variables"],
    ["Valores nulos",
     "gk_pens_save_pct y gk_pens_save_pct_against (33 de 48)",
     "Imputación por la mediana", "258 nulos a 0"],
    ["Partidos no comparables",
     "games entre 3 y 8 (correlación con goals de 0,89)",
     "Variables por partido y por 90 minutos", "Métricas comparables"],
    ["Variables categóricas",
     "team, los 48 nombres de las selecciones",
     "Codificación por etiquetas y one-hot si aplica",
     "0 variables de texto en los CSV"],
]

LIMPIEZA_RESULTADO = (
    "Como resultado, el dataset depurado conserva las 48 selecciones con 105 variables útiles, "
    "más dos variables nuevas calculadas por partido (goles por partido y disparos a puerta por "
    "partido), y se guarda como teams_limpio.csv. Para el simulador de enfrentamiento directo "
    "se seleccionan las cuatro variables que forman el vector de diferencias del apartado 2.2, "
    "goles, posesión, disparos a puerta y edad promedio, junto con el número de partidos y los "
    "dos ratios por partido, lo que da un archivo de 48 filas y 8 variables que se exporta como "
    "variables_modelo.csv."
)

LIMPIEZA_CODIFICACION = (
    "Como el modelo no admite valores de texto, la única variable categórica que permanece "
    "tras la limpieza, el nombre de la selección, se sustituye por un código entero mediante "
    "codificación por etiquetas: las 48 selecciones se numeran del 1 al 48 en orden alfabético y "
    "la equivalencia se registra en el archivo codigos_equipos.csv. Como no queda ninguna otra "
    "variable de baja cardinalidad, no se aplica codificación one-hot, que habría creado 48 "
    "columnas binarias adicionales sin aportar información. De esta forma, ni el dataset "
    "depurado ni el archivo del modelo contienen letras: todas sus columnas son numéricas y "
    "pueden entrar directamente al escalador estándar y a la red neuronal del pipeline del "
    "apartado 2.2."
)

LIMPIEZA_TITULO_CODIGO = "Fragmento 2. Limpieza del dataset teams.csv en el notebook de Google Colab."

LIMPIEZA_CODIGO = [
    "# Diagnóstico: nulos, constantes y variables duplicadas",
    "nulos = df.isna().sum()",
    "constantes = [c for c in df.columns if df[c].nunique(dropna=True) <= 1]",
    "numericas = df.select_dtypes(include=[np.number])",
    "grupos = {}",
    "for c in numericas.columns:",
    "    clave = tuple(numericas[c].fillna(-999).round(6).tolist())",
    "    grupos.setdefault(clave, []).append(c)",
    "duplicadas = [g for g in grupos.values() if len(g) > 1]",
    "",
    "# Limpieza: eliminar, imputar y normalizar",
    "df_clean = df.drop(columns=constantes)                     # vacías y constantes",
    "a_eliminar = [c for g in duplicadas for c in g[1:]]          # se conserva la primera",
    "a_eliminar = [c for c in a_eliminar if c in df_clean.columns]",
    "df_clean = df_clean.drop(columns=a_eliminar)                # redundantes",
    "df_clean = df_clean.drop(columns=['team_country'])          # alias del nombre",
    "for c in df_clean.columns[df_clean.isna().any()]:",
    "    df_clean[c] = df_clean[c].fillna(df_clean[c].median())  # imputación",
    "df_clean['goals_per_game'] = (df_clean['goals'] / df_clean['games']).round(3)",
    "df_clean['shots_on_target_per_game'] = (",
    "    df_clean['shots_on_target'] / df_clean['games']).round(3)",
    "",
    "",
    "# Codificación de variables categóricas: el nombre pasa a ser un código entero",
    "codigos = {nombre: i + 1 for i, nombre",
    "           in enumerate(sorted(df_clean['team'].unique()))}",
    "df_clean['team_codigo'] = df_clean['team'].map(codigos)",
    "df_clean = df_clean.drop(columns=['team'])",
    "diccionario = pd.DataFrame(sorted(codigos.items()), columns=['team', 'team_codigo'])",
    "",
    "# Selección de variables y exportación",
    "features = ['goals', 'possession', 'shots_on_target', 'avg_age']",
    "ratios = ['goals_per_game', 'shots_on_target_per_game']",
    "variables = ['team_codigo', 'games'] + features + ratios",
    "df_modelo = df_clean[variables].sort_values('team_codigo')",
    "df_modelo = df_modelo.reset_index(drop=True)",
    "df_clean.to_csv('teams_limpio.csv', index=False)",
    "df_modelo.to_csv('variables_modelo.csv', index=False)",
    "diccionario.to_csv('codigos_equipos.csv', index=False)",
]

LIMPIEZA_CIERRE = (
    "La verificación final del notebook confirma que el archivo resultante no contiene valores "
    "nulos ni variables de texto, mantiene las 48 selecciones sin duplicados y conserva la "
    "trazabilidad de cada "
    "decisión, ya que la celda de diagnóstico precede a la de limpieza y muestra las variables "
    "afectadas antes de transformarlas. El archivo variables_modelo.csv es el que se carga en "
    "el primer paso del pipeline del apartado 2.2, de modo que la red neuronal recibe datos "
    "homogeneizados y comparables entre selecciones."
)


# --------------------------------------------------------------------------
# Construccion del documento
# --------------------------------------------------------------------------


def main():
    if not os.path.exists(SRC):
        raise SystemExit("No se encuentra el documento fuente: {}".format(SRC))

    shutil.copyfile(SRC, DST)
    doc = Document(DST)
    ps = doc.paragraphs

    def buscar(texto, estilo=None, inicio=False):
        for p in ps:
            t = p.text.strip()
            coincide = t.startswith(texto) if inicio else t == texto
            if coincide and (estilo is None or p.style.name == estilo):
                return p
        raise SystemExit("No se encontro el parrafo: {}".format(texto))

    # ---- plantillas -------------------------------------------------------
    tpl_h2 = buscar("2.2. Pipeline de implementación propuesto", "Heading 2")
    tpl_titulo = buscar("Tabla 1. Resumen descriptivo del dataset teams.csv.", "Normal")
    tpl_cuerpo_txt = buscar("El Mundial de la FIFA 2026 trae un cambio", "Normal", inicio=True)
    tpl_codigo = buscar("import pandas as pd", "Normal", inicio=True)
    tpl_tabla = doc.tables[0]

    # ---- encabezado 2.3 ---------------------------------------------------
    p_biblio = None
    for p in ps:
        if p.style.name == "Heading 1" and p.text.strip() == "BIBLIOGRAF\u00cdA":
            p_biblio = p
            break
    if p_biblio is None:
        raise SystemExit("No se encontro el encabezado BIBLIOGRAF\u00cdA")

    limpieza = []
    limpieza.append(_encabezado(tpl_h2, "2.3. Limpieza de datos", 18, "_Toc18"))
    limpieza.append(_nueva_parrafo(tpl_cuerpo_txt, LIMPIEZA_INTRO, keep_next=True))
    limpieza.append(_nueva_parrafo(tpl_cuerpo_txt, LIMPIEZA_DIAGNOSTICO))
    limpieza.append(_nueva_parrafo(tpl_titulo, LIMPIEZA_TITULO_TABLA, keep_next=True))
    limpieza.append(_tabla(tpl_tabla, LIMPIEZA_TITULO_TABLA,
                            LIMPIEZA_ENCABEZADOS, LIMPIEZA_FILAS,
                            [1900, 2900, 2200, 2098]))
    limpieza.append(_nueva_parrafo(tpl_titulo,
                                    "Nota. La limpieza se ejecuta en el notebook "
                                    "Limpieza_FIFA2026_Colab.ipynb."))
    limpieza.append(_nueva_parrafo(tpl_cuerpo_txt, LIMPIEZA_RESULTADO))
    limpieza.append(_nueva_parrafo(tpl_cuerpo_txt, LIMPIEZA_CODIFICACION))
    limpieza.append(_nueva_parrafo(tpl_titulo, LIMPIEZA_TITULO_CODIGO, keep_next=True))
    for linea in LIMPIEZA_CODIGO:
        limpieza.append(_nueva_parrafo(tpl_codigo, linea))
    limpieza.append(_nueva_parrafo(tpl_cuerpo_txt, LIMPIEZA_CIERRE))

    for el in limpieza:
        p_biblio._p.addprevious(el)

    # ---- indice (TOC) -----------------------------------------------------
    toc_pipe = buscar("2.2. Pipeline de implementaci\u00f3n propuesto", "toc 2", inicio=True)
    toc_pipe._p.addnext(_entrada_toc(toc_pipe._p, "_Toc18", "2.3. Limpieza de datos",
                                          estilo=toc_pipe._p.find(qn("w:pPr")).find(qn("w:pStyle")).get(qn("w:val"))))

    _actualizar_campos_al_abrir(doc)
    doc.save(DST)
    print("Documento generado:", DST)


if __name__ == "__main__":
    main()
