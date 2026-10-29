#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera DiseñoMath.docx con ecuaciones nativas de Word (OMML) usando pandoc.
Toma el contenido del informe ya existente, lo pasa a Markdown, reemplaza las
ecuaciones de texto plano por LaTeX y construye el .docx con una plantilla de
estilos propia. No modifica el informe original.
"""

import copy
import os
import re
import shutil
import subprocess
import sys
import tempfile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import (
    WD_ALIGN_PARAGRAPH,
    WD_TAB_ALIGNMENT,
    WD_TAB_LEADER,
)
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.shared import Cm, Pt, RGBColor

PROYECTO = "/home/eynor/Documents/5_Class/sistemas-control/1_Proyecto"
BASE_DOCX = os.path.join(PROYECTO, "Informe_Proyecto_Sistemas_de_Control_ESP32-C3.docx")
SALIDA = os.path.join(PROYECTO, "2_Proyecto_SisContrl.docx")
LOGO = "/home/eynor/Documents/2_Proyect_Private/0_biblioteca-Skills/logoUnifranz/logounifranz.png"

TMP = "/tmp/opencode/diseno_math"
MD_RAW = os.path.join(TMP, "extraido.md")
MD = os.path.join(TMP, "diseno_math.md")
REF = os.path.join(TMP, "referencia.docx")

os.makedirs(TMP, exist_ok=True)


def ejecutar(cmd):
    resultado = subprocess.run(cmd, text=True, capture_output=True)
    if resultado.returncode != 0:
        print(resultado.stdout)
        print(resultado.stderr, file=sys.stderr)
        raise SystemExit(resultado.returncode)
    return resultado


PAGEBREAK = """```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```"""

TOC_FIELD = r"""```{=openxml}
<w:p>
  <w:r><w:fldChar w:fldCharType="begin"/></w:r>
  <w:r><w:instrText xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText></w:r>
  <w:r><w:fldChar w:fldCharType="separate"/></w:r>
  <w:r><w:t>Actualice el índice en Word: clic derecho → Actualizar campos.</w:t></w:r>
  <w:r><w:fldChar w:fldCharType="end"/></w:r>
</w:p>
```"""


# ---------------------------------------------------------------------------
# 1. Extraer el contenido actual del informe
# ---------------------------------------------------------------------------
def extraer_markdown():
    ejecutar(["pandoc", BASE_DOCX, "-t", "markdown", "-o", MD_RAW, "--wrap=none"])
    with open(MD_RAW, encoding="utf-8") as f:
        return f.read()


def datos_portada(raw):
    lineas = raw.splitlines()
    titulo = ""
    for linea in lineas:
        if "SISTEMA PORTÁTIL" in linea and linea.strip().startswith("**"):
            titulo = linea.strip().strip("*").strip().strip('"“”')
            break

    idx_est = next(i for i, l in enumerate(lineas) if l.strip() == "**ESTUDIANTES:**")
    idx_doc = next(i for i, l in enumerate(lineas) if l.strip() == "**DOCENTE:**")
    nombres = [
        l.strip() for l in lineas[idx_est + 1:idx_doc]
        if l.strip() and not l.strip().startswith("**")
    ]
    docente = ""
    for linea in lineas[idx_doc + 1:]:
        if linea.strip() and not linea.strip().startswith("**"):
            docente = linea.strip()
            break
    return titulo, nombres, docente


def portada_md(titulo, nombres, docente):
    nombres_md = "\n\n".join(nombres)
    return f"""::: {{custom-style="Cover Universidad"}}
UNIVERSIDAD PRIVADA FRANZ TAMAYO
:::

::: {{custom-style="Cover Facultad"}}
FACULTAD DE INGENIERÍA
:::

::: {{custom-style="Cover Carrera"}}
CARRERA DE INGENIERÍA DE SISTEMAS
:::

::: {{custom-style="Cover Asignatura"}}
ASIGNATURA: SISTEMAS DE CONTROL
:::

::: {{custom-style="Cover Proyecto"}}
PROYECTO DE INVESTIGACIÓN
:::

![Logo]({LOGO}){{width=5.0cm}}

::: {{custom-style="Cover Titulo"}}
“{titulo}”
:::

::: {{custom-style="Cover Etiqueta"}}
ESTUDIANTES:
:::

::: {{custom-style="Cover Autor"}}
{nombres_md}
:::

::: {{custom-style="Cover Etiqueta"}}
DOCENTE:
:::

::: {{custom-style="Cover Autor"}}
{docente}
:::

::: {{custom-style="Cover Lugar"}}
EL ALTO – BOLIVIA
:::

::: {{custom-style="Cover Anio"}}
2025
:::

{PAGEBREAK}

::: {{custom-style="Indice Titulo"}}
ÍNDICE
:::

{TOC_FIELD}

{PAGEBREAK}
"""


# ---------------------------------------------------------------------------
# 2. Integrar el contenido de Laplace en las secciones pendientes
# ---------------------------------------------------------------------------
def integrar_laplace(cuerpo):
    def cambiar(viejo, nuevo, etiqueta):
        if viejo not in cuerpo:
            print(
                f"ADVERTENCIA: no se encontró el bloque de {etiqueta}.",
                file=sys.stderr,
            )
            return cuerpo
        return cuerpo.replace(viejo, nuevo, 1)

    # 6.2 Definición formal de la transformada de Laplace
    viejo_62 = (
        "La función de transferencia relaciona la salida con la entrada de un "
        "sistema lineal e invariante en el tiempo, en el dominio de Laplace. Se "
        "define como G(s) = Y(s)/U(s), con condiciones iniciales nulas. Sus "
        "polos determinan la estabilidad y su forma permite identificar si el "
        "sistema es de primer orden, de segundo orden o de orden superior."
    )
    nuevo_62 = (
        viejo_62
        + "\n\n"
        + r"""De forma más formal, para una señal $f(t)$ definida para $t \ge 0$, la transformada de Laplace se define como

$$F(s) = \mathcal{L}\{f(t)\} = \int_{0}^{\infty} f(t)e^{-st}\,dt.$$

La propiedad que interesa aquí es que la derivada de orden $n$ se transforma en una multiplicación por $s^n$,

$$\mathcal{L}\left\{\frac{d^n f(t)}{dt^n}\right\} = s^n F(s),$$

si las condiciones iniciales son nulas. Así, una ecuación diferencial lineal se convierte en una relación algebraica entre $Y(s)$ y $U(s)$, y de allí se obtiene $G(s)=Y(s)/U(s)$."""
    )
    cuerpo = cambiar(viejo_62, nuevo_62, "6.2")

    # 7.2 Modelo térmico y función descriptiva de la histéresis
    viejo_72 = r"""Como punto de partida para el canal de temperatura se propone un modelo de primer orden, habitual en sensores térmicos:

*G(s) = K / (τs + 1)*

Donde K es la ganancia estática y τ la constante de tiempo. Los valores concretos deben obtenerse de la hoja de datos del MAX30205 o de una prueba de respuesta. No se inventan aquí.

**[PENDIENTE --- completar las ecuaciones definitivas del modelo (planta, sensor y lazo de control) y justificar cada parámetro.]{.mark}**"""
    nuevo_72 = r"""El canal de temperatura se modela por primeros principios. Si $T_{skin}(t)$ es la temperatura de la piel y $T_{sensor}(t)$ la del encapsulado, el balance de energía en el sensor es

$$C_{th}\frac{dT_{sensor}(t)}{dt} + \frac{T_{sensor}(t)-T_{skin}(t)}{R_{th}} = 0,$$

donde $R_{th}$ es la resistencia térmica del encapsulado y $C_{th}$ su capacidad térmica. Al definir $\tau = R_{th}C_{th}$, la ecuación queda en la forma estándar de primer orden:

$$\tau\frac{dT_{sensor}(t)}{dt} + T_{sensor}(t) = T_{skin}(t).$$

Con condiciones iniciales nulas y aplicando Laplace se obtiene

$$G_{temp}(s) = \frac{T_{sensor}(s)}{T_{skin}(s)} = \frac{K}{\tau s + 1},$$

con $K=1$ en estado estacionario. Para el MAX30205 se adopta $\tau \approx 30$ s, valor coherente con el tiempo de estabilización térmica del encapsulado TDFN y con la norma ASTM E1112; este valor es una estimación teórica inicial y debe validarse con una prueba de respuesta.

El lazo de alerta no es lineal: el motor vibrador se gobierna con un MOSFET en modo ON-OFF y la decisión incluye una banda de histéresis. Para analizarlo con herramientas frecuenciales se usa la función descriptiva del relé con histéresis:

$$N(A) = \frac{4M}{\pi A}\left(\sqrt{1-(\Delta/A)^2} - j\frac{\Delta}{A}\right),$$

La expresión es válida para $A \ge \Delta$.

donde $M$ es la tensión de activación del MOSFET y $\Delta$ es el semi-ancho de la banda de histéresis (por ejemplo, $2.5$ bpm para la frecuencia cardíaca o $0.15$ °C para la temperatura). La condición de ciclo límite se plantea como

$$1 + G(j\omega)N(A) = 0 \quad \Rightarrow \quad G(j\omega) = -\frac{1}{N(A)}.$$

Si las curvas no se intersecan, el lazo supervisor no presenta oscilaciones autosostenidas. La implementación en firmware sigue siendo la ecuación discreta de histéresis ya presentada; la función descriptiva es la herramienta de análisis, no una ecuación que se programe en el ESP32-C3."""
    cuerpo = cambiar(viejo_72, nuevo_72, "7.2")

    # 7.3 Funciones de transferencia de los canales
    viejo_73 = r"""La función de transferencia definitiva se obtendrá del modelo que se implemente en Simulink. Para el sensor térmico se parte de la forma de primer orden ya presentada. Para el lazo de alerta, en cambio, la función de transferencia no describe un actuador físico: describe la relación entre la señal de entrada y la decisión de alarma, que es discreta y no lineal.

Esa diferencia es importante. Un PID clásico se aplica a un lazo continuo. La alerta por umbrales se analiza mejor como un autómata de estados o como un sistema híbrido. En Simulink, la lógica se puede implementar con bloques de comparación, memoria y temporización, o con Stateflow.

**[PENDIENTE --- insertar la función de transferencia final y su deducción.]{.mark}**"""
    nuevo_73 = r"""La función de transferencia de cada canal se deduce del modelo físico y después se implementa en Simulink. Para el canal térmico, la deducción anterior conduce a

$$G_{temp}(s) = \frac{1}{30s + 1},$$

cuyo polo real está en $s=-1/30 \approx -0.0333$ rad/s. La ganancia estática es unitaria porque, en equilibrio, la lectura del sensor iguala la temperatura de la piel.

Para la señal PPG del MAX30102 se propone un acondicionador pasa-banda de segundo orden. La etapa pasa-altas elimina la componente continua y la deriva de la línea base,

$$G_{HP}(s) = \frac{s}{s+\pi},$$

con frecuencia de corte inferior $f_L = 0.5$ Hz. La etapa pasa-bajas elimina el ruido de alta frecuencia,

$$G_{LP}(s) = \frac{10\pi}{s+10\pi},$$

con frecuencia de corte superior $f_H = 5.0$ Hz. Al multiplicar ambas etapas,

$$G_{PPG}(s) = \left(\frac{s}{s+\pi}\right)\left(\frac{10\pi}{s+10\pi}\right),$$

y al desarrollar el producto,

$$G_{PPG}(s) = \frac{31.42s}{s^2+34.56s+98.70}.$$

El cero en el origen anula la componente DC y los polos en $s\approx-3.1416$ y $s\approx-31.4159$ rad/s limitan la banda a las frecuencias fisiológicas del pulso (30 a 300 bpm).

Para el MPU6050 se adopta un modelo mecánico de segundo orden subamortiguado:

$$G_{acc}(s) = \frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}.$$

Con el filtro digital interno configurado a 20 Hz, $\omega_n = 40\pi \approx 125.66$ rad/s, y con $\zeta=0.707$ para minimizar el sobreimpulso, queda

$$G_{acc}(s) = \frac{15791.36}{s^2+177.68s+15791.36}.$$

Estas tres funciones describen los canales lineales. El lazo supervisor de alerta no se representa con una $G(s)$ lineal: por la conmutación y la histéresis se analiza con la función descriptiva $N(A)$ de la sección 7.2. Esa separación permite combinar modelos continuos para los sensores con lógica discreta para la alarma."""
    cuerpo = cambiar(viejo_73, nuevo_73, "7.3")

    # 7.4 Descripción textual del lazo
    viejo_74 = "**[PENDIENTE --- insertar el diagrama de bloques del sistema.]{.mark}**"
    nuevo_74 = r"""El lazo se ordena así: los sensores entregan las variables medidas; el acondicionamiento y el filtro digital generan $y[k]$; el comparador calcula $e[k]=r[k]-y[k]$; el bloque de histéresis decide el estado de alarma; y la salida del ESP32-C3 excita la compuerta del MOSFET que enciende el motor vibrador. La realimentación es la lectura continua de los sensores. El diagrama se insertará en el espacio reservado."""
    cuerpo = cambiar(viejo_74, nuevo_74, "7.4")

    # 8.2 PID filtrado, Tustin y ecuación en diferencias
    viejo_82 = "**[PENDIENTE --- definir los valores de Kp, Ki y Kd y la ecuación final implementada.]{.mark}**"
    nuevo_82 = r"""Para reducir la amplificación de ruido del término derivativo del PID se agrega un polo de filtrado:

$$C(s) = K_p + \frac{K_i}{s} + \frac{K_d s}{\alpha s+1}.$$

La ecuación en diferencias hacia atrás ya presentada es una forma de implementar el PID. Para el filtro del sensor se usa la transformación bilineal de Tustin,

$$s \approx \frac{2}{T_s}\frac{z-1}{z+1},$$

con $T_s=1.0$ s para el canal de temperatura y $T_s=0.02$ s para los canales PPG e inercial. Aplicada a $G_{temp}(s)=1/(30s+1)$, la transformación produce

$$G_{temp}(z) = \frac{0.016393 + 0.016393z^{-1}}{1 - 0.967213z^{-1}},$$

y la ecuación de diferencias implementable en el ESP32-C3 es

$$y[k] = 0.967213\,y[k-1] + 0.016393\,x[k] + 0.016393\,x[k-1],$$

donde $x[k]$ es la lectura cruda del MAX30205 y $y[k]$ la temperatura filtrada. Esta ecuación es un filtro IIR de primer orden que se ejecuta en el firmware.

En esta versión el control implementado sigue siendo on/off con histéresis; el PID queda como alternativa para el canal de temperatura y para la comparación en Simulink. Por eso los valores de $K_p$, $K_i$ y $K_d$ no se fijan en el firmware: se ajustan en la simulación y se validan antes de cualquier implementación real."""
    cuerpo = cambiar(viejo_82, nuevo_82, "8.2")

    # 8.3 Parámetros teóricos del modelo
    viejo_83 = "**[PENDIENTE --- documentar el método de ajuste y los valores finales.]{.mark}**"
    nuevo_83 = r"""Los parámetros teóricos del modelo quedan así: para el canal térmico, $K=1$, $\tau=30$ s y un polo en $s=-0.0333$ rad/s; para el PPG, $f_L=0.5$ Hz y $f_H=5.0$ Hz; para el acelerómetro, $\omega_n=125.66$ rad/s y $\zeta=0.707$. En la histéresis, el semi-ancho es $\Delta=2.5$ bpm para la frecuencia cardíaca, $\Delta=0.15$ °C para la temperatura y $\Delta=1$ % para la SpO2, de modo que las bandas totales coinciden con la tabla anterior. Estos valores son el punto de partida teórico; la validación con el prototipo y con equipos de referencia sigue siendo la etapa que confirma o corrige el ajuste."""
    cuerpo = cambiar(viejo_83, nuevo_83, "8.3")

    # 9.1 Configuración del solver
    viejo_91 = (
        "La versión de MATLAB/Simulink está pendiente de confirmar. Conviene "
        "anotarla en el informe final porque los resultados pueden variar "
        "ligeramente entre versiones."
    )
    nuevo_91 = (
        viejo_91
        + "\n\n"
        + r"""Para la simulación se propone el solver ode4 con paso fijo de $0.01$ s. Ese paso es menor que el período de $0.02$ s de los sensores rápidos (50 Hz) y que el período de $1$ s del lazo de decisión, de modo que la discretización no domina la dinámica del modelo."""
    )
    cuerpo = cambiar(viejo_91, nuevo_91, "9.1")

    # 15.3 Configuración de los bloques de Simulink
    viejo_153 = "**[PENDIENTE --- adjuntar el modelo .slx y las capturas de Simulink.]{.mark}**"
    nuevo_153 = r"""El modelo de Simulink se armará con tres bloques principales. Para el canal térmico se usa un bloque Transfer Fcn con numerador $[1]$ y denominador $[30\ 1]$. La histéresis se implementa con un bloque Relay: encendido en $+5$ bpm o $+0.3$ °C y apagado en $-5$ bpm o $-0.3$ °C, según el canal. La salida se observa en un Scope conectado al motor de vibración. El archivo .slx y las capturas se adjuntarán cuando se ejecute la simulación."""
    cuerpo = cambiar(viejo_153, nuevo_153, "15.3")

    return cuerpo


# ---------------------------------------------------------------------------
# 2. Transformar el cuerpo: encabezados, listas y ecuaciones
# ---------------------------------------------------------------------------
def transformar_cuerpo(raw):
    inicio = raw.find("# **RESUMEN**")
    if inicio < 0:
        inicio = raw.find("# RESUMEN")
    if inicio < 0:
        raise RuntimeError("No se encontró el inicio del cuerpo (RESUMEN).")
    cuerpo = raw[inicio:]

    # Encabezados sin negritas internas
    cuerpo = re.sub(r"^(#{1,6})\s+\*\*(.+?)\*\*\s*$", r"\1 \2", cuerpo, flags=re.M)

    # Viñetas del documento original a listas Markdown
    cuerpo = re.sub(r"^[ \t]*•[ \t]+", "- ", cuerpo, flags=re.M)

    # Unir los ítems de una misma lista (dejando una línea en blanco antes)
    lineas = cuerpo.split("\n")
    salida_listas = []
    for i, linea in enumerate(lineas):
        if (
            linea.strip() == ""
            and i + 1 < len(lineas)
            and lineas[i + 1].startswith("- ")
        ):
            if (
                not salida_listas
                or salida_listas[-1].strip() == ""
                or salida_listas[-1].startswith("- ")
            ):
                continue
            salida_listas.append("")
            continue
        salida_listas.append(linea)
    cuerpo = "\n".join(salida_listas)

    # --- Contenido de Laplace en las secciones pendientes ---
    cuerpo = integrar_laplace(cuerpo)

    # --- Ecuaciones de texto plano -> LaTeX ---
    pid = (
        "$$u(t) = K_p\\,e(t) + K_i \\int e(t)\\,dt + "
        "K_d\\,\\frac{de(t)}{dt}$$"
    )
    cuerpo = cuerpo.replace(
        "*u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt*", pid
    )

    pid_discreto = (
        "$$u[k] = K_p\\,e[k] + K_i \\sum_{j} e[j]\\,\\Delta t + "
        "K_d\\,\\frac{e[k] - e[k-1]}{\\Delta t}$$"
    )
    cuerpo = cuerpo.replace(
        "*u\\[k\\] = Kp·e\\[k\\] + Ki·Σe\\[j\\]·Δt + "
        "Kd·(e\\[k\\] − e\\[k−1\\])/Δt*",
        pid_discreto,
    )

    cuerpo = cuerpo.replace(
        "*e\\[k\\] = r\\[k\\] − y\\[k\\]*",
        "$$e[k] = r[k] - y[k]$$",
    )
    cuerpo = cuerpo.replace(
        "*G(s) = K / (τs + 1)*",
        "$$G(s) = \\frac{K}{\\tau s + 1}$$",
    )

    # Bloque de histéresis: reemplazo por una ecuación con casos
    ini_h = cuerpo.find("*u\\[k\\] = 1, si")
    if ini_h >= 0:
        fin_h = cuerpo.find("en otro caso*", ini_h)
        if fin_h >= 0:
            fin_h += len("en otro caso*")
            hist = (
                "$$u[k] = \\begin{cases}\n"
                "1, & e[k] > +h \\\\\n"
                "0, & e[k] < -h \\\\\n"
                "u[k-1], & \\text{en otro caso}\n"
                "\\end{cases}$$"
            )
            cuerpo = cuerpo[:ini_h] + hist + cuerpo[fin_h:]

    # Expresiones en línea
    reemplazos = [
        ("G(s) = Y(s)/U(s)", "$G(s) = Y(s)/U(s)$"),
        ("G(s) = K/(τs + 1)", "$G(s) = K/(\\tau s + 1)$"),
        ("r\\[k\\]", "$r[k]$"),
        ("y\\[k\\]", "$y[k]$"),
        ("e\\[k\\]", "$e[k]$"),
        ("u\\[k−1\\]", "$u[k-1]$"),
        ("u\\[k\\]", "$u[k]$"),
        ("Δt", "$\\Delta t$"),
        ("Kp, Ki y Kd", "$K_p$, $K_i$ y $K_d$"),
    ]
    for viejo, nuevo in reemplazos:
        cuerpo = cuerpo.replace(viejo, nuevo)

    # Saltos de página antes de cada sección principal
    lineas = cuerpo.splitlines()
    salida = []
    visto_h1 = False
    for linea in lineas:
        if re.match(r"^#\s+", linea):
            if visto_h1:
                salida.extend(["", PAGEBREAK, ""])
            visto_h1 = True
        salida.append(linea)
    return "\n".join(salida).strip() + "\n"


# ---------------------------------------------------------------------------
# 3. Plantilla de estilos para pandoc
# ---------------------------------------------------------------------------
def fuente(style, size=12, bold=False, italic=False):
    style.font.name = "Arial"
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = RGBColor(0, 0, 0)


def parrafo(style, alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY, interlineado=1.5,
            sangria=1.25, antes=0, despues=0, keep=False):
    pf = style.paragraph_format
    pf.alignment = alineacion
    pf.line_spacing = interlineado
    pf.first_line_indent = Cm(sangria)
    pf.left_indent = Cm(0)
    pf.space_before = Pt(antes)
    pf.space_after = Pt(despues)
    pf.keep_with_next = keep


def crear_referencia():
    with open(REF, "wb") as f:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            stdout=f, check=True,
        )
    doc = Document(REF)

    for section in doc.sections:
        section.page_width = Cm(21.59)
        section.page_height = Cm(27.94)
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.54)

    normal = doc.styles["Normal"]
    fuente(normal, 12)
    parrafo(normal)

    for nombre in ("Body Text", "First Paragraph"):
        st = doc.styles[nombre]
        fuente(st, 12)
        parrafo(st)

    compact = doc.styles["Compact"]
    fuente(compact, 12)
    parrafo(compact, WD_ALIGN_PARAGRAPH.LEFT, 1.5, 0)

    h1 = doc.styles["Heading 1"]
    fuente(h1, 14, bold=True)
    parrafo(h1, WD_ALIGN_PARAGRAPH.LEFT, 1.5, 0, 18, 8, keep=True)

    h2 = doc.styles["Heading 2"]
    fuente(h2, 12, bold=True)
    parrafo(h2, WD_ALIGN_PARAGRAPH.LEFT, 1.5, 0, 12, 6, keep=True)

    h3 = doc.styles["Heading 3"]
    fuente(h3, 12, bold=True)
    parrafo(h3, WD_ALIGN_PARAGRAPH.LEFT, 1.5, 0, 12, 6, keep=True)

    existentes = {s.name: s for s in doc.styles}
    for nombre in ("Caption", "Table Caption"):
        if nombre in existentes:
            st = existentes[nombre]
            fuente(st, 10, italic=True)
            parrafo(st, WD_ALIGN_PARAGRAPH.LEFT, 1.0, 0, 3, 3)

    if "TOC Heading" in existentes:
        st = existentes["TOC Heading"]
        fuente(st, 14, bold=True)
        parrafo(st, WD_ALIGN_PARAGRAPH.LEFT, 1.15, 0, 0, 12)

    for nivel in range(1, 4):
        nombre = "TOC " + str(nivel)
        if nombre in existentes:
            st = existentes[nombre]
        else:
            st = doc.styles.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        fuente(st, 12)
        parrafo(
            st,
            WD_ALIGN_PARAGRAPH.LEFT,
            1.5,
            0,
            0,
            0,
        )
        st.paragraph_format.left_indent = Cm(0.388 * (nivel - 1))
        st.paragraph_format.first_line_indent = Cm(0)
        st.paragraph_format.tab_stops.add_tab_stop(
            Cm(15.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )

    def crear(nombre, size, bold=False, antes=0, despues=0, interlineado=1.15):
        st = doc.styles.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles["Normal"]
        fuente(st, size, bold=bold)
        parrafo(st, WD_ALIGN_PARAGRAPH.CENTER, interlineado, 0, antes, despues)
        return st

    crear("Cover Universidad", 14, bold=True, despues=2)
    crear("Cover Facultad", 13, bold=True, despues=2)
    crear("Cover Carrera", 13, bold=True, despues=8)
    crear("Cover Asignatura", 12, bold=True, despues=2)
    crear("Cover Proyecto", 12, bold=True, despues=12)
    crear("Cover Titulo", 13, bold=True, antes=10, despues=16)
    crear("Cover Etiqueta", 12, bold=True, antes=10, despues=2)
    crear("Cover Autor", 12, antes=0, despues=0)
    crear("Cover Lugar", 12, bold=True, antes=14, despues=0)
    crear("Cover Anio", 12, bold=True, antes=0, despues=0)
    crear("Indice Titulo", 14, bold=True, despues=12)

    section = doc.sections[0]
    section.different_first_page_header_footer = True

    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.first_line_indent = Cm(0)
    run = hp.add_run()
    run.font.name = "Arial"
    run.font.size = Pt(10)
    f1 = OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    run._r.append(f1)
    run2 = hp.add_run()
    run2.font.name = "Arial"
    run2.font.size = Pt(10)
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    run2._r.append(instr)
    run3 = hp.add_run()
    run3.font.name = "Arial"
    run3.font.size = Pt(10)
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "separate")
    run3._r.append(f2)
    run4 = hp.add_run("1")
    run4.font.name = "Arial"
    run4.font.size = Pt(10)
    run5 = hp.add_run()
    f3 = OxmlElement("w:fldChar")
    f3.set(qn("w:fldCharType"), "end")
    run5._r.append(f3)

    first = section.first_page_header
    first.is_linked_to_previous = False
    for p in first.paragraphs:
        p.clear()

    doc.save(REF)


# ---------------------------------------------------------------------------
# 4. Post-proceso del .docx generado
# ---------------------------------------------------------------------------
def bordes_celda(celda, lados, color="000000", tipo="single", sz="6"):
    tcPr = celda._tc.get_or_add_tcPr()
    for viejo in tcPr.findall(qn("w:tcBorders")):
        tcPr.remove(viejo)
    xml = f'<w:tcBorders {nsdecls("w")}>'
    for lado in lados:
        xml += f'<w:{lado} w:val="{tipo}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
    xml += "</w:tcBorders>"
    tcPr.append(parse_xml(xml))


def ancho_tabla(tabla, anchos, alto_cm=None):
    tabla.autofit = False
    for i, ancho in enumerate(anchos):
        tabla.columns[i].width = Cm(ancho)
    for fila in tabla.rows:
        for i, ancho in enumerate(anchos):
            fila.cells[i].width = Cm(ancho)
    if alto_cm:
        trPr = tabla.rows[0]._tr.get_or_add_trPr()
        alto = OxmlElement("w:trHeight")
        alto.set(qn("w:val"), str(int(alto_cm * 567)))
        alto.set(qn("w:hRule"), "atLeast")
        trPr.append(alto)


def entradas_indice_original():
    doc = Document(BASE_DOCX)
    entradas = []
    for p in doc.paragraphs:
        nombre = p.style.name.lower()
        if nombre in ("toc 1", "toc 2", "toc 3") and "\t" in p.text:
            titulo, pagina = p.text.rsplit("\t", 1)
            titulo = titulo.strip()
            pagina = pagina.strip()
            if titulo and pagina.isdigit():
                entradas.append((int(nombre[-1]), titulo, pagina))
    return entradas


def insertar_indice_estatico(doc):
    entradas = entradas_indice_original()
    if not entradas:
        return

    toc_p = None
    for p in doc.paragraphs:
        for instr in p._p.iter(qn("w:instrText")):
            if "TOC" in (instr.text or ""):
                toc_p = p
                break
        if toc_p is not None:
            break
    if toc_p is None:
        return

    def estilo(nivel):
        return doc.styles["TOC " + str(nivel)].style_id

    p = toc_p._p
    pPr = p.get_or_add_pPr()
    for hijo in list(pPr):
        pPr.remove(hijo)
    pStyle = OxmlElement("w:pStyle")
    pStyle.set(qn("w:val"), estilo(entradas[0][0]))
    pPr.append(pStyle)
    for hijo in list(p):
        if hijo is not pPr:
            p.remove(hijo)

    def campo(tipo):
        r = OxmlElement("w:r")
        fld = OxmlElement("w:fldChar")
        fld.set(qn("w:fldCharType"), tipo)
        r.append(fld)
        p.append(r)

    campo("begin")
    r = OxmlElement("w:r")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = ' TOC \\o "1-3" \\h \\z \\u '
    r.append(instr)
    p.append(r)
    campo("separate")

    def texto(elemento, valor):
        r = OxmlElement("w:r")
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = valor
        r.append(t)
        elemento.append(r)

    def tabulador(elemento):
        r = OxmlElement("w:r")
        r.append(OxmlElement("w:tab"))
        elemento.append(r)

    nivel, titulo, pagina = entradas[0]
    texto(p, titulo)
    tabulador(p)
    texto(p, pagina)

    cursor = p
    for nivel, titulo, pagina in entradas[1:]:
        nueva = OxmlElement("w:p")
        nuevo_pPr = OxmlElement("w:pPr")
        nuevo_estilo = OxmlElement("w:pStyle")
        nuevo_estilo.set(qn("w:val"), estilo(nivel))
        nuevo_pPr.append(nuevo_estilo)
        nueva.append(nuevo_pPr)
        texto(nueva, titulo)
        tabulador(nueva)
        texto(nueva, pagina)
        cursor.addnext(nueva)
        cursor = nueva

    r = OxmlElement("w:r")
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "end")
    r.append(fld)
    cursor.append(r)


def separar_portada_indice(doc):
    saltos = []
    for p in doc.paragraphs:
        for br in p._p.iter(qn("w:br")):
            if br.get(qn("w:type")) == "page":
                saltos.append(p)
                break
    if len(saltos) < 2:
        return

    corte = saltos[1]
    cuerpo_sectPr = doc.sections[-1]._sectPr
    copia = copy.deepcopy(cuerpo_sectPr)
    for tag in ("w:headerReference", "w:footerReference",
                "w:titlePg", "w:pgNumType"):
        for el in copia.findall(qn(tag)):
            copia.remove(el)

    p = corte._p
    pPr = p.get_or_add_pPr()
    for hijo in list(p):
        if hijo is not pPr:
            p.remove(hijo)
    pPr.append(copia)

    for el in cuerpo_sectPr.findall(qn("w:titlePg")):
        cuerpo_sectPr.remove(el)
    if cuerpo_sectPr.find(qn("w:pgNumType")) is None:
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), "1")
        cuerpo_sectPr.insert_element_before(
            pg,
            "w:cols", "w:formProt", "w:vAlign", "w:noEndnote",
            "w:titlePg", "w:textDirection", "w:bidi", "w:rtlGutter",
            "w:docGrid", "w:printerSettings", "w:sectPrChange",
        )


def postprocesar():
    doc = Document(SALIDA)

    doc.core_properties.title = (
        "SISTEMA PORTÁTIL DE MONITOREO DE SIGNOS VITALES BASADO EN ESP32-C3 "
        "PARA SUPERVISIÓN REMOTA DE PERSONAS MAYORES O ENFERMOS CARDÍACOS"
    )
    doc.core_properties.subject = "Sistemas de Control"
    doc.core_properties.keywords = "ESP32-C3, signos vitales, IoT, control, Simulink"

    # Portada sin número
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    first = section.first_page_header
    first.is_linked_to_previous = False
    for p in first.paragraphs:
        p.clear()

    separar_portada_indice(doc)
    insertar_indice_estatico(doc)

    # Actualizar campos al abrir en Word
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is None:
        upd = OxmlElement("w:updateFields")
        upd.set(qn("w:val"), "true")
        settings.append(upd)

    # Ecuaciones desplegadas centradas
    for p in doc.paragraphs:
        if p._p.findall(".//" + qn("m:oMathPara")):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)

    # Comentarios en los avisos PENDIENTE
    comentarios = {
        "ecuaciones definitivas": "Completar el modelo matemático: planta, sensor, "
        "linealización, parámetros y condiciones iniciales.",
        "función de transferencia final": "Insertar la función de transferencia y su "
        "deducción, con numerador, denominador, polos y ceros.",
        "diagrama de bloques": "Insertar el diagrama de bloques con planta, sensor, "
        "controlador, salida y realimentación.",
        "Kp, Ki y Kd": "Definir los parámetros del controlador, el método de ajuste y "
        "la ecuación final implementada.",
        "definir los valores de": "Definir los parámetros del controlador, el método "
        "de ajuste y la ecuación final implementada.",
        "método de ajuste": "Documentar las pruebas de ajuste, los valores elegidos y "
        "la comparación con equipos de referencia.",
        "gráficas y capturas de Simulink": "Agregar el modelo en Simulink, la respuesta "
        "al escalón, las perturbaciones y la comparación on/off vs. PID.",
        "análisis con los datos reales": "Reemplazar con la interpretación de las "
        "gráficas y la comparación sin control vs. con control.",
        ".slx": "Adjuntar el modelo .slx, la configuración del solver y las capturas.",
        "esquema electrónico": "Insertar el esquema electrónico y el diagrama de "
        "funcionamiento con el usuario.",
    }
    for p in doc.paragraphs:
        texto = p.text.strip()
        if texto.startswith("PENDIENTE"):
            mensaje = "Completar esta sección."
            for clave, valor in comentarios.items():
                if clave.lower() in texto.lower():
                    mensaje = valor
                    break
            if p.runs:
                doc.add_comment(runs=p.runs, text=mensaje, author="Equipo",
                                initials="EQ")

    # Tablas: tipografía, bordes y anchos
    for tabla in doc.tables:
        es_caja = len(tabla.rows) == 1 and len(tabla.columns) == 1
        if es_caja:
            tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
            texto_caja = tabla.cell(0, 0).text.lower()
            alto = 6.0
            if "diagrama de bloques" in texto_caja:
                alto = 6.5
            elif ".slx" in texto_caja:
                alto = 7.0
            elif "esquema" in texto_caja or "funcionamiento" in texto_caja:
                alto = 6.5
            ancho_tabla(tabla, [16.05], alto_cm=alto)
            celda = tabla.cell(0, 0)
            for p in celda.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.first_line_indent = Cm(0)
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(10)
                    r.font.italic = True
                    r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
            bordes_celda(celda, ["top", "left", "bottom", "right"],
                         color="999999", tipo="single", sz="6")
            continue

        tabla.alignment = WD_TABLE_ALIGNMENT.LEFT
        for fila in tabla.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    p.paragraph_format.first_line_indent = Cm(0)
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        r.font.name = "Arial"
                        r.font.size = Pt(10)
        for celda in tabla.rows[0].cells:
            for p in celda.paragraphs:
                for r in p.runs:
                    r.font.bold = True
            bordes_celda(celda, ["top", "bottom"], sz="6")
        for celda in tabla.rows[-1].cells:
            bordes_celda(celda, ["bottom"], sz="6")

        encabezados = [c.text.strip() for c in tabla.rows[0].cells]
        if len(encabezados) == 4 and encabezados[0] == "Variable":
            ancho_tabla(tabla, [3.6, 2.2, 7.4, 2.3])
        elif len(encabezados) == 4 and encabezados[0] == "Parámetro":
            ancho_tabla(tabla, [4.0, 3.3, 4.9, 3.3])
        elif len(encabezados) == 2 and encabezados[0] == "Métrica":
            ancho_tabla(tabla, [5.4, 9.6])
        elif len(encabezados) == 3 and encabezados[0] == "N.º":
            ancho_tabla(tabla, [1.4, 6.4, 7.2])
        elif len(encabezados) == 3 and encabezados[0] == "Variable":
            ancho_tabla(tabla, [4.4, 5.4, 5.2])

    # Referencias con sangría francesa
    en_refs = False
    for p in doc.paragraphs:
        if p.style.name.startswith("Heading 1") and "REFERENCIAS" in p.text.upper():
            en_refs = True
            continue
        if en_refs and p.style.name.startswith("Heading 1"):
            break
        if en_refs and p.text.strip():
            p.paragraph_format.left_indent = Cm(1.25)
            p.paragraph_format.first_line_indent = Cm(-1.25)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(6)

    doc.save(SALIDA)


def actualizar_indice_desde_pdf():
    """Ajusta los números de página del índice estático con la paginación real."""
    if not shutil.which("soffice") or not shutil.which("pdftotext"):
        print(
            "ADVERTENCIA: no se encontró soffice o pdftotext; "
            "el índice queda con la paginación original.",
            file=sys.stderr,
        )
        return

    with tempfile.TemporaryDirectory(prefix="toc_") as tmp:
        conversion = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                tmp,
                SALIDA,
            ],
            capture_output=True,
            text=True,
        )
        pdf = os.path.join(
            tmp, os.path.splitext(os.path.basename(SALIDA))[0] + ".pdf"
        )
        if conversion.returncode != 0 or not os.path.exists(pdf):
            print(
                "ADVERTENCIA: no se pudo convertir el documento a PDF; "
                "el índice queda con la paginación original.",
                file=sys.stderr,
            )
            return

        info = subprocess.run(
            ["pdfinfo", pdf], capture_output=True, text=True
        ).stdout
        coincidencia = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
        if not coincidencia:
            return
        paginas = []
        for numero in range(1, int(coincidencia.group(1)) + 1):
            texto = subprocess.run(
                [
                    "pdftotext",
                    "-layout",
                    "-f",
                    str(numero),
                    "-l",
                    str(numero),
                    pdf,
                    "-",
                ],
                capture_output=True,
                text=True,
            ).stdout
            paginas.append(texto)

        def normalizar(valor):
            return re.sub(r"\s+", " ", valor).strip()

        inicio_cuerpo = None
        for indice, texto in enumerate(paginas):
            if any(
                normalizar(linea) == "RESUMEN"
                for linea in texto.splitlines()
            ):
                inicio_cuerpo = indice
                break
        if inicio_cuerpo is None:
            return

        def pagina_de(titulo):
            objetivo = normalizar(titulo)
            for indice in range(inicio_cuerpo, len(paginas)):
                lineas = paginas[indice].splitlines()
                for linea in lineas:
                    if normalizar(linea) == objetivo:
                        return indice - inicio_cuerpo + 1
                for linea in lineas:
                    if normalizar(linea).startswith(objetivo):
                        return indice - inicio_cuerpo + 1
            return None

        doc = Document(SALIDA)
        estilos = {
            "TOC 1", "TOC 2", "TOC 3",
            "toc 1", "toc 2", "toc 3",
        }
        cambios = 0
        for p in doc.paragraphs:
            if p.style.name not in estilos or "\t" not in p.text:
                continue
            titulo = p.text.split("\t")[0].strip()
            titulo = re.sub(r"\.{2,}\s*\d+\s*$", "", titulo).strip()
            nueva = pagina_de(titulo)
            if nueva is None:
                continue
            for run in reversed([r for r in p.runs if r.text.strip()]):
                if re.fullmatch(r"\d+", run.text.strip()):
                    if run.text.strip() != str(nueva):
                        run.text = str(nueva)
                        cambios += 1
                    break
        if cambios:
            doc.save(SALIDA)
        print(f"Índice actualizado: {cambios} entradas.")


def main():
    if not os.path.exists(BASE_DOCX):
        raise SystemExit("No se encontró el informe base: " + BASE_DOCX)
    raw = extraer_markdown()
    titulo, nombres, docente = datos_portada(raw)
    cuerpo = transformar_cuerpo(raw)

    with open(MD, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("lang: es\n")
        f.write("---\n\n")
        f.write(portada_md(titulo, nombres, docente))
        f.write("\n")
        f.write(cuerpo)

    crear_referencia()
    ejecutar([
        "pandoc", MD, "-o", SALIDA,
        "--reference-doc", REF,
        "--from", "markdown",
        "--standalone",
    ])
    postprocesar()
    actualizar_indice_desde_pdf()
    print(SALIDA)


if __name__ == "__main__":
    main()
