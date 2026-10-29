# -*- coding: utf-8 -*-
"""Genera el informe .docx del Unit Testing de las 5 funciones criticas."""
import os
import sys

sys.path.insert(0, "/home/eynor/Documents/biblioteca-Skills/skills")

from base_documento import (  # noqa: E402
    crear_documento,
    configurar_estilos,
    add_paragraph,
    add_heading_custom,
    add_bullets,
    add_table_with_data,
    agregar_toc,
    agregar_referencias,
    agregar_nueva_seccion,
    configurar_header,
    configurar_primer_header_vacio,
    Cm,
    Pt,
    RGBColor,
    WD_ALIGN_PARAGRAPH,
    set_cell_text,
)
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = "/home/eynor/Documents/semestr7/Testing /hito3/att/appTesting"
CAPTURAS = os.path.join(AQUI, "capturas")
LOGO = "/home/eynor/Documents/biblioteca-Skills/logoUnifranz/logounifranz.png"

TITULO = ("UNIT TESTING DE LAS FUNCIONES CRÍTICAS DEL SISTEMA DE "
          "PRODUCTOS Y VENTAS")
AUTOR = "BRAYAN QUISPE MAMANI"
ASIGNATURA = "TESTING DE SOFTWARE"
DOCENTE = "NELSON CRISTHIAN URUCHI QUISPE"
ANIO = "2026"


# ---------------------------------------------------------------- utilidades
def leer(archivo):
    with open(os.path.join(RAIZ_PROYECTO, archivo), encoding="utf-8") as archivo_abierto:
        return archivo_abierto.read()


def extraer(texto, inicio, fin=None):
    i = texto.index(inicio)
    if fin is None:
        return texto[i:].rstrip()
    j = texto.index(fin, i + len(inicio))
    return texto[i:j].rstrip()


def linea_centrada(doc, texto, size=12, bold=False, space_after=0, space_before=0):
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    return p


def agregar_caratula(doc, titulo, autor, asignatura, docente):
    linea_centrada(doc, "UNIVERSIDAD PRIVADA FRANZ TAMAYO", size=14, bold=True)
    linea_centrada(doc, "SEDE EL ALTO", size=14, bold=True)
    linea_centrada(doc, "FACULTAD DE INGENIERÍA", size=14, bold=True)
    linea_centrada(doc, "CARRERA DE INGENIERÍA DE SISTEMAS", size=14, bold=True,
                   space_after=18)
    linea_centrada(doc, titulo, size=14, bold=True, space_before=10, space_after=18)
    linea_centrada(doc, f"AUTOR: {autor}", size=12)
    linea_centrada(doc, f"ASIGNATURA: {asignatura}", size=12)
    linea_centrada(doc, "DOCENTE:", size=12, space_before=10)
    linea_centrada(doc, docente, size=12, space_after=12)
    if os.path.exists(LOGO):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.first_line_indent = Cm(0)
        p_logo.paragraph_format.space_after = Pt(12)
        p_logo.add_run().add_picture(LOGO, width=Cm(6.04), height=Cm(5.73))
    linea_centrada(doc, "EL ALTO – BOLIVIA", size=12, bold=True)
    linea_centrada(doc, ANIO, size=12, bold=True)


def add_codigo(doc, texto, size=8.0):
    for linea in texto.split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(linea if linea else " ")
        run.font.name = 'Courier New'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0, 0, 0)


def add_figura(doc, archivo, pie, ancho_cm=15.5):
    ruta = os.path.join(CAPTURAS, archivo)
    if os.path.exists(ruta):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_after = Pt(4)
        p.add_run().add_picture(ruta, width=Cm(ancho_cm))
    add_paragraph(doc, pie, italic=True, size=10,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)


def tabla_casos(doc, titulo, filas):
    add_table_with_data(
        doc,
        ["Caso de prueba", "Arrange (entrada / estado)", "Act (acción)",
         "Assert (resultado esperado)", "Estado"],
        filas,
        title=titulo,
        note="Estado: PASA = la aserción se cumplió en la ejecución real de pytest.",
    )


# ---------------------------------------------------------------- documento
def main():
    doc = crear_documento()
    configurar_estilos(doc)

    configurar_header(doc, doc.sections[0], mostrar=False)
    agregar_caratula(doc, TITULO, AUTOR, ASIGNATURA, DOCENTE)

    agregar_nueva_seccion(doc, fmt='upperRoman', start=1, mostrar=True)
    agregar_toc(doc)

    agregar_nueva_seccion(doc, fmt='decimal', start=1, mostrar=True)

    # ================================================================
    # 0. INSTRUCCION Y RUBRICA
    # ================================================================
    add_heading_custom(doc, 'Instrucción de la tarea y rúbrica de evaluación', level=2)
    add_paragraph(doc,
        "Analizar y elaborar los Unit Test de 5 funciones (las más críticas) "
        "dentro del sistema que está desarrollando para su proyecto integrador. "
        "Para cada caso, debe presentar: Arrange, Act y Assert, el código de su "
        "función o método, el código de sus pruebas y sus respectivas capturas.")
    add_bullets(doc, [
        "Modalidad: individual.",
        "Formato de presentación: documento en PDF, describiendo claramente cada "
        "punto instruido.",
        "Retroalimentación: en plataforma.",
        "Recuerde que se penaliza (5% por día) la entrega con retraso.",
    ])
    add_table_with_data(
        doc,
        ["Criterio evaluado", "Peso", "Sección donde se cumple"],
        [
            ["1. Justifica técnicamente la criticidad de sus funciones frente a "
             "otras de menor criticidad.", "20%", "Sección 2"],
            ["2. Comparte el código de las funciones a probar.", "20%", "Sección 3"],
            ["3. Comparte el código de sus Unit Test, con Assert.", "20%", "Sección 4"],
            ["4. Identifica los casos de prueba (Arrange), obtiene sus respuestas "
             "(Act) y realiza la comparación (Assert).", "20%", "Sección 5"],
            ["5. Demuestra el funcionamiento de sus pruebas mostrando capturas.",
             "15%", "Sección 6"],
            ["6. Documento ordenado, claramente identificable en cada punto y con "
             "ortografía impecable.", "5%", "Todo el documento"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER,
                        WD_ALIGN_PARAGRAPH.CENTER],
        title="Tabla A. Correspondencia entre la rúbrica y las secciones del informe.",
    )

    # ================================================================
    # 1. INTRODUCCION
    # ================================================================
    add_heading_custom(doc, '1. Introducción', level=2)
    add_paragraph(doc,
        "El presente informe documenta el diseño y la ejecución de pruebas "
        "unitarias sobre las cinco funciones más críticas del sistema de gestión "
        "de productos y ventas desarrollado como proyecto integrador. El sistema "
        "consiste en una API REST construida con Flask que administra productos, "
        "compradores, usuarios y ventas, con autenticación por roles y control de "
        "inventario.")
    add_paragraph(doc,
        "Una prueba unitaria aísla la unidad más pequeña de código (en este caso, "
        "una función o un método) y comprueba su comportamiento con entradas "
        "controladas, sin depender de la base de datos ni de servicios externos. "
        "Para ello se aplicó el patrón Arrange–Act–Assert: primero se prepara el "
        "escenario, luego se ejecuta la acción y finalmente se compara el resultado "
        "obtenido con el esperado.")

    add_heading_custom(doc, '1.1 Objetivo', level=3)
    add_paragraph(doc,
        "Analizar y elaborar las pruebas unitarias de las cinco funciones más "
        "críticas del sistema, justificando técnicamente su criticidad, presentando "
        "el código bajo prueba, el código de las pruebas y la evidencia de su "
        "ejecución satisfactoria.")

    add_heading_custom(doc, '1.2 Herramientas utilizadas', level=3)
    add_bullets(doc, [
        "Lenguaje: Python 3.14.",
        "Marco de pruebas: pytest (versión 9.1.1).",
        "Componentes simulados: dobles de prueba (fakes) y monkeypatch para aislar la base de datos.",
        "Cliente de pruebas de Flask (test_client) para las funciones de la capa web.",
        "Entorno: sistema operativo Linux.",
    ])

    # ================================================================
    # 2. JUSTIFICACION DE CRITICIDAD
    # ================================================================
    add_heading_custom(doc, '2. Justificación técnica de la criticidad', level=2)
    add_paragraph(doc,
        "No todas las funciones del sistema merecen el mismo esfuerzo de prueba. "
        "La criticidad de una función se evaluó con cuatro criterios técnicos: el "
        "impacto de un fallo (qué se pierde si la función se comporta mal), la "
        "frecuencia de uso (cuántas veces se ejecuta en la operación real), el "
        "acoplamiento (cuántas otras partes dependen de ella) y la dificultad de "
        "detección del error (si el fallo se manifiesta de inmediato o permanece "
        "oculto). Las cinco funciones seleccionadas concentran el mayor producto de "
        "estos cuatro criterios.")

    add_heading_custom(doc, '2.1 Matriz de criticidad', level=3)
    add_table_with_data(
        doc,
        ["Función", "Impacto del fallo", "Frecuencia", "Detección", "Criticidad"],
        [
            ["VentaRepository.registrar", "Pérdida de dinero e inventario inconsistente",
             "Muy alta", "Difícil", "Muy alta"],
            ["app.iniciar_sesion", "Acceso no autorizado y suplantación de identidad",
             "Muy alta", "Media", "Muy alta"],
            ["app.requiere_rol", "Escalada de privilegios entre roles",
             "Alta", "Media", "Muy alta"],
            ["validaciones.validar_precio", "Precios inválidos y totales de venta erróneos",
             "Alta", "Fácil", "Alta"],
            ["validaciones.validar_cantidad", "Sobregiro de stock y ventas nulas o negativas",
             "Alta", "Fácil", "Alta"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT] * 5,
        title="Tabla 1. Matriz de criticidad de las funciones analizadas.",
    )

    add_heading_custom(doc, '2.2 VentaRepository.registrar', level=3)
    add_paragraph(doc,
        "Es la función más crítica del sistema porque concentra la lógica de "
        "negocio en una sola transacción: bloquea al comprador y al producto, "
        "valida el stock disponible, descuenta el inventario, calcula el total con "
        "aritmética decimal y registra la venta. Si falla, o se cobra un monto "
        "incorrecto o se descuenta stock sin dejar constancia de la venta. Además, "
        "su acoplamiento es máximo: depende de las tablas de productos, "
        "compradores, usuarios y ventas, y su error no aparece de inmediato, sino "
        "cuando el inventario ya no cuadra.")

    add_heading_custom(doc, '2.3 app.iniciar_sesion', level=3)
    add_paragraph(doc,
        "Es la puerta de entrada al sistema. Verifica que el usuario exista, que la "
        "cuenta esté activa y que la contraseña coincida con su hash antes de crear "
        "la sesión. Un fallo aquí permitiría el ingreso con credenciales "
        "incorrectas o la suplantación de otro rol, por lo que su impacto es de "
        "seguridad y afecta a todos los módulos posteriores.")

    add_heading_custom(doc, '2.4 app.requiere_rol', level=3)
    add_paragraph(doc,
        "Es el control de autorización del lado del servidor. Envuelve cada "
        "endpoint protegido y decide si el usuario autenticado puede ejecutar la "
        "operación. Su criticidad es transversal: si el decorador falla, un "
        "vendedor podría eliminar productos, crear usuarios o ver información "
        "reservada al administrador. La validación en el cliente no sustituye este "
        "control, de modo que es la última línea de defensa.")

    add_heading_custom(doc, '2.5 validaciones.validar_precio y validar_cantidad', level=3)
    add_paragraph(doc,
        "Ambas funciones son la primera barrera de integridad de datos. "
        "validar_precio impide que un producto se registre con precio nulo, "
        "negativo, infinito o desmesurado, y valida_cantidad impide vender cero, "
        "negativos o cantidades que desbordan el inventario. Su detección es más "
        "sencilla, por eso su criticidad se clasifica como alta y no como muy alta, "
        "pero se incluyen porque alimentan directamente a las tres funciones "
        "anteriores.")

    add_heading_custom(doc, '2.6 Funciones de menor criticidad descartadas', level=3)
    add_paragraph(doc,
        "Quedaron fuera del alcance funciones como index, serializar, "
        "datos_publicos, los métodos listar y obtener de los repositorios, y "
        "validar_descripcion. Se trata de funciones de presentación o de simple "
        "consulta: no transforman datos financieros ni decisiones de seguridad, y "
        "un error en ellas produce un resultado visible de inmediato que no "
        "compromete la integridad del sistema. Esa diferencia de impacto es, "
        "precisamente, la que justifica concentrar las pruebas unitarias en las "
        "cinco funciones seleccionadas.")

    # ================================================================
    # 3. CODIGO DE LAS FUNCIONES
    # ================================================================
    add_heading_custom(doc, '3. Código de las funciones a probar', level=2)
    add_paragraph(doc,
        "A continuación se presenta el código fuente de cada función bajo prueba, "
        "extraído de los archivos validaciones.py, models.py y app.py del proyecto.")

    fuente_validaciones = leer("validaciones.py")
    fuente_models = leer("models.py")
    fuente_app = leer("app.py")

    codigo_precio = extraer(fuente_validaciones, "def validar_precio(", "def validar_cantidad(")
    codigo_cantidad = extraer(fuente_validaciones, "def validar_cantidad(", "def validar_unidad_medida(")
    codigo_registrar = extraer(fuente_models, "    def registrar(", "    def listar(")
    codigo_login = extraer(
        fuente_app,
        '@app.route("/api/sesion", methods=["POST"])',
        '@app.route("/api/sesion", methods=["DELETE"])',
    )
    codigo_rol = extraer(fuente_app, "def requiere_rol(", "def datos_publicos(")

    add_heading_custom(doc, '3.1 validaciones.validar_precio', level=3)
    add_codigo(doc, codigo_precio)

    add_heading_custom(doc, '3.2 validaciones.validar_cantidad', level=3)
    add_codigo(doc, codigo_cantidad)

    add_heading_custom(doc, '3.3 models.VentaRepository.registrar', level=3)
    add_codigo(doc, codigo_registrar)

    add_heading_custom(doc, '3.4 app.iniciar_sesion', level=3)
    add_codigo(doc, codigo_login)

    add_heading_custom(doc, '3.5 app.requiere_rol', level=3)
    add_codigo(doc, codigo_rol)

    # ================================================================
    # 4. CODIGO DE LOS UNIT TESTS
    # ================================================================
    add_heading_custom(doc, '4. Código de los Unit Tests', level=2)
    add_paragraph(doc,
        "Las pruebas se agruparon en el archivo test_funciones_criticas.py. Cada "
        "función se aísla con dobles de prueba (fakes) cuando depende de la base de "
        "datos, y con el cliente de pruebas de Flask cuando depende del contexto "
        "web. En todos los casos el escenario se prepara en la sección marcada como "
        "Arrange, la acción se ejecuta en Act y la comparación se realiza en "
        "Assert.")

    fuente_tests = open(os.path.join(AQUI, "test_funciones_criticas.py"),
                        encoding="utf-8").read()

    add_heading_custom(doc, '4.1 Pruebas de validar_precio (5 casos)', level=3)
    add_codigo(doc, extraer(fuente_tests, "def test_validar_precio_convierte", "\n# ===="))

    add_heading_custom(doc, '4.2 Pruebas de validar_cantidad (5 casos)', level=3)
    add_codigo(doc, extraer(fuente_tests, "def test_validar_cantidad_positiva", "\n# ===="))

    add_heading_custom(doc, '4.3 Pruebas de VentaRepository.registrar (5 casos)', level=3)
    add_codigo(doc, extraer(fuente_tests, "class CursorFake:", "\n# ===="))

    add_heading_custom(doc, '4.4 Pruebas de iniciar_sesion (5 casos)', level=3)
    add_codigo(doc, extraer(fuente_tests, "class UsuariosFake:", "\n# ===="))

    add_heading_custom(doc, '4.5 Pruebas de requiere_rol (5 casos)', level=3)
    add_codigo(doc, extraer(fuente_tests, "def app_con_permisos():"))

    # ================================================================
    # 5. CASOS DE PRUEBA (ARRANGE - ACT - ASSERT)
    # ================================================================
    add_heading_custom(doc, '5. Casos de prueba: Arrange, Act y Assert', level=2)
    add_paragraph(doc,
        "Para cada función se identificaron cinco casos de prueba. La columna "
        "Arrange describe la preparación de la entrada o del estado; la columna Act "
        "indica la acción ejecutada; la columna Assert muestra la respuesta "
        "esperada y comparada por la prueba.")

    add_heading_custom(doc, '5.1 Casos de validar_precio', level=3)
    tabla_casos(doc, "Tabla 2. Casos de prueba de validar_precio.", [
        ["1", "entrada = 10.999", "validar_precio(10.999)", "devuelve 11.0", "PASA"],
        ["2", "entrada = \"1500.50\"", "validar_precio(\"1500.50\")", "devuelve 1500.50", "PASA"],
        ["3", "entrada ∈ {0, −100, −0.01}", "validar_precio(valor)", "lanza ValueError", "PASA"],
        ["4", "entrada ∈ {\"abc\", None, inf, nan}", "validar_precio(valor)", "lanza ValueError", "PASA"],
        ["5", "entrada = 99999999.99 y 100000000", "validar_precio(...)", "acepta el límite y rechaza el exceso", "PASA"],
    ])

    add_heading_custom(doc, '5.2 Casos de validar_cantidad', level=3)
    tabla_casos(doc, "Tabla 3. Casos de prueba de validar_cantidad.", [
        ["1", "entrada = \"0.250\"", "validar_cantidad(\"0.250\")", "devuelve 0.25", "PASA"],
        ["2", "entrada = 0 (permitir_cero=True)", "validar_cantidad(0, permitir_cero=True)", "devuelve 0.0", "PASA"],
        ["3", "entrada = 0 (permitir_cero=False)", "validar_cantidad(0)", "lanza ValueError", "PASA"],
        ["4", "entrada ∈ {−1, True, None}", "validar_cantidad(valor)", "lanza ValueError", "PASA"],
        ["5", "entrada = nan y 1000000000", "validar_cantidad(valor)", "lanza ValueError", "PASA"],
    ])

    add_heading_custom(doc, '5.3 Casos de VentaRepository.registrar', level=3)
    tabla_casos(doc, "Tabla 4. Casos de prueba de VentaRepository.registrar.", [
        ["1", "stock 4.250 kg, precio 2.35, venta 1.25", "registrar(7, 3, 1.25, 12)",
         "total 2.94; stock 3.000; 1 commit y 0 rollback", "PASA"],
        ["2", "precio 1.00, cantidad 1.005", "registrar(7, 3, 1.005, 12)",
         "total 1.01 (redondeo HALF_UP)", "PASA"],
        ["3", "stock 4.250 kg, venta 5", "registrar(7, 3, 5, 12)",
         "lanza StockInsuficiente; stock intacto; 1 rollback", "PASA"],
        ["4", "producto inexistente (id 999)", "registrar(999, 3, 1, 12)",
         "lanza ProductoNoEncontrado; 1 rollback", "PASA"],
        ["5", "comprador inexistente (id 999)", "registrar(7, 3, 1, 999)",
         "lanza CompradorNoEncontrado; 1 rollback", "PASA"],
    ])

    add_heading_custom(doc, '5.4 Casos de iniciar_sesion', level=3)
    tabla_casos(doc, "Tabla 5. Casos de prueba de iniciar_sesion.", [
        ["1", "usuario admin activo", "POST /api/sesion", "200; perfil \"Gerente\"; sesión creada", "PASA"],
        ["2", "correo \"  ADMIN@Test.Local  \"", "POST /api/sesion", "200; rol admin (correo normalizado)", "PASA"],
        ["3", "correo inexistente / clave errónea", "POST /api/sesion", "401 en ambos casos", "PASA"],
        ["4", "usuario con activo = False", "POST /api/sesion", "401", "PASA"],
        ["5", "contrasena = 12345678 (no texto)", "POST /api/sesion", "400", "PASA"],
    ])

    add_heading_custom(doc, '5.5 Casos de requiere_rol', level=3)
    tabla_casos(doc, "Tabla 6. Casos de prueba de requiere_rol.", [
        ["1", "sin sesión iniciada", "GET /solo-admin", "401 \"Debes iniciar sesión\"", "PASA"],
        ["2", "sesión con rol vendedor", "GET /solo-admin", "403", "PASA"],
        ["3", "sesión con rol admin", "GET /solo-admin", "200", "PASA"],
        ["4", "sesión con rol vendedor", "GET /admin-o-vendedor", "200", "PASA"],
        ["5", "sesión con rol compras", "GET /cualquier-rol", "200", "PASA"],
    ])

    # ================================================================
    # 6. EVIDENCIAS
    # ================================================================
    add_heading_custom(doc, '6. Evidencia de ejecución', level=2)
    add_paragraph(doc,
        "Las siguientes capturas corresponden a la ejecución real de la suite de "
        "pruebas con pytest. En total se ejecutaron 25 casos y todos resultaron "
        "exitosos (25 passed).")

    add_figura(doc, "captura_01_suite_completa.png",
               "Figura 1. Ejecución completa de la suite: 25 casos exitosos.", ancho_cm=15.5)
    add_figura(doc, "captura_02_validar_precio.png",
               "Figura 2. Pruebas de validar_precio: 5 casos exitosos.", ancho_cm=15.5)
    add_figura(doc, "captura_03_validar_cantidad.png",
               "Figura 3. Pruebas de validar_cantidad: 5 casos exitosos.", ancho_cm=15.5)
    add_figura(doc, "captura_04_venta_registrar.png",
               "Figura 4. Pruebas de VentaRepository.registrar: 5 casos exitosos.", ancho_cm=15.5)
    add_figura(doc, "captura_05_iniciar_sesion.png",
               "Figura 5. Pruebas de iniciar_sesion: 5 casos exitosos.", ancho_cm=15.5)
    add_figura(doc, "captura_06_requiere_rol.png",
               "Figura 6. Pruebas de requiere_rol: 5 casos exitosos.", ancho_cm=15.5)

    # ================================================================
    # 7. CONCLUSIONES
    # ================================================================
    add_heading_custom(doc, '7. Conclusiones', level=2)
    add_points = [
        "Las cinco funciones seleccionadas cubren el negocio transaccional, la "
        "entrada del dinero, el control de inventario y la seguridad de acceso, "
        "que son los puntos donde un error produce consecuencias reales.",
        "El patrón Arrange–Act–Assert permitió separar con claridad la preparación "
        "del escenario, la acción y la verificación, lo que hace que cada caso sea "
        "legible y repetible.",
        "El uso de dobles de prueba y de monkeypatch aisló por completo la base de "
        "datos, de modo que las pruebas unitarias se ejecutan de forma rápida y "
        "determinista.",
        "Los 25 casos se ejecutaron sin fallos, lo que confirma el comportamiento "
        "correcto de las funciones ante entradas válidas, entradas de frontera y "
        "situaciones de error.",
    ]
    add_bullets(doc, add_points)

    # ================================================================
    # 8. ANEXO
    # ================================================================
    add_heading_custom(doc, '8. Anexo. Código fuente en el editor', level=2)
    add_paragraph(doc,
        "Como evidencia adicional se incluyen capturas del código fuente abierto "
        "en el editor VSCodium. En ellas se observan la numeración de líneas y el "
        "resaltado de sintaxis de los archivos validaciones.py, models.py y app.py, "
        "así como del archivo de pruebas test_funciones_criticas.py.")

    add_figura(doc, "anexo_1_validaciones.png",
               "Figura A1. validaciones.py: funciones validar_precio y validar_cantidad.",
               ancho_cm=15.5)
    add_figura(doc, "anexo_2_models.png",
               "Figura A2. models.py: método VentaRepository.registrar (cálculo del "
               "total y actualización de stock).", ancho_cm=15.5)
    add_figura(doc, "anexo_3_app_roles.png",
               "Figura A3. app.py: decorador requiere_rol.", ancho_cm=15.5)
    add_figura(doc, "anexo_4_app_login.png",
               "Figura A4. app.py: función iniciar_sesion.", ancho_cm=15.5)
    add_figura(doc, "anexo_5_tests.png",
               "Figura A5. test_funciones_criticas.py: casos de prueba de validar_precio.",
               ancho_cm=15.5)

    agregar_referencias(doc, [
        "Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.",
        "Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2.ª ed.). O'Reilly Media.",
        "Kaner, C., Falk, J. y Nguyen, H. Q. (1999). Testing Computer Software (2.ª ed.). Wiley.",
        "Pressman, R. S. (2014). Ingeniería del software: un enfoque práctico (9.ª ed.). McGraw-Hill.",
        "pytest. (2024). pytest documentation. https://docs.pytest.org",
    ])

    salida = os.path.join(AQUI, "Informe_Unit_Testing_Funciones_Criticas.docx")
    doc.save(salida)
    print("Documento generado:", salida)


if __name__ == "__main__":
    main()
