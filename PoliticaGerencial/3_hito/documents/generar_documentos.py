# -*- coding: utf-8 -*-
"""Genera los dos .docx del 3er hito de Política Gerencial.

1. Investigacion_Objetivos_Estrategicos_BCG_Comunicacion_Efectiva.docx
2. Aplicacion_Practica_Nova_Eventos_Implementacion.docx

Usa la librería base_documento.py como plantilla de estilos.
"""
import os
import sys

sys.path.insert(0, "/home/eynor/Documents/2_Proyect_Private/0_biblioteca-Skills")

from base_documento import (  # noqa: E402
    crear_documento,
    configurar_estilos,
    add_heading_custom,
    add_table_with_data,
    add_code_block,
    agregar_toc,
    agregar_referencias,
    agregar_nueva_seccion,
    configurar_header,
    configurar_primer_header_vacio,
    Cm,
    Pt,
    RGBColor,
    WD_ALIGN_PARAGRAPH,
)
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = ("/home/eynor/Documents/2_Proyect_Private/0_biblioteca-Skills/"
        "logoUnifranz/logounifranz.png")

AUTOR = "BRAYAN QUISPE MAMANI"
ASIGNATURA = "POLÍTICA Y GERENCIA EMPRESARIAL"
DOCENTE = "______________________________"
ANIO = "2026"

SALIDA_INV = "Investigacion_Objetivos_Estrategicos_BCG_Comunicacion_Efectiva.docx"
SALIDA_IMP = "Aplicacion_Practica_Nova_Eventos_Implementacion.docx"


# ------------------------------------------------------------------ helpers
def add_parrafo(doc, partes, size=12, bold=False, italic=False, alignment=None,
                space_before=0, space_after=0, first_line_indent=None,
                left_indent=None, line_spacing=1.5):
    """Párrafo con énfasis parcial: partes = str o [(texto, bold, italic), ...]."""
    if isinstance(partes, str):
        partes = [partes]
    p = doc.add_paragraph()
    for parte in partes:
        if isinstance(parte, str):
            txt, b, i = parte, bold, italic
        else:
            txt = parte[0]
            b = parte[1] if len(parte) > 1 else False
            i = parte[2] if len(parte) > 2 else False
        run = p.add_run(txt)
        run.font.name = 'Arial'
        run.font.size = Pt(size)
        run.font.bold = b
        run.font.italic = i
        run.font.color.rgb = RGBColor(0, 0, 0)
    if alignment is not None:
        p.alignment = alignment
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.first_line_indent = Cm(1.25) if first_line_indent is None else Cm(first_line_indent)
    if left_indent is not None:
        pf.left_indent = Cm(left_indent)
    pf.line_spacing = line_spacing
    return p


def add_items(doc, items, numerado=False, nivel=0, start=1):
    """Viñetas o lista numerada con sangría francesa. items: str o (etiqueta, texto)."""
    for idx, item in enumerate(items, start):
        if isinstance(item, str):
            partes = [item]
        else:
            partes = [(item[0], True), item[1]]
        if numerado:
            prefijo = f'{idx}. '
            left, first = 1.5, -0.8
        else:
            prefijo = '  \u2022  '
            left = 1.5 + 1.5 * nivel
            first = -0.85
        add_parrafo(doc, [prefijo] + partes, left_indent=left,
                    first_line_indent=first)


def set_col_widths(table, widths_cm):
    """Fija anchos de columna (cm) y evita filas/encabezados partidos entre páginas."""
    table.autofit = False
    for fila in table.rows:
        for idx, ancho in enumerate(widths_cm):
            fila.cells[idx].width = Cm(ancho)
        trPr = fila._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
    for idx, ancho in enumerate(widths_cm):
        table.columns[idx].width = Cm(ancho)
    header_trPr = table.rows[0]._tr.get_or_add_trPr()
    header_trPr.append(OxmlElement('w:tblHeader'))
    anterior = table._tbl.getprevious()
    if anterior is not None and anterior.tag == qn('w:p'):
        pPr = anterior.get_or_add_pPr()
        if pPr.find(qn('w:keepNext')) is None:
            pPr.append(OxmlElement('w:keepNext'))


def add_cita(doc, texto):
    """Párrafo en cursiva con sangría izquierda (definición citada, visión, etc.)."""
    return add_parrafo(doc, texto, italic=True, left_indent=1.5,
                       first_line_indent=0, space_before=6, space_after=6)


def add_formula(doc, texto):
    return add_parrafo(doc, texto, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                       first_line_indent=0, space_before=6, space_after=6)


def linea_centrada(doc, texto, size=12, bold=False, space_after=0, space_before=0):
    return add_parrafo(doc, texto, size=size, bold=bold,
                       alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=space_before,
                       space_after=space_after, first_line_indent=0)


def agregar_caratula(doc, titulo):
    doc.add_paragraph()
    linea_centrada(doc, "UNIVERSIDAD PRIVADA FRANZ TAMAYO", size=14, bold=True)
    linea_centrada(doc, "SEDE EL ALTO", size=14, bold=True)
    linea_centrada(doc, "FACULTAD DE INGENIERÍA", size=14, bold=True)
    linea_centrada(doc, "CARRERA DE INGENIERÍA DE SISTEMAS", size=14, bold=True,
                   space_after=18)
    linea_centrada(doc, titulo, size=14, bold=True, space_before=10, space_after=18)
    if os.path.exists(LOGO):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.first_line_indent = Cm(0)
        p_logo.paragraph_format.space_after = Pt(12)
        p_logo.add_run().add_picture(LOGO, width=Cm(6.04), height=Cm(5.73))
    linea_centrada(doc, f"AUTOR: {AUTOR}", size=12, space_after=6)
    linea_centrada(doc, f"ASIGNATURA: {ASIGNATURA}", size=12, space_after=6)
    linea_centrada(doc, f"DOCENTE: {DOCENTE}", size=12, space_after=12)
    linea_centrada(doc, "EL ALTO – BOLIVIA", size=12, bold=True)
    linea_centrada(doc, ANIO, size=12, bold=True)


def preparar(doc, titulo):
    configurar_header(doc, doc.sections[0], mostrar=False)
    agregar_caratula(doc, titulo)
    agregar_nueva_seccion(doc, fmt='upperRoman', start=1, mostrar=True)
    agregar_toc(doc)
    agregar_nueva_seccion(doc, fmt='decimal', start=1, mostrar=True)


def h2(doc, texto):
    return add_heading_custom(doc, texto, level=2)


def h3(doc, texto):
    return add_heading_custom(doc, texto, level=3)


# ========================================================== DOC 1: INVESTIGACIÓN
def generar_investigacion():
    doc = crear_documento()
    configurar_estilos(doc)
    preparar(
        doc,
        "ESTABLECIMIENTO DE LOS OBJETIVOS ESTRATÉGICOS, MATRIZ BOSTON "
        "CONSULTING GROUP (BCG) Y ESTRATEGIAS DE COMUNICACIÓN EFECTIVA",
    )

    # ---------------------------------------------------------------- 1
    h2(doc, '1. Introducción')
    add_parrafo(doc,
        "El presente documento desarrolla la investigación de tres puntos del plan "
        "de trabajo de la asignatura Política y Gerencia Empresarial: el "
        "establecimiento de los objetivos estratégicos, la matriz Boston Consulting "
        "Group (BCG) y su relación con el posicionamiento, y las estrategias de "
        "comunicación efectiva.")
    add_parrafo(doc,
        "La selección de estos temas responde a su utilidad para la gestión "
        "empresarial contemporánea y, de manera especial, para el ejercicio "
        "profesional en Ingeniería de Sistemas, donde la formulación de metas, la "
        "priorización de portafolios tecnológicos y la coordinación entre actores "
        "determinan el éxito de los proyectos.")
    add_parrafo(doc,
        "Para cada punto se presenta la definición y el concepto, la forma en que se "
        "desarrolla o aplica, los casos principales de uso y un ejemplo vinculado con "
        "el ámbito tecnológico. La información fue organizada a partir de fuentes "
        "bibliográficas y digitales confiables, cuyas referencias se listan en la "
        "bibliografía final conforme a la norma APA 7.ª edición.")

    # ---------------------------------------------------------------- 2
    h2(doc, '2. Establecimiento de los Objetivos Estratégicos')

    h3(doc, '2.1 Definición y concepto')
    add_parrafo(doc, [
        ("Los Objetivos Estratégicos", True),
        " son las metas cuantitativas y cualitativas de alto nivel que una "
        "organización define para alcanzar en un horizonte temporal de mediano o "
        "largo plazo (generalmente de 3 a 5 años). Representan la operacionalización "
        "del ",
        ("Objetivo General", True),
        ", desglosándolo en logros concretos por cada dimensión funcional de la "
        "empresa (David y David, 2017).",
    ])
    add_parrafo(doc, [
        "En el marco de la ",
        ("Ingeniería de Sistemas", True),
        ", los objetivos estratégicos conectan las metas de negocio con los activos "
        "tecnológicos, garantizando que el desarrollo de software, la infraestructura "
        "de TI y la gestión de datos aporten valor real a la organización "
        "(Kaplan y Norton, 1996).",
    ])

    h3(doc, '2.2 Cómo se Desarrollan')
    add_parrafo(doc,
        "El proceso metodológico para la formulación de objetivos estratégicos sigue "
        "una secuencia lógica:")
    add_code_block(doc, [
        "        [Visión y Misión]",
        "              │",
        "              ▼",
        "   [Diagnóstico FODA / PESTEL]",
        "              │",
        "              ▼",
        "      [Objetivo General]",
        "              │",
        "              ▼",
        "[Objetivos Estratégicos (SMART)]",
    ])
    add_items(doc, [
        ("Alineación con el diagnóstico: ",
         "se derivan de cruzar las fortalezas y oportunidades del análisis FODA "
         "(por ejemplo, aprovechar una fortaleza técnica para capturar una "
         "oportunidad de mercado)."),
        ("Aplicación de criterios SMART: ",
         "cada objetivo debe formularse bajo cinco atributos verificables."),
    ], numerado=True)
    add_items(doc, [
        ("S (Specific / Específico): ",
         "definir qué se va a lograr de manera clara y sin ambigüedades."),
        ("M (Measurable / Medible): ",
         "asociar el objetivo a un indicador clave de rendimiento (KPI)."),
        ("A (Achievable / Alcanzable): ",
         "garantizar que sea factible con los recursos disponibles."),
        ("R (Relevant / Relevante): ",
         "orientarlo directamente a las prioridades del negocio."),
        ("T (Time-bound / Temporal): ",
         "asignar un plazo estricto de cumplimiento."),
    ], nivel=1)
    add_items(doc, [
        ("Mapeo por perspectiva: ",
         "clasificar cada objetivo dentro de las cuatro perspectivas del Balanced "
         "Scorecard (Financiera, Cliente, Procesos Internos, Aprendizaje y "
         "Crecimiento)."),
    ], numerado=True, start=3)

    h3(doc, '2.3 En Qué Casos Son Usados')
    add_items(doc, [
        ("Reestructuración o transformación digital: ",
         "cuando una empresa tradicional migra a arquitecturas en la nube o adopta "
         "modelos SaaS."),
        ("Gestión de portafolio de proyectos (PPM): ",
         "para priorizar qué sistemas o proyectos de software deben financiarse y "
         "desarrollarse primero."),
        ("Evaluación del desempeño: ",
         "para alinear las metas del equipo directivo y del área de ingeniería con "
         "los incentivos corporativos."),
    ])

    h3(doc, '2.4 Ejemplo de Aplicación en Ingeniería de Sistemas')
    add_parrafo(doc, "Como ejemplo, una organización puede plantear el siguiente "
                     "objetivo estratégico:")
    add_cita(doc,
        "\u201cReducir el tiempo promedio de despliegue de software en producción "
        "(Lead Time for Changes) de 14 días a menos de 4 horas en los próximos "
        "12 meses, manteniendo una tasa de fallas menor al 1%.\u201d")
    add_parrafo(doc, [
        ("KPI asociado: ", True),
        "tiempo de ciclo de despliegue CI/CD y porcentaje de despliegues exitosos.",
    ])

    # ---------------------------------------------------------------- 3
    h2(doc, '3. Matriz \u201cBoston Consulting Group\u201d (BCG) y Posicionamiento')

    h3(doc, '3.1 Definición y Concepto')
    add_parrafo(doc, [
        "La ",
        ("Matriz BCG", True),
        " (o matriz Crecimiento-Participación) es un modelo analítico de gestión "
        "estratégica desarrollado por Bruce D. Henderson para la firma Boston "
        "Consulting Group en 1970. Esta herramienta evalúa la cartera de productos o "
        "Unidades de Negocio Estratégicas (UNE) en función de dos variables "
        "bidimensionales (Henderson, 1970):",
    ])
    add_items(doc, [
        ("Tasa de crecimiento del mercado (eje vertical): ",
         "mide el atractivo de la industria."),
        ("Cuota de mercado relativa (eje horizontal): ",
         "mide la ventaja competitiva de la empresa frente a su competidor "
         "principal."),
    ], numerado=True)
    tabla = add_table_with_data(
        doc,
        ["Tasa de crecimiento del mercado", "Cuota de mercado relativa alta",
         "Cuota de mercado relativa baja"],
        [
            ["Alto", "ESTRELLA — Invertir y mantener",
             "INTERROGACIÓN — Evaluar o seleccionar"],
            ["Bajo", "VACA LECHERA — Ordeñar o cosechar",
             "PERRO — Reestructurar o liquidar"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.CENTER] * 3,
        title="Tabla 1. Matriz BCG: los cuatro cuadrantes de posicionamiento.",
        note="Elaboración propia a partir de Henderson (1970) y Kotler y Keller (2016).",
    )
    set_col_widths(tabla, [5.0, 5.5, 5.5])

    h3(doc, '3.2 Análisis de los 4 Cuadrantes y Posicionamiento')
    tabla = add_table_with_data(
        doc,
        ["Cuadrante", "Características financieras / operativas",
         "Estrategia recomendada", "Ejemplo en empresas de TI / software"],
        [
            ["Estrella (High Growth / High Share)",
             "Alto crecimiento y alta participación. Generan grandes ingresos pero "
             "requieren alta inversión para mantener el liderazgo.",
             "Invertir y mantener: consolidar infraestructura y escalar la capacidad "
             "operativa.",
             "Plataformas de IA generativa en expansión corporativa (por ejemplo, "
             "OpenAI enterprise)."],
            ["Vaca Lechera (Low Growth / High Share)",
             "Bajo crecimiento y alta participación. Generan excedentes de caja "
             "constantes con mínimos costos de reinversión.",
             "Ordeñar o cosechar: utilizar el flujo de efectivo generado para "
             "financiar productos Estrella e Interrogante.",
             "Sistemas ERP locales tradicionales o licencias de bases de datos "
             "relacionales maduras (por ejemplo, Oracle o SAP)."],
            ["Signo de Interrogación (High Growth / Low Share)",
             "Alto crecimiento pero baja participación. Requieren mucha liquidez "
             "para competir; su futuro es incierto.",
             "Evaluar o seleccionar: decidir si invertir agresivamente para "
             "convertirlo en Estrella o desinvertir.",
             "Nuevos módulos de analítica cuántica o blockchain empresarial."],
            ["Perro (Low Growth / Low Share)",
             "Bajo crecimiento y baja participación. Consumen recursos sin generar "
             "rendimientos significativos.",
             "Reestructurar o liquidar: eliminar del portafolio o descontinuar el "
             "soporte técnico.",
             "Alojamiento en servidores físicos dedicados legacy o software en "
             "lenguajes obsoletos."],
        ],
        title="Tabla 2. Análisis de los cuadrantes de la matriz BCG.",
        note="Elaboración propia a partir de Henderson (1970) y Kotler y Keller (2016).",
    )
    set_col_widths(tabla, [3.2, 5.0, 4.3, 3.5])

    h3(doc, '3.3 Cómo se Desarrolla el Análisis')
    add_items(doc, [
        ("Identificar las UNE o servicios: ",
         "definir la lista de productos o líneas de servicios tecnológicos de la "
         "empresa."),
        ("Calcular la cuota relativa de mercado: ",
         "comparar las ventas de la empresa frente a las de su competidor líder."),
        ("Determinar la tasa de crecimiento: ",
         "analizar la tasa de variación anual del sector o segmento."),
        ("Graficar los productos: ",
         "trazar círculos donde el tamaño representa la contribución en ingresos de "
         "cada producto."),
    ], numerado=True)
    add_formula(doc,
        "Cuota relativa de mercado = Ventas de la empresa / Ventas del competidor "
        "líder")

    h3(doc, '3.4 En Qué Casos Es Usada')
    add_items(doc, [
        ("Gestión del ciclo de vida del software: ",
         "para decidir cuándo retirar soporte a un sistema antiguo (legacy) y "
         "cuándo financiar una migración a la nube."),
        ("Asignación del presupuesto tecnológico (I+D): ",
         "para no malgastar el presupuesto de desarrollo en tecnologías que están "
         "en declive."),
        ("Fusiones y adquisiciones (M&A): ",
         "para evaluar el portafolio de una startup tecnológica antes de comprarla."),
    ])

    # ---------------------------------------------------------------- 4
    h2(doc, '4. Estrategias de Comunicación Efectiva')

    h3(doc, '4.1 Definición y Concepto')
    add_parrafo(doc, [
        "La ",
        ("Comunicación Efectiva", True),
        " en la gestión empresarial es el conjunto de procesos, canales y protocolos "
        "diseñados para garantizar que la información estratégica (visión, "
        "políticas, requerimientos y metas) sea transmitida, comprendida y ejecutada "
        "correctamente sin distorsión (ruido) entre los distintos actores "
        "organizacionales (Robbins y Judge, 2018).",
    ])
    add_parrafo(doc, [
        "En entornos de ",
        ("Ingeniería de Sistemas y Desarrollo de Software", True),
        ", donde la complejidad técnica es alta, la comunicación efectiva actúa como "
        "el puente imprescindible entre los stakeholders de negocio (quienes tienen "
        "las necesidades) y los equipos técnicos (quienes construyen la solución) "
        "(Pressman y Maxim, 2020).",
    ])

    h3(doc, '4.2 Tipos y Canales de Comunicación')
    add_parrafo(doc, [("Comunicación interna", True)], first_line_indent=0,
                space_before=6)
    add_items(doc, [
        ("Descendente (Top-Down): ",
         "transmisión de metas de la alta dirección a los ingenieros y desarrolladores "
         "(por ejemplo, comunicados ejecutivos, town halls)."),
        ("Ascendente (Bottom-Up): ",
         "retroalimentación desde el equipo operativo hacia la gerencia (por ejemplo, "
         "reportes de riesgos, retrospectivas de sprints, métricas de error)."),
        ("Horizontal o cruzada: ",
         "colaboración directa entre áreas de desarrollo, ciberseguridad, "
         "infraestructura y calidad (por ejemplo, metodologías DevOps, cultura "
         "Agile)."),
    ])
    add_parrafo(doc, [("Comunicación externa", True)], first_line_indent=0,
                space_before=6)
    add_items(doc, [
        "Transmisión de valor hacia clientes, proveedores e inversionistas a través "
        "de portales de transparencia, release notes, documentación de API públicas "
        "y Acuerdos de Nivel de Servicio (SLA).",
    ])

    h3(doc, '4.3 Cómo se Desarrollan las Estrategias de Comunicación')
    add_items(doc, [
        ("Definición de matriz de comunicación (stakeholder mapping): ",
         "identificar qué información requiere cada actor, con qué frecuencia y a "
         "través de qué canal."),
        ("Estandarización del lenguaje: ",
         "utilizar vocabularios y diagramaciones estándar (notación UML, "
         "arquitectura C4, lenguaje de negocio en BDD) para evitar ambigüedades "
         "entre ingenieros y clientes."),
        ("Selección del stack de herramientas: ",
         "implementar plataformas colaborativas integradas (por ejemplo, Jira, "
         "Confluence, Slack y dashboards automatizados)."),
        ("Bucles de retroalimentación (feedback loops): ",
         "establecer reuniones cortas y sistemáticas (como las dailies o revisiones "
         "de avance) para corregir desviaciones tempranamente."),
    ], numerado=True)

    h3(doc, '4.4 En Qué Casos Son Usadas')
    add_items(doc, [
        ("Gestión del cambio organizacional: ",
         "al migrar la infraestructura de la empresa a un nuevo sistema ERP o CRM."),
        ("Proyectos complejos de software (Agile/Scrum): ",
         "para alinear continuamente el trabajo de los programadores con los cambios "
         "en los requerimientos del cliente."),
        ("Gestión de incidentes críticos: ",
         "ante una caída masiva de servidores o una brecha de seguridad, para "
         "coordinar la respuesta técnica e informar adecuadamente a los clientes."),
    ])

    h3(doc, '4.5 Ejemplo de Aplicación en Ingeniería de Sistemas')
    add_parrafo(doc, [
        ("Modelo de documentación técnica centralizada: ", True),
        "creación de un sitio de Confluence donde las políticas de arquitectura de "
        "software se traducen en guías visuales sencillas, reduciendo las reuniones "
        "de aclaración en un 40%.",
    ])

    # ---------------------------------------------------------------- 5
    h2(doc, '5. Conclusiones')
    add_items(doc, [
        "Los objetivos estratégicos traducen la visión de la organización en metas "
        "SMART y medibles; sin ellos, la planificación se quedaría en declaraciones "
        "de intención difícilmente auditables.",
        "La matriz BCG permite decidir con criterio dónde invertir, qué mantener y "
        "qué desinvertir en el portafolio de productos o servicios, evitando "
        "dispersar recursos escasos en líneas sin potencial.",
        "La comunicación efectiva es el mecanismo que hace ejecutable la estrategia: "
        "alinea a los stakeholders, reduce la ambigüedad y acelera la "
        "retroalimentación entre negocio y equipos técnicos.",
        "En conjunto, los tres temas forman un ciclo: se fijan los objetivos, se "
        "priorizan con herramientas de análisis y se sostienen con comunicación "
        "ordenada; en Ingeniería de Sistemas, su aplicación mejora la entrega de "
        "valor tecnológico.",
    ])

    agregar_referencias(doc, [
        "David, F. R., & David, F. R. (2017). Strategic Management: A Competitive "
        "Advantage Approach, Concepts and Cases (16.ª ed.). Pearson Education.",
        "Henderson, B. D. (1970). The Product Portfolio. Boston Consulting Group "
        "Perspectives, No. 66.",
        "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard: Translating "
        "Strategy into Action. Harvard Business School Press.",
        "Kotler, P., & Keller, K. L. (2016). Marketing Management (15.ª ed.). "
        "Pearson Education.",
        "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A "
        "Practitioner's Approach (9.ª ed.). McGraw-Hill Education.",
        "Robbins, S. P., & Judge, T. A. (2018). Organizational Behavior (18.ª ed.). "
        "Pearson Education.",
    ])

    salida = os.path.join(AQUI, SALIDA_INV)
    doc.save(salida)
    print("Documento generado:", salida)


# ====================================================== DOC 2: IMPLEMENTACIÓN
def generar_implementacion():
    doc = crear_documento()
    configurar_estilos(doc)
    preparar(
        doc,
        "APLICACIÓN PRÁCTICA DE LA PLANIFICACIÓN ESTRATÉGICA: IMPLEMENTACIÓN "
        "DEL SERVICIO NOVA EXPERIENCE EN NOVA EVENTOS",
    )

    # ---------------------------------------------------------------- 1
    h2(doc, '1. Introducción')
    add_parrafo(doc,
        "El presente documento aplica los temas investigados —establecimiento de "
        "objetivos estratégicos, matriz Boston Consulting Group (BCG) y estrategias "
        "de comunicación efectiva— a una empresa concreta, conforme a la sección 3 "
        "de la tarea de la asignatura.")
    add_parrafo(doc,
        "La empresa seleccionada es Nova Eventos, una empresa ficticia de servicios "
        "dedicada a la organización y producción de acontecimientos sociales en la "
        "ciudad de La Paz, Bolivia, que propone implementar Nova Experience, una "
        "línea de eventos temáticos personalizados dirigida a jóvenes adultos de 18 "
        "a 30 años.")
    add_parrafo(doc,
        "El documento se organiza en la presentación de la empresa, la aplicación de "
        "los tres temas investigados a su realidad, un ejemplo práctico de "
        "implementación con cronograma, presupuesto e indicadores de seguimiento, y "
        "una conclusión sobre la importancia y los beneficios de aplicar el tema en "
        "la empresa.")

    # ---------------------------------------------------------------- 2
    h2(doc, '2. Presentación de la Empresa')

    h3(doc, '2.1 Descripción de la Empresa')
    add_parrafo(doc,
        "Nova Eventos es una empresa ficticia de servicios dedicada a la "
        "planificación, organización y producción de acontecimientos sociales. Su "
        "actividad comprende la coordinación de espacios, decoración, sonido, "
        "iluminación, animación, catering, fotografía y otros componentes necesarios "
        "para la ejecución de eventos.")
    add_parrafo(doc,
        "La empresa desarrolla sus actividades en la ciudad de La Paz y trabaja "
        "mediante la contratación de proveedores especializados, lo que le permite "
        "adaptar cada proyecto a las características y posibilidades económicas de "
        "sus clientes. Actualmente ofrece servicios convencionales para cumpleaños, "
        "aniversarios, reuniones familiares y celebraciones privadas.")

    h3(doc, '2.2 Datos Generales')
    tabla = add_table_with_data(
        doc,
        ["Elemento", "Descripción"],
        [
            ["Nombre comercial", "Nova Eventos"],
            ["Naturaleza", "Empresa ficticia de servicios"],
            ["Sector económico", "Servicios de organización de eventos"],
            ["Ubicación", "La Paz, Bolivia"],
            ["Mercado actual", "Familias, particulares y pequeños grupos"],
            ["Nuevo segmento", "Jóvenes adultos de 18 a 30 años"],
            ["Nuevo servicio", "Nova Experience"],
            ["Modalidad de atención", "Presencial, digital e híbrida"],
            ["Modelo de operación", "Equipo organizador y red de proveedores"],
        ],
        title="Tabla 1. Datos generales de Nova Eventos.",
    )
    set_col_widths(tabla, [5.0, 10.8])

    h3(doc, '2.3 Servicio Actual y Necesidad de Innovación')
    add_parrafo(doc,
        "El servicio actual incluye la organización integral del evento: "
        "planificación, contratación de proveedores, ambientación, control de "
        "horarios y supervisión de la ejecución. Esta oferta, sin embargo, presenta "
        "limitaciones cuando el cliente busca una experiencia temática, una "
        "propuesta visual atractiva, una administración transparente del presupuesto "
        "o una participación más activa en el diseño de su celebración.")
    add_parrafo(doc,
        "Por ello, la innovación se plantea como estrategia de crecimiento y "
        "diferenciación: en lugar de competir únicamente mediante descuentos, la "
        "empresa mantendrá sus servicios actuales e incorporará Nova Experience como "
        "nueva línea comercial, cuya aceptación se evaluará mediante una prueba "
        "piloto.")

    h3(doc, '2.4 El Nuevo Servicio: Nova Experience')
    add_parrafo(doc,
        "Nova Experience será una línea especializada en el diseño, planificación y "
        "ejecución de eventos temáticos personalizados para jóvenes adultos de 18 a "
        "30 años. Su proceso de atención comprende consulta inicial, diseño "
        "conceptual, cotización, coordinación de proveedores, preparación, ejecución "
        "y evaluación de satisfacción.")
    tabla = add_table_with_data(
        doc,
        ["Paquete", "Precio de referencia (Bs)", "Características"],
        [
            ["Nova Essential", "1.800",
             "Planificación básica, coordinación y decoración temática sencilla."],
            ["Nova Plus", "3.500",
             "Diseño personalizado, decoración ampliada, coordinación de proveedores "
             "y planificación audiovisual básica."],
            ["Nova Experience Premium", "5.500",
             "Diseño integral, ambientación avanzada, coordinación prioritaria y "
             "contenido fotográfico o audiovisual según el alcance acordado."],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER,
                        WD_ALIGN_PARAGRAPH.LEFT],
        title="Tabla 2. Paquetes comerciales propuestos.",
        note="Los precios son estimaciones preliminares de diseño comercial y deben "
             "validarse con cotizaciones reales de proveedores; no incluyen "
             "automáticamente alquiler del espacio, alimentación, transporte ni "
             "impuestos.",
    )
    set_col_widths(tabla, [3.8, 3.0, 9.0])

    # ---------------------------------------------------------------- 3
    h2(doc, '3. Aplicación de los Temas Investigados')
    add_parrafo(doc,
        "Esta sección aplica los tres puntos investigados en el documento de "
        "investigación a la realidad de Nova Eventos.")

    h3(doc, '3.1 Dirección Estratégica: Visión, Misión, Valores y Objetivo General')
    add_parrafo(doc, [("Visión. ", True),
        ("Ser una empresa reconocida en La Paz por ofrecer experiencias sociales "
         "creativas, personalizadas y confiables, destacándose por la calidad de su "
         "organización, la innovación en sus servicios y la satisfacción de sus "
         "clientes.", False, True)])
    add_parrafo(doc, [("Misión. ", True),
        ("Planificar y ejecutar eventos sociales mediante soluciones personalizadas, "
         "presupuestos transparentes, proveedores confiables y herramientas "
         "digitales que permitan a los clientes disfrutar de celebraciones "
         "organizadas de acuerdo con sus preferencias y posibilidades económicas.",
         False, True)])
    add_parrafo(doc, "Valores empresariales:", first_line_indent=0, space_before=6)
    add_items(doc, [
        ("Responsabilidad:", " cumplir los compromisos asumidos con clientes y "
         "proveedores."),
        ("Creatividad:", " desarrollar propuestas originales de acuerdo con cada "
         "evento."),
        ("Transparencia:", " comunicar claramente los costos, condiciones y alcances "
         "del servicio."),
        ("Calidad:", " mantener procedimientos de planificación y control."),
        ("Innovación:", " incorporar herramientas y métodos que mejoren la "
         "experiencia del cliente."),
        ("Sostenibilidad:", " promover el uso responsable de materiales y recursos."),
        ("Respeto:", " atender a los clientes sin discriminación y considerar sus "
         "preferencias."),
    ])
    add_parrafo(doc, [("Objetivo general. ", True),
        ("Implementar el servicio Nova Experience durante un periodo de seis meses, "
         "dirigido a jóvenes adultos de 18 a 30 años de La Paz, mediante una "
         "propuesta de eventos temáticos personalizados que combine creatividad, "
         "transparencia presupuestaria, promoción digital y coordinación "
         "profesional.", False, True)])

    h3(doc, '3.2 Establecimiento de los Objetivos Estratégicos')
    add_parrafo(doc,
        "El objetivo general se desglosa en objetivos específicos que cumplen los "
        "criterios SMART y se clasifican en las cuatro perspectivas del Balanced "
        "Scorecard (Kaplan y Norton, 1996). De este modo, cada meta tiene un "
        "indicador y un plazo verificables (David et al., 2020):")
    tabla = add_table_with_data(
        doc,
        ["Objetivo estratégico", "Meta y plazo (criterio SMART)",
         "Perspectiva (Balanced Scorecard)"],
        [
            ["Investigación del segmento",
             "100 encuestas exploratorias a jóvenes de 18 a 30 años durante el "
             "mes 1", "Cliente"],
            ["Diseño de la oferta comercial",
             "3 paquetes diferenciados en los meses 1 y 2", "Procesos internos"],
            ["Alianzas con proveedores",
             "Al menos 5 proveedores aliados durante los primeros 3 meses",
             "Procesos internos"],
            ["Validación del servicio",
             "Mínimo 3 eventos piloto en los meses 4 y 5", "Cliente"],
            ["Resultado comercial",
             "12 contratos pagados acumulados en 6 meses", "Financiera"],
            ["Satisfacción del cliente",
             "Calificación promedio igual o superior a 4,5 / 5 tras cada evento",
             "Cliente"],
            ["Cumplimiento operativo",
             "90 % de eventos ejecutados conforme al cronograma en el primer "
             "semestre", "Procesos internos"],
            ["Desarrollo del equipo",
             "100 % del personal involucrado capacitado antes del lanzamiento",
             "Aprendizaje y Crecimiento"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
                        WD_ALIGN_PARAGRAPH.LEFT],
        title="Tabla 3. Objetivos estratégicos de Nova Eventos.",
        note="Elaboración propia a partir de los objetivos del proyecto; las metas "
             "son estimaciones de gestión sujetas a validación de mercado "
             "(David et al., 2020; Kaplan y Norton, 1996).",
    )
    set_col_widths(tabla, [4.2, 8.0, 3.8])
    add_parrafo(doc,
        "Los objetivos conectan las metas de negocio con la operación diaria: la "
        "meta de 12 contratos se vincula con la perspectiva financiera, la "
        "satisfacción de 4,5 / 5 con la perspectiva del cliente y la capacitación "
        "del equipo con el aprendizaje y crecimiento.")

    h3(doc, '3.3 Matriz BCG Aplicada al Portafolio de Servicios')
    add_parrafo(doc,
        "Para priorizar el uso de sus recursos, Nova Eventos aplica la matriz BCG a "
        "sus líneas de servicio (Henderson, 1970; Kotler y Keller, 2016). El primer "
        "paso consiste en identificar las líneas de negocio; el segundo, estimar la "
        "cuota relativa de mercado comparando sus ventas con las del competidor de "
        "referencia; el tercero, determinar el crecimiento del segmento; y el "
        "cuarto, representar cada línea en la matriz.")
    add_parrafo(doc,
        "Como empresa en lanzamiento, Nova Eventos no cuenta todavía con ventas "
        "históricas del nuevo servicio; por ello, la participación relativa se "
        "estima de manera preliminar a partir de la base actual de clientes y de la "
        "encuesta exploratoria a 100 personas, sin utilizar cifras inventadas.")
    tabla = add_table_with_data(
        doc,
        ["Línea de servicio", "Crecimiento del segmento", "Participación relativa",
         "Cuadrante", "Estrategia recomendada"],
        [
            ["Eventos sociales convencionales (cumpleaños, aniversarios, "
             "reuniones)", "Baja", "Media-alta (base actual de clientes)",
             "Vaca lechera",
             "Ordeñar: destinar sus excedentes para financiar el lanzamiento de "
             "Nova Experience."],
            ["Nova Experience — paquetes Essential y Plus", "Alta",
             "Baja (marca nueva)", "Signo de interrogación",
             "Evaluar con 3 eventos piloto e invertir si se alcanza una "
             "satisfacción igual o superior a 4,5 / 5."],
            ["Nova Experience Premium (diseño integral y audiovisual)", "Alta",
             "Baja, con potencial en el nicho premium",
             "Signo de interrogación con potencial de estrella",
             "Invertir y mantener tras validar la demanda; meta de 2 contratos "
             "premium en 6 meses."],
            ["Venta suelta de componentes sin coordinación (servicio aislado)",
             "Baja", "Baja", "Perro",
             "Descontinuar o incorporar como complemento opcional de los "
             "paquetes."],
        ],
        title="Tabla 4. Matriz BCG aplicada al portafolio de Nova Eventos.",
        note="Clasificación preliminar elaborada para este caso; la participación "
             "relativa deberá medirse con datos reales de ventas propias y del "
             "competidor de referencia (Henderson, 1970; Kotler y Keller, 2016).",
    )
    set_col_widths(tabla, [4.2, 2.6, 3.2, 3.0, 3.0])
    add_parrafo(doc,
        "La decisión estratégica es directa: la inversión inicial de Bs 9.350 se "
        "concentra en el signo de interrogación (Nova Experience), financiada por "
        "los excedentes de los eventos convencionales (vaca lechera), mientras que "
        "los servicios sueltos sin coordinación (perro) se descontinuarán o se "
        "incorporarán como complementos opcionales de los paquetes.")

    h3(doc, '3.4 Estrategias de Comunicación Efectiva Aplicadas')
    add_parrafo(doc,
        "La comunicación efectiva garantiza que la información estratégica llegue "
        "sin distorsión a cada actor de la organización (Robbins y Judge, 2018). "
        "Para Nova Eventos, esto implica definir quién necesita qué información, con "
        "qué frecuencia y por qué canal:")
    tabla = add_table_with_data(
        doc,
        ["Actor (stakeholder)", "Información necesaria", "Frecuencia", "Canal"],
        [
            ["Cliente potencial", "Paquetes, precios y portafolio de eventos",
             "Continua", "Redes sociales, WhatsApp, catálogo digital"],
            ["Cliente contratado",
             "Cronograma, cambios y presupuesto desglosado",
             "Semanal y por hito",
             "Tablero digital del evento, WhatsApp, correo"],
            ["Proveedores",
             "Horarios, formatos de coordinación y responsabilidades",
             "Por evento y reunión mensual",
             "Reuniones, correo, cronograma compartido"],
            ["Personal interno",
             "Procedimientos, metas, avances y capacitación",
             "Diaria y semanal",
             "Reuniones breves, guías y listas de control"],
            ["Administración",
             "Gastos, autorizaciones e indicadores",
             "Mensual y por evento",
             "Registro documental y reporte de indicadores"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT] * 4,
        title="Tabla 5. Matriz de comunicación de Nova Eventos.",
        note="Elaboración propia a partir de Robbins y Judge (2018).",
    )
    set_col_widths(tabla, [3.2, 4.8, 3.0, 5.0])
    add_items(doc, [
        ("Estandarización del lenguaje: ",
         "cotizaciones, contratos, cronogramas y listas de control con formatos "
         "únicos, de modo que cliente, personal y proveedores compartan el mismo "
         "vocabulario y se reduzcan los malentendidos."),
        ("Presencia multicanal: ",
         "catálogo digital, redes sociales, WhatsApp y correo, sin depender de una "
         "sola plataforma; en Bolivia se estimaron 8,77 millones de usuarios de "
         "internet al inicio de 2025 (DataReportal, 2025)."),
        ("Bucles de retroalimentación: ",
         "encuesta de satisfacción tras cada evento y revisión mensual de "
         "indicadores para detectar y corregir desviaciones tempranamente."),
        ("Comunicación interna y externa: ",
         "metas y procedimientos hacia el personal (descendente), reportes de avance "
         "e incidencias hacia la administración (ascendente) y difusión de "
         "portafolio y políticas hacia clientes y proveedores (externa)."),
    ])

    # ---------------------------------------------------------------- 4
    h2(doc, '4. Ejemplo Práctico de Implementación')

    h3(doc, '4.1 Caso Ilustrativo')
    add_parrafo(doc,
        "Para comprender la utilidad del plan, considérese el siguiente caso. Una "
        "cliente de 24 años desea organizar una fiesta de graduación temática para "
        "40 invitados con un presupuesto aproximado de Bs 3.000. El proceso se "
        "inicia con un contacto por WhatsApp y una consulta de necesidades (ocasión, "
        "asistentes, temática, fecha y presupuesto). Con esa información, el equipo "
        "elabora una propuesta visual y cotiza el paquete Nova Plus (Bs 3.500), "
        "desglosando servicios incluidos y opcionales; la cliente ajusta algunas "
        "partidas y aprueba un presupuesto de Bs 3.200 mediante contrato escrito.")
    add_parrafo(doc,
        "Durante la preparación, el cronograma y el tablero digital del evento se "
        "comparten con la cliente y los proveedores, quienes confirman horarios y "
        "responsabilidades. El día del evento se aplica la lista de control previa "
        "(contrato, diseño, seguridad, proveedores y materiales) y se designa un "
        "responsable de incidencias. Finalmente, se envía la encuesta de "
        "satisfacción, cuyo resultado se registra para la meta de 4,5 / 5 y para la "
        "revisión mensual de indicadores.")
    add_parrafo(doc,
        "Cada contratación de este tipo contribuye a la meta de 12 contratos "
        "pagados en seis meses y, en términos de la matriz BCG, valida o descarta la "
        "inversión en el servicio clasificado como signo de interrogación. La "
        "comunicación estructurada reduce reclamos por cambios de última hora y "
        "mantiene a cliente, personal y proveedores informados con la misma "
        "información.")

    h3(doc, '4.2 Cronograma de Implementación')
    add_parrafo(doc,
        "La implementación se distribuye en un periodo de seis meses que comprende "
        "investigación, diseño, preparación, prueba piloto, lanzamiento y "
        "evaluación:")
    tabla = add_table_with_data(
        doc,
        ["Actividad", "Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"],
        [
            ["Investigación de mercado", "X", "", "", "", "", ""],
            ["Diseño de paquetes", "", "X", "X", "", "", ""],
            ["Selección de proveedores", "", "X", "X", "", "", ""],
            ["Material comercial", "", "", "X", "X", "", ""],
            ["Capacitación y procedimientos", "", "", "X", "", "", ""],
            ["Eventos piloto", "", "", "", "X", "X", ""],
            ["Lanzamiento comercial", "", "", "", "", "X", "X"],
            ["Seguimiento de ventas", "", "", "", "", "X", "X"],
            ["Evaluación de resultados", "", "", "", "", "", "X"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT] + [WD_ALIGN_PARAGRAPH.CENTER] * 6,
        title="Tabla 6. Cronograma de implementación de Nova Experience.",
    )
    set_col_widths(tabla, [4.6, 1.88, 1.88, 1.88, 1.88, 1.88, 1.88])

    h3(doc, '4.3 Presupuesto y Punto de Equilibrio')
    add_parrafo(doc,
        "El lanzamiento requiere una inversión inicial estimada de Bs 9.350:")
    tabla = add_table_with_data(
        doc,
        ["N.°", "Concepto", "Costo estimado (Bs)"],
        [
            ["1", "Investigación de mercado y encuestas", "600"],
            ["2", "Diseño de identidad visual y material comercial", "700"],
            ["3", "Catálogo digital y portafolio", "500"],
            ["4", "Promoción digital de lanzamiento", "900"],
            ["5", "Capacitación del personal", "600"],
            ["6", "Materiales decorativos reutilizables", "1.800"],
            ["7", "Herramientas de planificación y administración", "400"],
            ["8", "Ejecución de eventos piloto", "2.000"],
            ["9", "Revisión administrativa y contractual", "500"],
            ["10", "Transporte, coordinación y logística inicial", "500"],
            ["", "Subtotal", "8.500"],
            ["", "Contingencia del 10 %", "850"],
            ["", "INVERSIÓN INICIAL ESTIMADA", "9.350"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
                        WD_ALIGN_PARAGRAPH.CENTER],
        title="Tabla 7. Presupuesto de implementación.",
        note="Estimaciones académicas en bolivianos; no constituyen cotizaciones "
             "comerciales verificadas.",
    )
    set_col_widths(tabla, [1.2, 10.8, 4.0])
    add_parrafo(doc,
        "Con un margen de contribución supuesto del 40 %, el punto de equilibrio "
        "en ingresos sería:")
    add_formula(doc,
        "Punto de equilibrio = Inversión inicial / Margen de contribución")
    add_formula(doc,
        "Punto de equilibrio = Bs 9.350 / 0,40 = Bs 23.375")
    add_parrafo(doc,
        "Este cálculo es una aproximación para la planificación inicial y no "
        "sustituye un análisis financiero basado en costos reales.")

    h3(doc, '4.4 Indicadores de Seguimiento y Monitoreo')
    add_parrafo(doc,
        "El seguimiento se apoya en indicadores con meta y frecuencia definidas:")
    tabla = add_table_with_data(
        doc,
        ["Indicador", "Meta inicial", "Frecuencia de evaluación"],
        [
            ["Encuestas completadas", "100 respuestas exploratorias",
             "Una vez, durante el primer mes"],
            ["Proveedores aliados", "Al menos 5", "Mensual"],
            ["Eventos piloto", "Al menos 3", "Al finalizar cada evento"],
            ["Contratos pagados acumulados", "12 en seis meses", "Mensual"],
            ["Satisfacción del cliente", "Promedio mínimo de 4,5 / 5",
             "Después de cada evento"],
            ["Cumplimiento del cronograma", "Al menos 90 %",
             "Después de cada evento"],
            ["Personal capacitado", "100 % del equipo involucrado",
             "Antes del lanzamiento"],
            ["Desviación presupuestaria", "Seguimiento de cada evento",
             "Por evento"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
                        WD_ALIGN_PARAGRAPH.CENTER],
        title="Tabla 8. Indicadores de control estratégico.",
    )
    set_col_widths(tabla, [5.2, 5.8, 5.0])
    add_parrafo(doc,
        "La administración revisará mensualmente los resultados comerciales y "
        "financieros. Cuando un indicador quede por debajo de la meta, deberá "
        "identificar la causa, proponer una medida correctiva y establecer un plazo "
        "para verificar su efectividad. Por ejemplo, si las consultas son muchas "
        "pero los contratos pocos, corresponde revisar los precios, la claridad de "
        "las cotizaciones y la adecuación de los paquetes a las necesidades del "
        "mercado.")

    h3(doc, '4.5 Gestión del Cambio')
    add_parrafo(doc,
        "La implementación de Nova Experience también exige gestionar la resistencia "
        "al cambio del personal y de los proveedores, quienes pueden preferir los "
        "procedimientos habituales (Kotter, 1996). Para ello, la empresa seguirá "
        "cinco etapas:")
    add_items(doc, [
        ("Comunicación: ",
         "explicar por qué la empresa amplía su oferta y qué beneficios se esperan."),
        ("Participación: ",
         "el equipo y los proveedores principales proponen mejoras antes del "
         "lanzamiento."),
        ("Capacitación: ",
         "uso de cotizaciones estandarizadas, cronogramas y listas de control."),
        ("Prueba piloto: ",
         "eventos de alcance limitado para detectar errores antes de escalar."),
        ("Evaluación y consolidación: ",
         "revisar resultados, corregir deficiencias y fijar los procedimientos "
         "útiles."),
    ])
    add_parrafo(doc,
        "El avance se medirá con el porcentaje de personal capacitado (meta inicial: "
        "100 %), el número de incidencias relacionadas con los nuevos procedimientos "
        "y el porcentaje de tareas realizadas según el proceso establecido.")

    # ---------------------------------------------------------------- 5
    h2(doc, '5. Conclusión')
    add_parrafo(doc,
        "La aplicación de la planificación estratégica a Nova Eventos demuestra que "
        "los temas investigados no son teoría aislada: los objetivos estratégicos "
        "convirtieron la visión de la empresa en ocho metas concretas y medibles que "
        "orientan decisiones diarias; la matriz BCG permitió priorizar dónde "
        "invertir el presupuesto limitado, favoreciendo el nuevo servicio con "
        "potencial de crecimiento; y las estrategias de comunicación ordenaron la "
        "información entre cliente, proveedores y personal.")
    add_parrafo(doc,
        "Entre los beneficios prácticos se encuentran decisiones basadas en análisis "
        "y no en intuición, el uso eficiente de una inversión inicial de Bs 9.350, "
        "la alineación del equipo mediante indicadores compartidos y la "
        "retroalimentación temprana a través de encuestas y revisiones mensuales. "
        "Además, el enfoque incremental —prueba piloto antes de escalar— reduce el "
        "riesgo financiero y operativo del proyecto.")
    add_parrafo(doc,
        "En síntesis, aplicar el tema en la empresa aporta dirección, priorización y "
        "control. No obstante, su utilidad depende de que los supuestos del plan se "
        "validen con investigación de mercado y cotizaciones reales, de modo que la "
        "estrategia se ajuste a la evidencia obtenida durante la implementación.")

    agregar_referencias(doc, [
        "DataReportal. (2025). Digital 2025: Bolivia. "
        "https://datareportal.com/reports/digital-2025-bolivia",
        "David, F. R., David, F. R., & David, M. E. (2020). Strategic Management: A "
        "Competitive Advantage Approach, Concepts and Cases (17.ª ed.). Pearson.",
        "Henderson, B. D. (1970). The Product Portfolio. Boston Consulting Group "
        "Perspectives, No. 66.",
        "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard: Translating "
        "Strategy into Action. Harvard Business School Press.",
        "Kotler, P., & Keller, K. L. (2016). Marketing Management (15.ª ed.). "
        "Pearson Education.",
        "Kotter, J. P. (1996). Leading Change. Harvard Business School Press.",
        "Robbins, S. P., & Judge, T. A. (2018). Organizational Behavior (18.ª ed.). "
        "Pearson Education.",
    ])

    salida = os.path.join(AQUI, SALIDA_IMP)
    doc.save(salida)
    print("Documento generado:", salida)


if __name__ == "__main__":
    generar_investigacion()
    generar_implementacion()
