#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe de proyecto de Sistemas de Control a partir del contenido
de 1_Embebidos.txt y la estructura del modelo de informe de la asignatura.
Usa la biblioteca de estilos base_documento.py.
"""

import os
import sys

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.shared import Cm, Pt, RGBColor

SKILLS_DIR = "/home/eynor/Documents/2_Proyect_Private/0_biblioteca-Skills/skills"
sys.path.insert(0, SKILLS_DIR)

from base_documento import (  # noqa: E402
    crear_documento,
    configurar_estilos,
    add_paragraph,
    add_heading_custom,
    add_bullets,
    add_table_with_data,
    configurar_header,
    configurar_primer_header_vacio,
    agregar_toc,
    agregar_nueva_seccion,
)

SALIDA = "/home/eynor/Documents/5_Class/sistemas-control/1_Proyecto"
NOMBRE = "Informe_Proyecto_Sistemas_de_Control_ESP32-C3.docx"
LOGO = "/home/eynor/Documents/2_Proyect_Private/0_biblioteca-Skills/logoUnifranz/logounifranz.png"

AUTORES = (
    "Breydy Ronald Choque Huanca\n"
    "Tony Isrrael Mamani Gallegos\n"
    "Rolando Quispe Llojlla"
)
DOCENTE = "Ing. José Francisco Aranibar Ortiz"
TITULO = (
    "SISTEMA PORTÁTIL DE MONITOREO DE SIGNOS VITALES BASADO EN ESP32-C3 "
    "PARA SUPERVISIÓN REMOTA DE PERSONAS MAYORES O ENFERMOS CARDÍACOS"
)


# ---------------------------------------------------------------------------
# Utilidades de formato
# ---------------------------------------------------------------------------
def configurar_heading1(doc):
    h1 = doc.styles["Heading 1"]
    h1.font.name = "Arial"
    h1.font.size = Pt(14)
    h1.font.bold = True
    h1.font.italic = False
    h1.font.color.rgb = RGBColor(0, 0, 0)
    pf = h1.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(18)
    pf.space_after = Pt(8)
    pf.first_line_indent = Cm(0)
    pf.keep_with_next = True

    h3 = doc.styles["Heading 3"]
    h3.paragraph_format.first_line_indent = Cm(0)


def h1(doc, texto):
    p = doc.add_heading(texto, level=1)
    for run in p.runs:
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.first_line_indent = Cm(0)
    return p


def h2(doc, texto):
    return add_heading_custom(doc, texto, level=2)


def h3(doc, texto):
    return add_heading_custom(doc, texto, level=3)


def p(doc, texto, **kwargs):
    return add_paragraph(doc, texto, **kwargs)


def p_centrado(doc, texto, negrita=False, cursiva=True, size=12):
    return add_paragraph(
        doc,
        texto,
        bold=negrita,
        italic=cursiva,
        size=size,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        first_line_indent=0,
        space_before=4,
        space_after=4,
    )


def salto(doc):
    doc.add_page_break()


def pendiente(doc, texto, comentario):
    """Párrafo visible + comentario real de Word anclado."""
    par = doc.add_paragraph()
    run = par.add_run("PENDIENTE — " + texto)
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x5A, 0x45, 0x00)
    run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    par.paragraph_format.first_line_indent = Cm(0)
    par.paragraph_format.line_spacing = 1.15
    par.paragraph_format.space_before = Pt(8)
    par.paragraph_format.space_after = Pt(4)
    doc.add_comment(runs=run, text=comentario, author="Equipo", initials="EQ")
    return par


def caja_espacio(doc, etiqueta, alto_cm=6.0):
    """Recuadro con borde punteado para pegar figuras o capturas."""
    tabla = doc.add_table(rows=1, cols=1)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    fila = tabla.rows[0]
    celda = fila.cells[0]
    celda.width = Cm(15.5)

    trPr = fila._tr.get_or_add_trPr()
    alto = OxmlElement("w:trHeight")
    alto.set(qn("w:val"), str(int(alto_cm * 567)))
    alto.set(qn("w:hRule"), "atLeast")
    trPr.append(alto)

    celda.text = ""
    par = celda.paragraphs[0]
    run = par.add_run(etiqueta)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.first_line_indent = Cm(0)
    par.paragraph_format.line_spacing = 1.0

    tcPr = celda._tc.get_or_add_tcPr()
    bordes = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        '<w:top w:val="dashed" w:sz="6" w:space="0" w:color="999999"/>'
        '<w:left w:val="dashed" w:sz="6" w:space="0" w:color="999999"/>'
        '<w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="999999"/>'
        '<w:right w:val="dashed" w:sz="6" w:space="0" w:color="999999"/>'
        "</w:tcBorders>"
    )
    tcPr.append(bordes)
    return tabla


def espacio(doc):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(0)
    par.paragraph_format.space_after = Pt(0)
    par.paragraph_format.line_spacing = 1.0
    return par


def anchos(tabla, lista_cm):
    tabla.autofit = False
    for i, ancho in enumerate(lista_cm):
        tabla.columns[i].width = Cm(ancho)
    for fila in tabla.rows:
        for i, ancho in enumerate(lista_cm):
            fila.cells[i].width = Cm(ancho)
    return tabla


# ---------------------------------------------------------------------------
# Portada
# ---------------------------------------------------------------------------
def portada(doc):
    for _ in range(2):
        doc.add_paragraph()

    add_paragraph(doc, "UNIVERSIDAD PRIVADA FRANZ TAMAYO", bold=True, size=14,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
    add_paragraph(doc, "FACULTAD DE INGENIERÍA", bold=True, size=13,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
    add_paragraph(doc, "CARRERA DE INGENIERÍA DE SISTEMAS", bold=True, size=13,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_after=8)
    add_paragraph(doc, "ASIGNATURA: SISTEMAS DE CONTROL", bold=True, size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)
    add_paragraph(doc, "PROYECTO DE INVESTIGACIÓN", bold=True, size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_after=12)

    if os.path.exists(LOGO):
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.first_line_indent = Cm(0)
        run = par.add_run()
        run.add_picture(LOGO, width=Cm(5.0), height=Cm(4.75))
        par.paragraph_format.space_after = Pt(14)

    add_paragraph(doc, f"“{TITULO}”", bold=True, size=13,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_before=10, space_after=16)
    add_paragraph(doc, "ESTUDIANTES:", bold=True, size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_after=2)
    for nombre in AUTORES.split("\n"):
        add_paragraph(doc, nombre, size=12, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                      first_line_indent=0)
    add_paragraph(doc, "DOCENTE:", bold=True, size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_before=10, space_after=2)
    add_paragraph(doc, DOCENTE, size=12, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                  first_line_indent=0)
    add_paragraph(doc, "EL ALTO – BOLIVIA", bold=True, size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_before=14, space_after=0)
    add_paragraph(doc, "2025", bold=True, size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)


# ---------------------------------------------------------------------------
# Contenido
# ---------------------------------------------------------------------------
def resumen(doc):
    h1(doc, "RESUMEN")
    p(doc,
      "El monitoreo continuo de signos vitales en adultos mayores y pacientes con "
      "enfermedades cardíacas suele depender de equipos clínicos costosos y poco "
      "portátiles. En Bolivia, muchas familias no tienen forma de mantener una "
      "supervisión permanente cuando el paciente vuelve a casa. Este proyecto "
      "desarrolla un dispositivo portátil basado en el microcontrolador ESP32-C3 que "
      "mide frecuencia cardíaca, saturación de oxígeno (SpO2), temperatura corporal y "
      "movimiento mediante los sensores MAX30102, MAX30205 y MPU6050, conectados por "
      "un bus I2C compartido. El ESP32-C3 procesa las lecturas, las muestra en una "
      "pantalla OLED y las transmite por WiFi o Bluetooth hacia una plataforma externa. "
      "Cuando un valor sale del rango configurado, se activa un motor vibrador mediante "
      "un MOSFET y se genera una alerta. La alimentación usa una batería LiPo de 3.7 V "
      "con módulo TP4056 y regulador LDO de 3.3 V.")
    p(doc,
      "El trabajo se centra en el diseño del lazo de control que decide cuándo alertar, "
      "en el modelado del sistema y en la simulación en MATLAB/Simulink, que el equipo "
      "se encuentra desarrollando. Se espera obtener un prototipo funcional que permita "
      "la supervisión remota y la detección temprana de eventos críticos, sin reemplazar "
      "equipos médicos certificados.")
    p(doc,
      "Palabras clave: ESP32-C3, signos vitales, IoT, control por umbrales, Simulink.",
      italic=True)


def introduccion(doc):
    h1(doc, "1. INTRODUCCIÓN")
    p(doc,
      "El envejecimiento de la población y el aumento de las enfermedades cardíacas "
      "convirtieron la supervisión de signos vitales en una tarea diaria para muchas "
      "familias. En el sistema público de salud boliviano, la mayor parte de los "
      "controles se realiza en hospitales o consultorios, con equipos que no salen de "
      "la sala. Cuando el paciente vuelve a su casa, la vigilancia desaparece.")
    p(doc,
      "Ese vacío tiene consecuencias. Una arritmia, una caída o una baja de la "
      "saturación de oxígeno pueden pasar inadvertidas durante horas. La atención llega "
      "tarde, cuando el evento ya ocurrió. No se trata de un problema teórico: es la "
      "diferencia entre una alerta a tiempo y una complicación que pudo evitarse.")
    p(doc,
      "El proyecto parte de una idea sencilla. Usar componentes de bajo costo y un "
      "microcontrolador con conectividad para construir un dispositivo portátil que no "
      "reemplace al médico, pero que avise cuando algo no está bien. El ESP32-C3 lee "
      "cuatro señales, las procesa, las muestra y las envía. Si un valor se sale del "
      "rango, activa una alerta.")
    p(doc,
      "Este informe está organizado en quince secciones. Las primeras describen el "
      "problema, los objetivos y la justificación. Después se presenta el marco teórico, "
      "el modelado del sistema y el diseño del controlador. Las secciones de simulación "
      "y análisis de resultados quedan preparadas para incorporar el trabajo que el "
      "equipo realizará en MATLAB/Simulink.")
    p(doc,
      "Una aclaración importante. El documento describe el diseño del sistema y el lazo "
      "de control que decide cuándo alertar. No inventamos mediciones ni resultados de "
      "simulación. Esas partes están marcadas de forma visible para que puedan "
      "completarse con las capturas y los datos reales del equipo.")

    h2(doc, "1.1 Antecedentes")
    p(doc,
      "A nivel internacional, los dispositivos portátiles para monitoreo de signos "
      "vitales crecieron junto con el Internet de las Cosas y los sistemas embebidos. "
      "Los antecedentes se parecen en una cosa: casi todos miden, pero pocos integran "
      "varios sensores, alertan y permiten supervisión remota en un mismo equipo.")
    p(doc,
      "Fuentes (2022) propuso un sistema IoT para el monitoreo remoto de saturación de "
      "oxígeno, frecuencia cardíaca y temperatura corporal. El trabajo integra sensores "
      "biomédicos con módulos inalámbricos y transmite los datos a plataformas externas. "
      "La limitación es que el prototipo se apoya en una conexión permanente y no "
      "contempla el consumo de energía de un dispositivo que debe llevarse puesto.")
    p(doc,
      "Arcos Coronel y Quezada Patiño (2023) desarrollaron un sistema wearable para "
      "medir frecuencia cardíaca y variables físicas en futbolistas. El estudio muestra "
      "que los equipos comerciales son costosos y que existe espacio para soluciones "
      "accesibles. Su enfoque, sin embargo, está pensado para sesiones de entrenamiento "
      "y no para el seguimiento domiciliario de un paciente crónico.")
    p(doc,
      "Badillo, Morales Martínez, Acuña Galván y Lezama León (2023) construyeron un "
      "prototipo para el registro de signos vitales en el servicio médico de la Escuela "
      "Superior de Tizayuca. El sistema reduce el tiempo de valoración y guarda un "
      "historial clínico. Es un buen ejemplo de integración, aunque depende de una "
      "infraestructura institucional y de una base de datos centralizada.")
    p(doc,
      "En Bolivia, los antecedentes son más dispersos. Apaza Mamani (2023) diseñó una "
      "central de monitoreo para unidades de terapia intensiva. El trabajo detecta un "
      "problema real: la falta de personal especializado obliga a los pocos intensivistas "
      "a repartirse entre varias camas y tareas. Una central de monitoreo ayuda, pero "
      "sigue atada a un entorno hospitalario.")
    p(doc,
      "Botello Cardozo (2022) desarrolló un dispositivo de bajo costo para personas que "
      "sufrieron infartos, con registro y alertas a través de una página web. El proyecto "
      "se acerca bastante a nuestra propuesta. La diferencia es que aquí se busca un "
      "equipo autónomo, con pantalla local, alerta por vibración y comunicación "
      "inalámbrica directa.")
    p(doc,
      "Ninguno de los trabajos revisados resuelve el problema completo en el contexto "
      "local. Unos apuntan a hospitales, otros a deportistas, otros a un solo parámetro. "
      "Ese es el espacio que ocupa este proyecto.")


def planteamiento(doc):
    h1(doc, "2. PLANTEAMIENTO DEL PROBLEMA")
    h2(doc, "2.1 Descripción del sistema")
    p(doc,
      "El sistema es un dispositivo portátil formado por varios módulos. El módulo "
      "principal es el ESP32-C3 SuperMini, que lee los sensores, procesa los datos, "
      "controla la pantalla y gestiona la comunicación inalámbrica. Los sensores "
      "biomédicos se conectan a un bus I2C compartido: el MAX30102 mide frecuencia "
      "cardíaca y SpO2, el MAX30205 mide temperatura corporal y el MPU6050 detecta "
      "movimiento y posibles caídas.")
    p(doc,
      "La interfaz local es una pantalla OLED SSD1306 de 0.66 pulgadas. No es una "
      "pantalla cómoda para mostrar cuatro variables a la vez, así que el diseño la "
      "organiza por páginas. El usuario avanza con un botón táctil. La alerta física es "
      "un motor vibrador controlado por un MOSFET, porque la corriente que entrega una "
      "GPIO del ESP32-C3 no alcanza para mover el motor directamente.")
    p(doc,
      "La alimentación viene de una batería LiPo de 3.7 V, un módulo de carga TP4056 y "
      "un regulador LDO de 3.3 V. El ESP32-C3 y los sensores trabajan a 3.3 V. La "
      "comunicación remota se hace por WiFi o Bluetooth hacia una plataforma externa.")
    p(doc,
      "El sistema puede sujetarse con una correa o un clip. No es un equipo médico "
      "certificado ni pretende serlo. Es un prototipo académico de supervisión.")

    h2(doc, "2.2 Problema específico")
    p(doc,
      "En Bolivia, el control de signos vitales en personas mayores y pacientes con "
      "enfermedades cardíacas depende casi siempre de un entorno clínico. Los equipos "
      "hospitalarios son costosos, pesados y requieren personal capacitado. Fuera del "
      "hospital, la supervisión continua se vuelve difícil. El paciente queda al cuidado "
      "de familiares que no tienen formación médica y que no pueden estar despiertos "
      "las 24 horas.")
    p(doc,
      "Existen dispositivos comerciales portátiles, pero funcionan de forma aislada. "
      "Miden un parámetro, muestran un número y listo. No integran varios sensores en un "
      "solo sistema, no procesan los datos en tiempo real y, en muchos casos, no generan "
      "alertas ni permiten que un familiar consulte el estado del paciente a distancia.")
    p(doc,
      "El problema específico es la falta de una solución accesible que integre "
      "adquisición de datos, procesamiento, visualización, alerta local y comunicación "
      "remota en un único dispositivo de bajo consumo. Sin esa integración, eventos "
      "como caídas, arritmias o episodios de hipoxia siguen pasando desapercibidos.")
    p(doc,
      "También hay un problema de diseño de control. ¿Cuándo debe sonar una alerta? Si "
      "el umbral es demasiado sensible, el dispositivo vibra por cualquier variación y "
      "el usuario lo apaga. Si es demasiado permisivo, la alerta llega tarde. Ese "
      "equilibrio es parte central de este proyecto.")

    h2(doc, "2.3 Pregunta de investigación")
    p(doc,
      "¿Cómo diseñar e implementar un sistema portátil basado en el microcontrolador "
      "ESP32-C3 que permita el monitoreo en tiempo real de signos vitales, integrando "
      "múltiples sensores biomédicos, con bajo consumo energético y capacidad de generar "
      "alertas y comunicación remota para la supervisión de personas mayores o pacientes "
      "con enfermedades cardíacas?")


def objetivos(doc):
    h1(doc, "3. OBJETIVOS")
    h2(doc, "3.1 Objetivo general")
    p(doc,
      "Desarrollar un sistema portátil de monitoreo de signos vitales basado en el "
      "microcontrolador ESP32-C3 para la supervisión remota de personas mayores o "
      "pacientes con enfermedades cardíacas.")
    h2(doc, "3.2 Objetivos específicos")
    add_bullets(doc, [
      "Analizar los requerimientos del sistema para el monitoreo de signos vitales en "
      "personas mayores o pacientes con enfermedades cardíacas.",
      "Diseñar la arquitectura del sistema portátil integrando el microcontrolador "
      "ESP32-C3 con sensores biomédicos mediante comunicación I2C.",
      "Desarrollar el sistema de adquisición y procesamiento de datos para la medición "
      "de frecuencia cardíaca, SpO2, temperatura corporal y movimiento.",
      "Implementar la visualización de datos en una pantalla OLED y la comunicación "
      "inalámbrica mediante WiFi o Bluetooth.",
      "Diseñar el lazo de control supervisor que decide la activación de la alerta por "
      "vibración y su histéresis.",
      "Modelar el sistema y simular el comportamiento del lazo de control en "
      "MATLAB/Simulink.",
      "Validar el funcionamiento del sistema mediante pruebas de medición, detección de "
      "eventos críticos y consumo energético.",
    ])


def justificacion(doc):
    h1(doc, "4. JUSTIFICACIÓN")
    h2(doc, "4.1 Justificación económica")
    p(doc,
      "Un monitor de signos vitales comercial puede costar miles de bolivianos. El "
      "conjunto de componentes de este proyecto —ESP32-C3, MAX30102, MAX30205, MPU6050, "
      "OLED, módulo de carga y batería— cuesta una fracción de ese valor y se consigue "
      "en el mercado local. Para una familia con un paciente crónico, esa diferencia "
      "es la que decide si el equipo se compra o no.")
    p(doc,
      "No se trata solo del precio inicial. Un equipo abierto y con componentes "
      "comerciales se puede reparar o reemplazar por partes. Si se quema el sensor de "
      "oxígeno, se cambia el MAX30102. Si falla el regulador, se cambia el LDO. En un "
      "equipo cerrado, cualquiera de esas fallas obliga a reemplazar todo.")

    h2(doc, "4.2 Justificación social")
    p(doc,
      "El proyecto apunta a un grupo vulnerable. Las personas mayores y los pacientes "
      "con enfermedades cardíacas necesitan supervisión constante, pero no siempre "
      "tienen acceso a un cuidador permanente. La posibilidad de que un familiar reciba "
      "una alerta en el teléfono cambia la dinámica del cuidado.")
    p(doc,
      "También reduce la carga sobre el sistema de salud. Si una complicación se detecta "
      "en casa, la consulta llega antes de que se convierta en una emergencia. No "
      "sustituye al médico. Le da información oportuna.")

    h2(doc, "4.3 Justificación técnica")
    p(doc,
      "El proyecto integra sistemas embebidos, sensores biomédicos, comunicación "
      "inalámbrica y teoría de control en un solo producto. El ESP32-C3 procesa los "
      "datos en tiempo real, el bus I2C permite conectar varios sensores con dos líneas "
      "y el diseño de alimentación obliga a cuidar el consumo. Cada decisión técnica "
      "tiene una consecuencia medible.")
    p(doc,
      "En la parte de control, el reto es convertir cuatro señales ruidosas en una "
      "decisión confiable: alertar o no alertar. Eso exige umbrales, histéresis, "
      "filtrado y una lógica que no se dispare con cualquier movimiento.")

    h2(doc, "4.4 Justificación académica")
    p(doc,
      "El trabajo conecta varias asignaturas de la carrera. La programación aparece en "
      "el firmware, la electrónica en el diseño de alimentación y acondicionamiento, las "
      "redes en la comunicación inalámbrica y los sistemas de control en el modelado y "
      "la simulación del lazo. Es un proyecto que obliga a integrar, no solo a aprobar "
      "una materia.")
    p(doc,
      "Para el equipo, el aprendizaje más valioso está en el modelado. Pasar de un "
      "diagrama de bloques a una función de transferencia y de ahí a una simulación "
      "obliga a entender qué se está controlando y qué se está suponiendo.")

    h2(doc, "4.5 Justificación ambiental")
    p(doc,
      "El dispositivo usa una batería recargable en lugar de pilas desechables. El "
      "consumo se puede reducir con modos de bajo consumo y con un diseño de firmware "
      "que no mantenga el WiFi encendido todo el tiempo. Es una contribución pequeña, "
      "pero evita la generación de residuos electrónicos asociada a equipos de un solo "
      "uso.")
    p(doc,
      "No se realizó un análisis de ciclo de vida completo. Sería exagerado afirmar que "
      "el proyecto es ambientalmente neutro. Lo que sí se puede decir es que la "
      "selección de componentes y el modo de operación apuntan a un uso más duradero.")


def alcances(doc):
    h1(doc, "5. ALCANCES Y LIMITACIONES")
    h2(doc, "5.1 Alcances")
    p(doc,
      "El proyecto contempla el diseño e implementación de un dispositivo portátil de "
      "monitoreo de signos vitales basado en el ESP32-C3, con adquisición, procesamiento "
      "y transmisión de datos biomédicos.")
    p(doc,
      "El sistema incluye un módulo de procesamiento principal, un módulo de sensores "
      "biomédicos con bus I2C compartido, una pantalla OLED de 0.66 pulgadas, un motor "
      "vibrador con MOSFET para la alerta, y un módulo de energía con batería LiPo de "
      "3.7 V, cargador TP4056 y regulador LDO de 3.3 V.")
    p(doc,
      "En el plano de control, el alcance incluye el diseño del lazo supervisor, la "
      "definición de umbrales e histéresis, y la simulación del comportamiento en "
      "MATLAB/Simulink. La simulación será realizada por el equipo y sus resultados se "
      "incorporarán a este informe.")
    p(doc,
      "También se contempla la transmisión de datos hacia una plataforma externa para "
      "la supervisión remota y la validación del prototipo mediante pruebas de medición, "
      "detección de eventos y consumo energético.")

    h2(doc, "5.2 Limitaciones")
    add_bullets(doc, [
      "El sistema no cuenta con certificación médica, por lo que no sustituye equipos "
      "clínicos profesionales.",
      "La autonomía está limitada por la capacidad de la batería LiPo utilizada.",
      "La transmisión de datos depende de la disponibilidad de conexión inalámbrica "
      "(WiFi o Bluetooth).",
      "No se contempla el desarrollo de una aplicación médica certificada, sino una "
      "plataforma básica de monitoreo.",
      "Las interferencias eléctricas y el movimiento del usuario pueden afectar la "
      "calidad de las mediciones.",
      "La validación clínica con pacientes reales queda fuera del alcance académico.",
      "Las simulaciones en MATLAB/Simulink están pendientes de ejecución y no se "
      "presentan resultados definitivos en esta versión del informe.",
    ])


def marco_teorico(doc):
    h1(doc, "6. MARCO TEÓRICO")

    h2(doc, "6.1 Sistemas dinámicos y modelado matemático")
    p(doc,
      "Un sistema dinámico es un conjunto de variables que evolucionan en el tiempo y "
      "que se relacionan entre sí mediante reglas físicas o lógicas. En control, se "
      "distinguen las entradas, las salidas y el estado interno. Modelar es escribir esa "
      "relación en forma matemática para poder predecir el comportamiento antes de "
      "construir el sistema.")
    p(doc,
      "En este proyecto, el modelo no describe la fisiología del paciente. Describe la "
      "cadena de supervisión: cómo llega la señal del sensor, cómo se procesa y cómo se "
      "decide una alerta. Esa distinción es importante para no prometer algo que el "
      "dispositivo no hace.")

    h2(doc, "6.2 Función de transferencia")
    p(doc,
      "La función de transferencia relaciona la salida con la entrada de un sistema "
      "lineal e invariante en el tiempo, en el dominio de Laplace. Se define como "
      "G(s) = Y(s)/U(s), con condiciones iniciales nulas. Sus polos determinan la "
      "estabilidad y su forma permite identificar si el sistema es de primer orden, de "
      "segundo orden o de orden superior.")
    p(doc,
      "Para un sensor térmico de primer orden, un modelo habitual es G(s) = K/(τs + 1), "
      "donde K es la ganancia estática y τ la constante de tiempo. No son valores "
      "universales: dependen del sensor, del contacto con la piel y del entorno. "
      "Cualquier valor que se use en la simulación debe justificarse con datos o con la "
      "hoja de datos.")

    h2(doc, "6.3 Estabilidad")
    p(doc,
      "Un sistema continuo es estable si todos los polos de su función de transferencia "
      "tienen parte real negativa. En un sistema discreto, la condición equivalente es "
      "que los polos estén dentro del círculo unitario. La estabilidad no lo es todo: un "
      "sistema puede ser estable y aun así responder demasiado lento o oscilar antes de "
      "estabilizarse.")
    p(doc,
      "En un lazo supervisor como el de este proyecto, la estabilidad también se traduce "
      "en algo práctico: que la alerta no se active y desactive sin control. La "
      "histéresis existe justamente para evitar ese comportamiento.")

    h2(doc, "6.4 Controladores P, PI, PID y control on/off")
    p(doc,
      "El controlador proporcional (P) actúa en función del error actual. El integral "
      "(I) acumula el error y elimina el error en estado estacionario. El derivativo (D) "
      "reacciona a la velocidad de cambio y puede anticipar la respuesta, aunque amplifica "
      "el ruido. El PID combina los tres términos y es el controlador más usado en la "
      "industria.")
    p_centrado(doc, "u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt")
    p(doc,
      "El control on/off es más simple: actúa cuando la variable cruza un umbral y se "
      "apaga cuando vuelve al rango. Su ventaja es la simplicidad; su desventaja es el "
      "ciclo de encendido y apagado constante. La histéresis reduce ese problema "
      "introduciendo dos umbrales en lugar de uno.")
    p(doc,
      "Para este proyecto, el control on/off con histéresis es la opción natural para la "
      "alerta. El PID queda como alternativa para un canal de temperatura o para un "
      "actuador futuro.")

    h2(doc, "6.5 Respuesta temporal")
    p(doc,
      "La respuesta temporal describe cómo evoluciona la salida ante una entrada. En una "
      "respuesta al escalón se analizan el tiempo de subida, el sobreimpulso, el tiempo "
      "de establecimiento y el error en estado estacionario. Cada métrica responde a una "
      "pregunta distinta: qué tan rápido reacciona, cuánto se pasa, cuánto tarda en "
      "calmarse y qué tan cerca queda del valor deseado.")
    p(doc,
      "En un lazo de alerta, el tiempo de respuesta se mide en segundos, no en "
      "milisegundos. Al paciente no le sirve una alerta que llega después de diez "
      "minutos. Pero tampoco sirve una que se dispara con cada movimiento. El análisis "
      "tiene que equilibrar ambas cosas.")

    h2(doc, "6.6 Dispositivo portátil")
    p(doc,
      "Un sistema portátil es un conjunto de componentes tecnológicos que puede "
      "transportarse y usarse sin una instalación fija. Tanenbaum y Wetherall (2011) "
      "señalan que los sistemas computacionales evolucionaron hacia modelos móviles, "
      "donde la portabilidad es una condición de accesibilidad. Stallings (2015) agrega "
      "que estos dispositivos integran hardware compacto, software optimizado y "
      "conectividad inalámbrica.")
    p(doc,
      "La portabilidad no es solo tamaño. También es consumo, peso y autonomía. Un equipo "
      "que dura dos horas con batería no sirve para monitorear a un paciente durante la "
      "noche.")

    h2(doc, "6.7 Monitoreo")
    p(doc,
      "El monitoreo es el proceso de observar, registrar y evaluar variables de forma "
      "continua. Laudon y Laudon (2016) lo describen como un mecanismo de control "
      "organizacional que permite detectar fallas antes de que afecten el proceso. En "
      "sistemas informáticos, Stallings (2015) lo relaciona con la recolección y el "
      "análisis de datos de hardware, software y red.")
    p(doc,
      "En salud, el monitoreo tiene una función preventiva, correctiva y predictiva. "
      "Preventiva cuando detecta un riesgo, correctiva cuando permite actuar y "
      "predictiva cuando anticipa una tendencia. Este proyecto apunta a las dos primeras.")

    h2(doc, "6.8 Signos vitales")
    p(doc,
      "Los signos vitales son indicadores fisiológicos que permiten evaluar el estado "
      "general de una persona. Los más conocidos son la temperatura corporal, la "
      "frecuencia cardíaca, la frecuencia respiratoria y la presión arterial. Hall (2016) "
      "explica que estos parámetros se regulan mediante procesos de homeostasis, y "
      "Tortora y Derrickson (2017) los presentan como herramienta clínica de valoración "
      "inicial.")
    p(doc,
      "Bickley (2017) insiste en que el control periódico no es exclusivo del hospital. "
      "También sirve en programas de seguimiento domiciliario, sobre todo en pacientes "
      "crónicos. La detección temprana de una alteración permite intervenir antes de que "
      "el cuadro se complique.")

    h2(doc, "6.9 Sensores biomédicos")
    p(doc,
      "Un sensor biomédico es un transductor que convierte una variable fisiológica en "
      "una señal eléctrica procesable. Webster (2009) lo define como el elemento que "
      "transforma una señal biológica en una señal cuantificable. Enderle y Bronzino "
      "(2012) los consideran componentes centrales de la instrumentación médica y los "
      "clasifican en invasivos y no invasivos.")
    p(doc,
      "Carr y Brown (2001) recuerdan que el diseño debe considerar biocompatibilidad, "
      "sensibilidad, estabilidad y seguridad. En este proyecto todos los sensores son no "
      "invasivos: el MAX30102 usa luz, el MAX30205 mide temperatura por contacto y el "
      "MPU6050 mide aceleración.")
    p(doc,
      "El MAX30102 se comunica por I2C en la dirección 0x57. El MAX30205 suele responder "
      "en 0x48 o 0x49, según la configuración. El MPU6050 usa 0x68 o 0x69. La pantalla "
      "SSD1306, en la mayoría de los módulos, responde en 0x3C. Con tres dispositivos en "
      "el mismo bus, revisar las direcciones antes de conectar evita más de un dolor de "
      "cabeza.")

    h2(doc, "6.10 Comunicación I2C")
    p(doc,
      "I2C es un protocolo serial síncrono que usa dos líneas: SDA para datos y SCL para "
      "reloj. Axelson (2015) describe su arquitectura maestro-esclavo, donde el maestro "
      "genera el reloj y coordina la transferencia. Barrett y Pack (2012) destacan que "
      "cada esclavo tiene una dirección única, lo que permite conectar varios "
      "dispositivos con solo dos pines.")
    p(doc,
      "Monk (2013) señala que el bus admite modos estándar y rápido, y que incorpora "
      "confirmaciones ACK/NACK para verificar la recepción. En la práctica, el bus "
      "necesita resistencias de pull-up y cierta tolerancia al ruido. Un cable largo o "
      "un mal contacto puede hacer que el ESP32-C3 no encuentre al sensor.")

    h2(doc, "6.11 IoT aplicado a la salud")
    p(doc,
      "El Internet de las Cosas aplicado a la salud conecta dispositivos, sensores y "
      "sistemas informáticos para recopilar y analizar datos clínicos. Gubbi, Buyya, "
      "Marusic y Palaniswami (2013) lo describen como una infraestructura global de "
      "objetos conectados. Islam, Kwak, Kabir, Hossain y Kwak (2015) muestran su impacto "
      "en el monitoreo remoto y en la detección temprana de anomalías.")
    p(doc,
      "Atzori, Iera y Morabito (2010) dividen la arquitectura en dispositivos "
      "inteligentes, infraestructura de red y sistemas de procesamiento. La salud digital "
      "usa esa estructura para telemedicina, hospitales inteligentes y alertas "
      "automatizadas. Este proyecto ocupa la primera capa: el dispositivo que adquiere y "
      "transmite los datos.")


def modelado(doc):
    h1(doc, "7. MODELADO DEL SISTEMA")
    h2(doc, "7.1 Descripción del modelo")
    p(doc,
      "Antes de escribir ecuaciones hay que aclarar qué se está modelando. El sistema no "
      "controla la fisiología del paciente. Sería irresponsable afirmarlo. Lo que "
      "controla es la cadena de supervisión: sensores, adquisición, decisión y alerta. "
      "La planta, en sentido estricto, es el conjunto sensor-adquisición, y la variable "
      "controlada es el estado de la alarma.")
    p(doc,
      "Las entradas son la frecuencia cardíaca, la SpO2, la temperatura corporal y la "
      "aceleración. Las salidas son la alerta por vibración, la información en pantalla "
      "y el paquete de datos que se transmite. El ESP32-C3 actúa como controlador "
      "discreto: muestrea, compara con umbrales y decide.")
    t = add_table_with_data(
        doc,
        ["Variable", "Tipo", "Descripción", "Frecuencia"],
        [
            ["Frecuencia cardíaca", "Entrada", "Pulsos por minuto obtenidos del PPG", "50 Hz"],
            ["SpO2", "Entrada", "Saturación de oxígeno estimada", "50 Hz"],
            ["Temperatura", "Entrada", "Temperatura corporal por contacto", "1 Hz"],
            ["Aceleración", "Entrada", "Aceleración en tres ejes", "50 Hz"],
            ["Alerta", "Salida", "Activación del motor vibrador", "1 Hz"],
            ["Pantalla", "Salida", "Visualización local", "1 Hz"],
            ["Datos remotos", "Salida", "Paquete WiFi o Bluetooth", "Eventual"],
        ],
        title="Tabla 1. Variables de entrada y salida del sistema.",
        note="La lógica de decisión se ejecuta a 1 Hz; los sensores pueden muestrear más rápido.",
    )
    anchos(t, [3.6, 2.2, 7.4, 2.3])
    p(doc, "Supuestos del modelo:")
    add_bullets(doc, [
      "El paciente se encuentra en reposo o en actividad leve durante la medición.",
      "El bus I2C trabaja a 400 kHz y los sensores tienen direcciones fijas.",
      "La temperatura se mide por contacto directo con la piel.",
      "El movimiento produce ruido en la señal PPG y debe filtrarse.",
      "La batería entrega 3.7 V y el regulador mantiene 3.3 V mientras haya carga.",
      "No se modela la fisiología del paciente; se usan rangos clínicos de referencia.",
    ])

    h2(doc, "7.2 Ecuaciones del sistema")
    p(doc,
      "La lógica básica del lazo supervisor se puede escribir en tiempo discreto. Sea "
      "r[k] el valor de referencia o umbral, y[k] la medición y e[k] el error:")
    p_centrado(doc, "e[k] = r[k] − y[k]")
    p(doc,
      "La salida de alerta u[k] se activa cuando el error supera un umbral positivo y se "
      "desactiva cuando cae por debajo de un umbral negativo. Entre ambos se mantiene el "
      "estado anterior. Esa es la histéresis:")
    p_centrado(doc, "u[k] = 1, si e[k] > +h")
    p_centrado(doc, "u[k] = 0, si e[k] < −h")
    p_centrado(doc, "u[k] = u[k−1], en otro caso")
    p(doc,
      "Como punto de partida para el canal de temperatura se propone un modelo de primer "
      "orden, habitual en sensores térmicos:")
    p_centrado(doc, "G(s) = K / (τs + 1)")
    p(doc,
      "Donde K es la ganancia estática y τ la constante de tiempo. Los valores concretos "
      "deben obtenerse de la hoja de datos del MAX30205 o de una prueba de respuesta. No "
      "se inventan aquí.")
    pendiente(
        doc,
        "completar las ecuaciones definitivas del modelo (planta, sensor y lazo de "
        "control) y justificar cada parámetro.",
        "Aquí va el desarrollo matemático completo: ecuaciones de la planta, "
        "linealización si corresponde, valores de K y τ, y las condiciones iniciales. "
        "El equipo debe reemplazar este bloque con el modelo final usado en Simulink.",
    )

    h2(doc, "7.3 Función de transferencia")
    p(doc,
      "La función de transferencia definitiva se obtendrá del modelo que se implemente "
      "en Simulink. Para el sensor térmico se parte de la forma de primer orden ya "
      "presentada. Para el lazo de alerta, en cambio, la función de transferencia no "
      "describe un actuador físico: describe la relación entre la señal de entrada y la "
      "decisión de alarma, que es discreta y no lineal.")
    p(doc,
      "Esa diferencia es importante. Un PID clásico se aplica a un lazo continuo. La "
      "alerta por umbrales se analiza mejor como un autómata de estados o como un "
      "sistema híbrido. En Simulink, la lógica se puede implementar con bloques de "
      "comparación, memoria y temporización, o con Stateflow.")
    pendiente(
        doc,
        "insertar la función de transferencia final y su deducción.",
        "Completar con la función de transferencia del modelo térmico o del canal que "
        "se decida controlar. Incluir numerador, denominador, polos, ceros y una breve "
        "interpretación física.",
    )

    h2(doc, "7.4 Diagrama de bloques")
    p(doc,
      "El diagrama de bloques debe mostrar la planta, el sensor, el controlador y la "
      "realimentación. En este caso, la realimentación es la lectura de los sensores y "
      "la salida es la alerta. El siguiente espacio está reservado para el diagrama "
      "definitivo.")
    pendiente(
        doc,
        "insertar el diagrama de bloques del sistema.",
        "Colocar aquí el diagrama de bloques (draw.io, Visio o Simulink) con las "
        "entradas, la planta, el controlador, las salidas y la realimentación. Debe "
        "coincidir con las ecuaciones de la sección 7.2.",
    )
    caja_espacio(doc, "[ Espacio para el diagrama de bloques ]", alto_cm=6.5)


def diseno_control(doc):
    h1(doc, "8. DISEÑO DEL SISTEMA DE CONTROL")
    h2(doc, "8.1 Tipo de controlador")
    p(doc,
      "El controlador es discreto y supervisor. No busca mantener la temperatura en un "
      "valor exacto ni regular la frecuencia cardíaca. Busca decidir si el estado del "
      "paciente es normal o crítico. Por eso el lazo principal es on/off con histéresis: "
      "simple, predecible y fácil de auditar.")
    p(doc,
      "La histéresis evita el encendido y apagado continuo. Si el umbral de frecuencia "
      "cardíaca alta es 120 bpm y no hay histéresis, basta con que la lectura oscile "
      "entre 119 y 121 para que el motor vibre sin parar. Con una banda de 5 bpm, la "
      "alerta se activa a 120 y no se apaga hasta bajar de 115.")
    p(doc,
      "Un PID queda como alternativa para el canal de temperatura o para un actuador "
      "futuro. En esta versión no se implementa en el firmware; se estudia en la "
      "simulación para comparar su comportamiento con el control on/off.")

    h2(doc, "8.2 Ecuación del controlador")
    p(doc,
      "La ley de control on/off con histéresis ya se presentó en la sección 7.2. La "
      "versión con PID, propuesta para el canal de temperatura, es la siguiente:")
    p_centrado(doc, "u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt")
    p(doc,
      "En tiempo discreto, con período de muestreo Δt, la forma implementable es:")
    p_centrado(doc, "u[k] = Kp·e[k] + Ki·Σe[j]·Δt + Kd·(e[k] − e[k−1])/Δt")
    p(doc,
      "El término integral acumula el error y elimina el offset. El derivativo reacciona "
      "al cambio, pero amplifica el ruido de la señal. En un sensor de temperatura "
      "lento, el derivativo aporta poco; en una señal PPG ruidosa, puede empeorar todo.")
    pendiente(
        doc,
        "definir los valores de Kp, Ki y Kd y la ecuación final implementada.",
        "Completar con los parámetros del controlador, el método de ajuste y la "
        "justificación. Si se usa solo on/off, indicarlo y eliminar la parte PID.",
    )

    h2(doc, "8.3 Ajuste de parámetros")
    p(doc,
      "El ajuste de los umbrales no es arbitrario. Se toman rangos clínicos de "
      "referencia para adultos en reposo y se deja un margen para evitar falsas alarmas. "
      "La tabla siguiente resume los valores propuestos para la primera versión.")
    t = add_table_with_data(
        doc,
        ["Parámetro", "Rango normal", "Umbral de alerta", "Histéresis"],
        [
            ["Frecuencia cardíaca", "50–120 bpm", "< 50 o > 120 bpm", "5 bpm"],
            ["SpO2", "≥ 92 %", "< 90 %", "2 %"],
            ["Temperatura", "36.0–37.5 °C", "< 35.5 o > 38.0 °C", "0.3 °C"],
            ["Aceleración", "≈ 1 g en reposo", "> 2.5 g (posible caída)", "Ventana de 2 s"],
        ],
        title="Tabla 2. Umbrales propuestos para el lazo de alerta.",
        note="Valores configurables. No constituyen un diagnóstico médico.",
    )
    anchos(t, [4.0, 3.3, 4.9, 3.3])
    p(doc,
      "El ajuste de los umbrales se puede hacer de forma manual, con prueba y error, o "
      "con Ziegler-Nichols si se opta por un PID. Ziegler-Nichols requiere llevar el "
      "sistema al límite de oscilación, algo que no se puede hacer con un paciente. Por "
      "eso, en este proyecto se aplicaría solo sobre el modelo simulado, nunca sobre una "
      "persona.")
    p(doc,
      "La puesta a punto real se hace con el prototipo: se compara la lectura del "
      "MAX30102 con un oxímetro comercial, la del MAX30205 con un termómetro clínico y "
      "la detección de caídas con pruebas controladas. Esa comparación es la que permite "
      "decidir si los umbrales elegidos tienen sentido.")
    pendiente(
        doc,
        "documentar el método de ajuste y los valores finales.",
        "Incluir aquí las pruebas de ajuste, los valores elegidos, las gráficas de "
        "respuesta y la comparación con equipos de referencia. Si se usa "
        "Ziegler-Nichols, indicar la tabla de sintonía y el punto crítico.",
    )


def simulacion(doc):
    h1(doc, "9. SIMULACIÓN DEL SISTEMA")
    h2(doc, "9.1 Herramientas utilizadas")
    p(doc,
      "La simulación se realizará en MATLAB/Simulink. El equipo eligió esta herramienta "
      "porque permite combinar bloques continuos, lógica discreta y visualización de "
      "señales en un mismo modelo. Además, la universidad cuenta con licencia para los "
      "laboratorios.")
    p(doc,
      "El modelo tendrá tres partes: una fuente de señal que representa las lecturas de "
      "los sensores, un bloque de control con los umbrales y la histéresis, y un scope "
      "para observar la respuesta. Para la parte térmica se usará una función de "
      "transferencia de primer orden. Para la lógica de alerta se pueden usar bloques "
      "de comparación y memoria, o Stateflow.")
    p(doc,
      "La versión de MATLAB/Simulink está pendiente de confirmar. Conviene anotarla en "
      "el informe final porque los resultados pueden variar ligeramente entre versiones.")

    h2(doc, "9.2 Escenarios de simulación")
    p(doc, "Se prevén los siguientes escenarios:")
    add_bullets(doc, [
      "Escalón en la frecuencia cardíaca: subida de 80 a 130 bpm para verificar la "
      "activación y desactivación de la alerta.",
      "Caída de SpO2: descenso gradual de 98 % a 88 % para evaluar el umbral y la "
      "histéresis.",
      "Cambio de temperatura: escalón de 36.5 °C a 38.5 °C para analizar el modelo "
      "térmico y, si se usa, el PID.",
      "Impulso de aceleración: simulación de una caída con un pico mayor a 2.5 g.",
      "Perturbación por ruido: señal PPG con ruido de movimiento para evaluar falsas "
      "alarmas.",
      "Caída de tensión de batería: descenso de 3.7 V a 3.3 V para observar el "
      "comportamiento del regulador.",
    ])

    h2(doc, "9.3 Resultados obtenidos")
    p(doc,
      "Esta sección se completará cuando el equipo ejecute las simulaciones. No se "
      "presentan resultados inventados. Los espacios siguientes están reservados para "
      "las capturas de Simulink y las gráficas de respuesta.")
    pendiente(
        doc,
        "insertar las gráficas y capturas de Simulink.",
        "El equipo debe agregar aquí: modelo en Simulink, respuesta al escalón, "
        "respuesta ante perturbaciones, tiempo de activación de la alerta y "
        "comparación on/off vs. PID. Incluir título, ejes y unidades en cada figura.",
    )
    caja_espacio(doc, "[ Figura 9.1 — Modelo del lazo de control en Simulink ]", alto_cm=6.0)
    espacio(doc)
    caja_espacio(doc, "[ Figura 9.2 — Respuesta temporal del sistema ]", alto_cm=6.0)


def analisis(doc):
    h1(doc, "10. ANÁLISIS DE RESULTADOS")
    p(doc,
      "El análisis se hará sobre las gráficas que produzca la simulación y sobre las "
      "pruebas del prototipo. No alcanza con mirar si la curva “se ve bien”. Hay que "
      "medir estabilidad, tiempo de establecimiento, sobreimpulso y error en estado "
      "estacionario. En un lazo de alerta, además, importa el tiempo que tarda en "
      "activarse y la cantidad de falsas alarmas.")
    p(doc,
      "También se comparará el sistema sin control —solo sensores y visualización— con "
      "el sistema con control —umbrales, histéresis y alerta—. Esa comparación es la que "
      "muestra si el lazo aporta algo o si solo agrega complejidad.")
    t = add_table_with_data(
        doc,
        ["Métrica", "Qué se evaluará"],
        [
            ["Estabilidad", "Que la salida no oscile de forma creciente."],
            ["Tiempo de establecimiento", "Cuánto tarda la señal en quedarse en el rango."],
            ["Sobreimpulso", "Cuánto se pasa del valor deseado."],
            ["Error en estado estacionario", "Diferencia final entre referencia y salida."],
            ["Tiempo de activación", "Segundos entre el evento y la alerta."],
            ["Falsas alarmas", "Activaciones sin evento real."],
            ["Consumo", "Corriente media del prototipo en operación."],
        ],
        title="Tabla 3. Métricas de evaluación.",
    )
    anchos(t, [5.4, 9.6])
    pendiente(
        doc,
        "escribir el análisis con los datos reales de simulación y prototipo.",
        "Reemplazar este bloque con la interpretación de las gráficas de la sección 9. "
        "Incluir comparación sin control vs. con control y comentar las limitaciones de "
        "los resultados.",
    )


def discusion(doc):
    h1(doc, "11. DISCUSIÓN")
    p(doc,
      "El diseño cumple los objetivos en la parte de arquitectura: los sensores están "
      "integrados, el bus I2C funciona con direcciones compatibles, la pantalla muestra "
      "las variables y la alerta tiene una lógica definida. La parte de simulación y "
      "validación sigue pendiente. Sería prematuro decir que el sistema “funciona” sin "
      "esas pruebas.")
    p(doc,
      "Hay limitaciones que no se resuelven solo con software. El MAX30205 necesita "
      "contacto con la piel; si se monta sobre la carcasa, mide la carcasa y no el "
      "cuerpo. El MAX30102 es sensible al movimiento y a la presión del dedo. El MPU6050 "
      "detecta una caída, pero también un golpe en la mesa. La calidad de la señal "
      "depende del diseño físico, no solo del código.")
    p(doc,
      "El consumo es otro punto crítico. El WiFi del ESP32-C3 tiene picos de corriente "
      "que pueden hacer parpadear el regulador si la batería está baja. Una estrategia "
      "razonable es mantener el WiFi apagado la mayor parte del tiempo y encenderlo solo "
      "para enviar datos o alertas. También conviene usar deep sleep entre lecturas.")
    p(doc,
      "En lo ético y legal, el dispositivo no es un equipo médico. No diagnostica ni "
      "trata. Cualquier uso real debería ir acompañado de una advertencia clara y de la "
      "supervisión de un profesional. La privacidad de los datos también importa: los "
      "signos vitales son datos sensibles y no deberían viajar sin cifrado.")
    p(doc,
      "¿Se pueden mejorar las cosas? Sí. Un filtro de mediana sobre la señal PPG, una "
      "calibración del SpO2 con un oxímetro de referencia y una detección de caídas que "
      "combine aceleración con orientación darían mejores resultados. También ayudaría "
      "guardar un historial local para revisar eventos pasados.")


def conclusiones(doc):
    h1(doc, "12. CONCLUSIONES")
    p(doc,
      "El proyecto permitió diseñar un dispositivo portátil que integra cuatro sensores "
      "biomédicos, una pantalla local, una alerta por vibración y comunicación "
      "inalámbrica sobre una base de bajo costo. La arquitectura queda definida y los "
      "módulos principales están seleccionados.")
    add_bullets(doc, [
      "Se definió la arquitectura del sistema y la distribución de los sensores en un "
      "bus I2C compartido.",
      "Se estableció una lógica de control supervisor con umbrales e histéresis para "
      "evitar alertas continuas.",
      "Se identificaron los puntos críticos del diseño: contacto del sensor de "
      "temperatura, ruido en la señal PPG y consumo del WiFi.",
      "Se dejó preparado el modelo para la simulación en MATLAB/Simulink, que el equipo "
      "completará con las gráficas y los parámetros definitivos.",
      "Se confirmó que el prototipo es una herramienta de apoyo y no un sustituto de "
      "equipos médicos certificados.",
    ])
    p(doc,
      "El aprendizaje principal no fue soldar componentes ni escribir código. Fue "
      "entender que un sistema de control empieza por definir qué se controla, qué se "
      "mide y qué se supone. Sin esa claridad, la simulación se convierte en un ejercicio "
      "de números sin significado.")


def recomendaciones(doc):
    h1(doc, "13. RECOMENDACIONES")
    add_bullets(doc, [
      "Completar el modelo en Simulink y comparar la respuesta simulada con las "
      "mediciones del prototipo.",
      "Validar los sensores contra equipos de referencia: oxímetro comercial, "
      "termómetro clínico y una prueba controlada de caída.",
      "Implementar deep sleep y medir el consumo real en cada modo de operación.",
      "Diseñar una carcasa que asegure el contacto del MAX30205 y reduzca el movimiento "
      "del sensor PPG.",
      "Agregar almacenamiento local para conservar el historial cuando no haya conexión.",
      "Cifrar la transmisión de datos y definir una política de privacidad para los "
      "signos vitales.",
      "Evaluar el prototipo con profesionales de salud antes de cualquier uso real.",
      "Como extensión, explorar algoritmos de detección de arritmias o de caídas con "
      "aprendizaje automático.",
    ])


def referencias(doc):
    h1(doc, "14. REFERENCIAS BIBLIOGRÁFICAS")
    refs = [
        "Apaza Mamani, E. F. (2023). Diseño de una central de monitoreo de parámetros de "
        "signos vitales [Proyecto académico].",
        "Arcos Coronel, F. E., & Quezada Patiño, J. S. (2023). Desarrollo de un sistema "
        "de monitoreo de frecuencia cardíaca y variables físicas para medir el desempeño "
        "en sesiones de entrenamiento de futbolistas usando tecnologías de comunicación "
        "inalámbrica [Proyecto académico].",
        "Atzori, L., Iera, A., & Morabito, G. (2010). The internet of things: A survey. "
        "Computer Networks, 54(15), 2787–2805.",
        "Axelson, J. (2015). Embedded systems: Introduction to microcontrollers for "
        "engineering students (2nd ed.). Lakeview Research.",
        "Badillo, J. A., Morales Martínez, D. A., Acuña Galván, I., & Lezama León, E. "
        "(2023). Prototipo para el monitoreo y registro de signos vitales como "
        "herramienta para el servicio médico de la Escuela Superior de Tizayuca (ESTi) "
        "[Proyecto académico].",
        "Barrett, S. F., & Pack, D. J. (2012). Embedded systems: Design and applications "
        "with the 68HC12 and HCS12 (2nd ed.). Pearson.",
        "Bickley, L. S. (2017). Bates' guide to physical examination and history taking "
        "(12th ed.). Wolters Kluwer.",
        "Botello Cardozo, D. M. (2022). Desarrollo de un dispositivo de fácil acceso para "
        "el monitoreo de signos vitales para personas que sufrieron infartos cardíacos "
        "[Proyecto académico].",
        "Carr, J. J., & Brown, J. M. (2001). Introduction to biomedical equipment "
        "technology (4th ed.). Prentice Hall.",
        "Dorf, R. C., & Bishop, R. H. (2011). Modern control systems (12th ed.). Pearson.",
        "Enderle, J. D., & Bronzino, J. D. (2012). Introduction to biomedical engineering "
        "(3rd ed.). Academic Press.",
        "Fuentes, R. C. (2022). Sistema IoT para monitoreo remoto de signos vitales "
        "[Proyecto académico].",
        "Gubbi, J., Buyya, R., Marusic, S., & Palaniswami, M. (2013). Internet of things "
        "(IoT): A vision, architectural elements, and future directions. Future "
        "Generation Computer Systems, 29(7), 1645–1660.",
        "Hall, J. E. (2016). Guyton and Hall textbook of medical physiology (13th ed.). "
        "Elsevier.",
        "Islam, S. M. R., Kwak, D., Kabir, M. H., Hossain, M., & Kwak, K. S. (2015). The "
        "internet of things for health care: A comprehensive survey. IEEE Access, 3, "
        "678–708.",
        "Laudon, K. C., & Laudon, J. P. (2016). Management information systems: Managing "
        "the digital firm (14th ed.). Pearson.",
        "Monk, S. (2013). Programming Arduino: Getting started with sketches (2nd ed.). "
        "McGraw-Hill.",
        "Nise, N. S. (2015). Control systems engineering (7th ed.). Wiley.",
        "Ogata, K. (2010). Modern control engineering (5th ed.). Pearson.",
        "Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). Operating system concepts "
        "(10th ed.). Wiley.",
        "Stallings, W. (2015). Computer organization and architecture: Designing for "
        "performance (10th ed.). Pearson.",
        "Tanenbaum, A. S., & Wetherall, D. J. (2011). Computer networks (5th ed.). "
        "Pearson.",
        "Tortora, G. J., & Derrickson, B. (2017). Principles of anatomy and physiology "
        "(15th ed.). Wiley.",
        "Webster, J. G. (Ed.). (2009). Medical instrumentation: Application and design "
        "(4th ed.). Wiley.",
    ]
    for ref in refs:
        par = doc.add_paragraph()
        run = par.add_run(ref)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
        par.paragraph_format.left_indent = Cm(1.25)
        par.paragraph_format.first_line_indent = Cm(-1.25)
        par.paragraph_format.line_spacing = 1.5
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.space_after = Pt(6)


def anexos(doc):
    h1(doc, "15. ANEXOS")
    h2(doc, "15.1 Tabla de componentes")
    t = add_table_with_data(
        doc,
        ["N.º", "Componente", "Función"],
        [
            ["1", "ESP32-C3 SuperMini", "Procesamiento, control y conectividad"],
            ["2", "MAX30102", "Frecuencia cardíaca y SpO2"],
            ["3", "MAX30205", "Temperatura corporal"],
            ["4", "MPU6050", "Aceleración, movimiento y caídas"],
            ["5", "OLED SSD1306 0.66\"", "Visualización local"],
            ["6", "Botón táctil", "Navegación entre pantallas"],
            ["7", "MOSFET", "Control del motor vibrador"],
            ["8", "TP4056 + LiPo 3.7 V + LDO 3.3 V", "Carga, alimentación y regulación"],
        ],
        title="Tabla 4. Componentes del prototipo.",
    )
    anchos(t, [1.4, 6.4, 7.2])

    h2(doc, "15.2 Tabla de entradas y salidas")
    t = add_table_with_data(
        doc,
        ["Variable", "Entradas (recibe del ESP32)", "Salidas (envía al ESP32)"],
        [
            ["mcu_heart", "4", "3"],
            ["sensor_ox", "1 (SCL)", "2 (SDA, INT)"],
            ["sensor_temp", "1 (SCL)", "1 (SDA)"],
            ["sensor_motion", "1 (SCL)", "2 (SDA, INT)"],
            ["display_main", "2 (SDA, SCL)", "0"],
            ["button_menu", "0", "1 (SIG)"],
            ["driver_motor", "1 (GATE)", "0"],
        ],
        title="Tabla 5. Entradas y salidas por variable de programación.",
        note="SCL es compartida por todos los dispositivos del bus I2C.",
    )
    anchos(t, [4.4, 5.4, 5.2])

    h2(doc, "15.3 Modelos de Simulink")
    p(doc,
      "En este apartado se adjuntarán el archivo .slx, las capturas del modelo y los "
      "scripts de inicialización de parámetros. El equipo los generará durante la fase "
      "de simulación.")
    pendiente(
        doc,
        "adjuntar el modelo .slx y las capturas de Simulink.",
        "Incluir el archivo del modelo, la configuración del solver, los parámetros "
        "usados y una captura legible del diagrama.",
    )
    caja_espacio(doc, "[ Espacio para el modelo .slx o captura ]", alto_cm=7.0)

    h2(doc, "15.4 Figuras del sistema")
    p(doc,
      "Las figuras del esquema electrónico y del funcionamiento con el usuario se "
      "incorporarán en este anexo. Las imágenes originales del proyecto no estaban "
      "disponibles en el archivo de texto de origen.")
    pendiente(
        doc,
        "insertar el esquema electrónico y el diagrama de funcionamiento.",
        "Agregar Figura 1 (esquema electrónico), Figura 2 (propósito de los componentes) "
        "y Figura 3 (funcionamiento con el usuario). Numerarlas y citarlas en el texto.",
    )
    caja_espacio(doc, "[ Figura 1 — Esquema electrónico ]", alto_cm=6.5)
    espacio(doc)
    caja_espacio(doc, "[ Figura 2 — Funcionamiento del sistema con el usuario ]", alto_cm=6.5)


# ---------------------------------------------------------------------------
def main():
    os.makedirs(SALIDA, exist_ok=True)
    doc = crear_documento()
    configurar_estilos(doc)
    configurar_heading1(doc)

    doc.core_properties.title = TITULO
    doc.core_properties.author = AUTORES.replace("\n", "; ")
    doc.core_properties.subject = "Sistemas de Control"
    doc.core_properties.keywords = "ESP32-C3, signos vitales, IoT, control, Simulink"

    sec0 = doc.sections[0]
    configurar_header(doc, sec0, mostrar=False)
    configurar_primer_header_vacio(doc, sec0)

    portada(doc)

    # Índice (sección sin numeración visible)
    sec_toc = agregar_nueva_seccion(doc, fmt=None)
    configurar_header(doc, sec_toc, mostrar=False)
    configurar_primer_header_vacio(doc, sec_toc)
    add_paragraph(doc, "ÍNDICE", bold=True, size=14,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0,
                  space_after=12)
    agregar_toc(doc)

    # Cuerpo (numeración desde 1, visible desde la primera página)
    sec_body = agregar_nueva_seccion(doc, fmt="decimal", start=1, mostrar=True)
    sec_body.different_first_page_header_footer = False

    resumen(doc)
    salto(doc)
    introduccion(doc)
    salto(doc)
    planteamiento(doc)
    salto(doc)
    objetivos(doc)
    salto(doc)
    justificacion(doc)
    salto(doc)
    alcances(doc)
    salto(doc)
    marco_teorico(doc)
    salto(doc)
    modelado(doc)
    salto(doc)
    diseno_control(doc)
    salto(doc)
    simulacion(doc)
    salto(doc)
    analisis(doc)
    salto(doc)
    discusion(doc)
    salto(doc)
    conclusiones(doc)
    salto(doc)
    recomendaciones(doc)
    salto(doc)
    referencias(doc)
    salto(doc)
    anexos(doc)

    ruta = os.path.join(SALIDA, NOMBRE)
    doc.save(ruta)
    print(ruta)


if __name__ == "__main__":
    main()
