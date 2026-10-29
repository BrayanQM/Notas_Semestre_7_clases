import os
import sys

sys.path.insert(0, "/home/eynor/Documents/biblioteca-Skills/skills")

from base_documento import (
    crear_documento,
    configurar_estilos,
    add_paragraph,
    add_heading_custom,
    add_bullets,
    add_code_block,
    add_table_with_data,
    add_image_placeholder,
    configurar_header,
    agregar_nueva_seccion,
    Cm,
    Pt,
    RGBColor,
    WD_ALIGN_PARAGRAPH,
)

BASE_DIR = "/home/eynor/Documents/semestr7/Testing /hito3/att"
CARPETA_CAPTURAS = os.path.join(BASE_DIR, "capturas")
LOGO = "/home/eynor/Documents/biblioteca-Skills/logoUnifranz/logounifranz.png"

TITULO = "PRUEBAS DE LOGIN VÍA API, SELENIUM Y CYPRESS"
INTEGRANTE = "BRAYAN QUISPE MAMANI"
ASIGNATURA = "TESTING DE SOFTWARE"
DOCENTE = "NELSON CRISTHIAN URUCHI QUISPE"


def centrado(doc, texto, size=12, bold=False, space_before=0, space_after=0):
    return add_paragraph(
        doc, texto, bold=bold, size=size,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=space_before, space_after=space_after,
        first_line_indent=0,
    )


def agregar_caratula(doc):
    doc.add_paragraph()
    centrado(doc, "UNIVERSIDAD PRIVADA FRANZ TAMAYO", size=15, bold=True)
    centrado(doc, "SEDE EL ALTO", size=14, bold=True)
    centrado(doc, "FACULTAD DE INGENIERÍA", size=14, bold=True)
    centrado(doc, "CARRERA DE INGENIERÍA DE SISTEMAS", size=14, bold=True,
             space_after=14)
    centrado(doc, f"ASIGNATURA: {ASIGNATURA}", size=12, bold=True,
             space_after=20)

    if os.path.exists(LOGO):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_after = Pt(24)
        p.add_run().add_picture(LOGO, width=Cm(6.5), height=Cm(6.17))

    centrado(doc, f'"{TITULO}"', size=14, bold=True,
             space_before=12, space_after=28)
    centrado(doc, f"INTEGRANTE: {INTEGRANTE}", size=12)
    centrado(doc, f"DOCENTE: {DOCENTE}", size=12, space_after=24)
    doc.add_paragraph()
    centrado(doc, "EL ALTO - BOLIVIA", size=12, bold=True)
    centrado(doc, "2026", size=12, bold=True)


def add_figura(doc, nombre_archivo, pie, ancho_cm=15.5):
    ruta = os.path.join(CARPETA_CAPTURAS, nombre_archivo)
    if os.path.exists(ruta):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)
        p.add_run().add_picture(ruta, width=Cm(ancho_cm))
    else:
        add_image_placeholder(doc, f"[FALTA CAPTURA: {nombre_archivo}]")
    add_paragraph(doc, pie, italic=True, size=10,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=0)


def add_subtitulo(doc, texto):
    return add_paragraph(doc, texto, bold=True, size=12,
                         space_before=6, space_after=2, first_line_indent=0)


def main():
    doc = crear_documento()
    configurar_estilos(doc)

    # ---- Sección 1: Carátula (sin numeración) ----
    configurar_header(doc, doc.sections[0], mostrar=False)
    agregar_caratula(doc)

    # ---- Sección 2: Cuerpo (numeración arábiga desde 1) ----
    agregar_nueva_seccion(doc, fmt="decimal", start=1, mostrar=True)

    # ================= ÍNDICE =================
    add_heading_custom(doc, "Índice", level=2)
    indice = [
        "1. Introducción y objetivo de la práctica",
        "2. Fundamentación teórica",
        "3. Preparación del entorno local",
        "4. Punto 1: Procedimiento para ejecutar el login vía API",
        "5. Punto 2: Procedimiento para ejecutar el login vía Selenium",
        "6. Punto 3: Procedimiento para ejecutar el login vía Cypress",
        "7. Resultados y evidencias (capturas)",
        "8. Dificultades encontradas",
        "9. Conclusiones",
        "10. Anexos",
    ]
    add_bullets(doc, indice)

    # ================= 1. INTRODUCCIÓN =================
    add_heading_custom(doc, "1. Introducción y objetivo de la práctica", level=2)
    add_paragraph(doc,
                  "El presente informe documenta la ejecución de pruebas automatizadas sobre "
                  "el inicio de sesión (login) del sistema de prueba appTesting. El sistema es "
                  "una aplicación web desarrollada con Flask que se apoya en una base de datos "
                  "MariaDB y que expone tanto una interfaz gráfica como una API REST. El objetivo "
                  "de la práctica es levantar el sistema de forma local y verificar el login "
                  "mediante tres herramientas distintas: una prueba de API, una prueba de "
                  "interfaz con Selenium y una prueba de interfaz con Cypress.")
    add_paragraph(doc,
                  "Las tres pruebas se ejecutan con la misma cuenta de prueba, cuyas credenciales "
                  "son el usuario pedrito@gmail.com y la contraseña bolivia123. De esta manera se "
                  "comprueba que el mismo caso de prueba es verificable desde distintos niveles "
                  "de la pirámide de automatización: la capa de servicios (API), y la capa de "
                  "interfaz de usuario (end-to-end).")
    add_paragraph(doc,
                  "Al final del informe se presentan las capturas que demuestran el funcionamiento "
                  "de cada prueba, tal como lo solicita la instrucción de la práctica.")

    # ================= 2. FUNDAMENTACIÓN =================
    add_heading_custom(doc, "2. Fundamentación teórica", level=2)
    add_paragraph(doc,
                  "Antes de describir los procedimientos conviene aclarar los conceptos y las "
                  "herramientas utilizadas en la práctica.")

    add_heading_custom(doc, "2.1 API REST y el endpoint de sesión", level=3)
    add_paragraph(doc,
                  "Una API REST es un estilo de arquitectura para servicios web que expone sus "
                  "operaciones a través del protocolo HTTP, usando los métodos GET, POST, PUT y "
                  "DELETE sobre recursos identificados por una URL, y cuyo cuerpo se intercambia "
                  "en formato JSON. El sistema appTesting define el recurso de sesión en la ruta "
                  "/api/sesion. El login por API consiste en enviar una petición POST con el "
                  "correo y la contraseña; el servidor busca al usuario, verifica la contraseña "
                  "contra su hash almacenado y, si todo es correcto, responde con código 200 y "
                  "los datos públicos del usuario.")

    add_heading_custom(doc, "2.2 Selenium", level=3)
    add_paragraph(doc,
                  "Selenium es una familia de herramientas para automatizar navegadores web. La "
                  "librería selenium-webdriver permite que un programa Python controle un "
                  "navegador real: abrir una página, localizar elementos por su identificador, "
                  "escribir texto en los campos, hacer clic en botones y esperar a que aparezcan "
                  "ciertas condiciones. La comunicación entre el código y el navegador se realiza "
                  "mediante un componente intermedio llamado chromedriver.")

    add_heading_custom(doc, "2.3 Cypress", level=3)
    add_paragraph(doc,
                  "Cypress es un framework de pruebas de extremo a extremo escrito en JavaScript "
                  "que se ejecuta dentro del mismo navegador donde vive la aplicación. Su API "
                  "encadenable, con métodos como cy.visit, cy.get y cy.type, permite describir el "
                  "recorrido del usuario de forma legible. Al igual que Selenium, comprueba el "
                  "resultado mediante aserciones, pero con la ventaja de que espera de forma "
                  "automática a que los elementos estén disponibles.")

    add_heading_custom(doc, "2.4 Flask, MariaDB y pytest", level=3)
    add_paragraph(doc,
                  "Flask es el microframework web con el que está construido el sistema: sirve "
                  "la interfaz HTML y expone la API REST. MariaDB es el motor de base de datos "
                  "relacional donde se guardan los usuarios, los productos y las ventas. pytest "
                  "es la herramienta de pruebas de Python que descubre y ejecuta los archivos de "
                  "prueba, y que en este caso también se usa para las pruebas de API y de "
                  "Selenium.")

    # ================= 3. ENTORNO =================
    add_heading_custom(doc, "3. Preparación del entorno local", level=2)
    add_paragraph(doc,
                  "Antes de ejecutar cualquier prueba se debe descargar el sistema y dejarlo "
                  "funcionando de forma local, junto con su base de datos.")

    add_heading_custom(doc, "3.1 Requisitos", level=3)
    add_bullets(doc, [
        "Sistema operativo Linux (en esta práctica se usó EndeavourOS).",
        "Python 3 y Node.js con npm instalados.",
        "Servidor MariaDB instalado y en ejecución.",
        "Un navegador basado en Chromium y su chromedriver para Selenium.",
    ])

    add_heading_custom(doc, "3.2 Descarga del repositorio", level=3)
    add_paragraph(doc, "Se clona el repositorio indicado en la instrucción:")
    add_code_block(doc, [
        "git clone https://github.com/CrisUruchi/appTesting",
        "cd appTesting",
    ])

    add_heading_custom(doc, "3.3 Base de datos", level=3)
    add_paragraph(doc,
                  "Se habilita e inicia el servidor MariaDB y luego se ejecuta el script "
                  "setup_db.sh, que recrea la base de datos crud_productos, habilita la conexión "
                  "de root sin contraseña (igual que db.py) y crea las tablas usuarios, "
                  "productos, ventas y compradores aplicando las migraciones del repositorio.")
    add_code_block(doc, [
        "sudo systemctl enable --now mariadb",
        "bash setup_db.sh",
    ])

    add_heading_custom(doc, "3.4 Entorno de Python y dependencias", level=3)
    add_paragraph(doc,
                  "Se crea un entorno virtual y se instalan las dependencias declaradas en "
                  "requirements.txt (Flask, mysql-connector-python, pytest, requests y selenium).")
    add_code_block(doc, [
        "python -m venv .venv",
        "source .venv/bin/activate",
        "pip install -r requirements.txt",
        "pip install webdriver-manager   # opcional, ayuda con el driver",
    ])

    add_heading_custom(doc, "3.5 Cuenta de prueba", level=3)
    add_paragraph(doc,
                  "Se crea una cuenta con perfil admin (gerente) para poder iniciar sesión. El "
                  "repositorio incluye el asistente crear_usuario.py, que pide nombre, correo, "
                  "perfil y contraseña, y guarda la contraseña como hash. En esta práctica la "
                  "cuenta creada fue pedrito@gmail.com con la contraseña bolivia123.")
    add_code_block(doc, [
        "python crear_usuario.py",
        "Nombre completo: Pedrito",
        "Correo: pedrito@gmail.com",
        "Perfil (admin/compras/vendedor): admin",
        "Contrasena (minimo 8 caracteres): bolivia123",
    ])

    add_heading_custom(doc, "3.6 Inicio del servidor", level=3)
    add_paragraph(doc,
                  "Finalmente se inicia la aplicación. Flask queda escuchando en "
                  "http://localhost:5000, que es la dirección que usan todas las pruebas.")
    add_code_block(doc, [
        "python app.py",
        "# * Running on http://127.0.0.1:5000",
    ])

    # ================= 4. API =================
    add_heading_custom(doc,
                       "4. Punto 1: Procedimiento para ejecutar el login vía API",
                       level=2)
    add_paragraph(doc,
                  "La prueba de login por API verifica el endpoint POST /api/sesion sin abrir "
                  "ningún navegador, únicamente con peticiones HTTP.")

    add_heading_custom(doc, "4.1 Descripción del endpoint", level=3)
    add_paragraph(doc,
                  "El endpoint recibe un cuerpo JSON con las claves correo y contrasena. Si las "
                  "credenciales son válidas, responde con código 200 y un objeto con los datos "
                  "públicos del usuario (nombre, correo y rol). Si el usuario no existe, está "
                  "inactivo o la contraseña no coincide, responde con código 401. El mismo "
                  "recurso admite GET para consultar la sesión activa y DELETE para cerrarla.")

    add_heading_custom(doc, "4.2 Código de la prueba", level=3)
    add_paragraph(doc,
                  "El archivo 4_test_api_productos.py define una fixture de sesión que inicia "
                  "el login una sola vez y conserva la cookie, y luego ejecuta quince casos de "
                  "prueba sobre los productos. El fragmento del login es el siguiente:")
    add_code_block(doc, [
        "def iniciar_sesion_api():",
        "    correo = os.environ.get(\"API_EMAIL\")",
        "    contrasena = os.environ.get(\"API_PASSWORD\")",
        "    if not correo or not contrasena:",
        "        pytest.skip(\"Configura API_EMAIL y API_PASSWORD\")",
        "    respuesta = requests.post(",
        "        f\"{BASE_URL}/api/sesion\",",
        "        json={\"correo\": correo, \"contrasena\": contrasena},",
        "        headers=HEADERS,",
        "    )",
        "    assert respuesta.status_code == 200",
    ], title="Fragmento: login por API (4_test_api_productos.py)")

    add_paragraph(doc,
                  "Además, se usó un pequeño script, api_login_demo.py, que hace el POST y luego "
                  "un GET a /api/sesion para mostrar la sesión activa de forma legible:")
    add_code_block(doc, [
        "respuesta = cliente.post(",
        "    f\"{BASE}/api/sesion\",",
        "    json={\"correo\": CORREO, \"contrasena\": CONTRASENA},",
        ")",
        "print(respuesta.status_code)",
        "print(respuesta.json())",
    ], title="Fragmento: api_login_demo.py")

    add_heading_custom(doc, "4.3 Procedimiento paso a paso", level=3)
    add_bullets(doc, [
        "Paso 1. Verificar que la aplicación esté corriendo en http://localhost:5000.",
        "Paso 2. Exportar las credenciales de la cuenta en variables de entorno.",
        "Paso 3. Ejecutar la prueba de API con pytest en modo detallado.",
        "Paso 4. Ejecutar el script api_login_demo.py para ver la respuesta del login.",
        "Paso 5. Observar que el estado devuelto es 200 y el perfil del usuario.",
    ])
    add_code_block(doc, [
        "export API_EMAIL=pedrito@gmail.com",
        "export API_PASSWORD=bolivia123",
        "python -m pytest 4_test_api_productos.py -v",
        "python api_login_demo.py",
    ])

    add_heading_custom(doc, "4.4 Resultado esperado", level=3)
    add_paragraph(doc,
                  "La prueba de API finaliza con quince casos aprobados y la sesión del usuario "
                  "pedrito@gmail.com se inicia correctamente con perfil Gerente. La evidencia se "
                  "muestra en la Figura 1.")

    add_figura(doc, "01_api_login.png",
               "Figura 1. Ejecución del login vía API: POST /api/sesion responde 200 y "
               "muestra la sesión activa de pedrito@gmail.com con perfil Gerente.")

    # ================= 5. SELENIUM =================
    add_heading_custom(doc,
                       "5. Punto 2: Procedimiento para ejecutar el login vía Selenium",
                       level=2)
    add_paragraph(doc,
                  "La prueba con Selenium automatiza un navegador real para simular el ingreso "
                  "del usuario a través de la interfaz gráfica.")

    add_heading_custom(doc, "5.1 Descripción de la prueba", level=3)
    add_paragraph(doc,
                  "El archivo 7_pruebaUISelenium.py abre el navegador, navega a la página "
                  "principal, localiza los campos del formulario de login por su identificador "
                  "HTML, escribe el correo y la contraseña, envía el formulario y espera a que "
                  "aparezca la vista de la aplicación. Después, como verificación adicional, "
                  "registra un producto y comprueba que aparezca en la tabla.")

    add_paragraph(doc,
                  "Los elementos de la interfaz que se utilizan son: el contenedor del "
                  "formulario #vista-login, el campo #correo-login, el campo #contrasena-login, "
                  "el formulario #form-login, y ya dentro de la aplicación, #vista-app y "
                  "#usuario-nombre.")

    add_heading_custom(doc, "5.2 Configuración del navegador", level=3)
    add_paragraph(doc,
                  "Para que Selenium no tenga que descargar el controlador en tiempo de "
                  "ejecución, el archivo conftest.py fija la ubicación del navegador y del "
                  "chromedriver, y garantiza que la variable DISPLAY esté definida en entornos "
                  "con servidor gráfico:")
    add_code_block(doc, [
        "CHROME_BIN = \"/usr/bin/brave-origin-nightly\"",
        "DRIVER_BIN = os.path.expanduser(",
        "    \"~/.cache/selenium/chromedriver/linux64/\"",
        "    \"155.0.8059.39/chromedriver\")",
        "opts = Options()",
        "opts.binary_location = CHROME_BIN",
        "svc = Service(executable_path=DRIVER_BIN)",
    ], title="Fragmento: conftest.py")

    add_paragraph(doc,
                  "Las credenciales se leen del archivo usuarios_prueba.json, que contiene la "
                  "cuenta con perfil admin:")
    add_code_block(doc, [
        "{",
        "  \"usuarios\": [",
        "    {",
        "      \"nombre\": \"Pedrito\",",
        "      \"correo\": \"pedrito@gmail.com\",",
        "      \"contrasena\": \"bolivia123\",",
        "      \"rol\": \"admin\"",
        "    }",
        "  ]",
        "}",
    ], title="Fragmento: usuarios_prueba.json")

    add_heading_custom(doc, "5.3 Procedimiento paso a paso", level=3)
    add_bullets(doc, [
        "Paso 1. Confirmar que la aplicación Flask esté activa en el puerto 5000.",
        "Paso 2. Verificar que el entorno virtual tenga instalada la librería selenium.",
        "Paso 3. Comprobar la configuración del navegador y del chromedriver (conftest.py).",
        "Paso 4. Crear el archivo usuarios_prueba.json con la cuenta admin.",
        "Paso 5. Ejecutar la prueba con pytest y observar cómo se abre el navegador.",
    ])
    add_code_block(doc, [
        "source .venv/bin/activate",
        "python -m pytest 7_pruebaUISelenium.py -v -s",
    ])

    add_heading_custom(doc, "5.4 Resultado esperado", level=3)
    add_paragraph(doc,
                  "El navegador se abre, se escriben las credenciales en el formulario y se "
                  "envía. La Figura 2 muestra el formulario de inicio de sesión con los datos "
                  "ya ingresados, y la Figura 3 muestra la aplicación autenticada, con el "
                  "nombre del usuario en la barra superior. La prueba finaliza con un caso "
                  "aprobado.")

    add_figura(doc, "02_selenium_login_form.png",
               "Figura 2. Formulario de inicio de sesión diligenciado por Selenium con el "
               "correo pedrito@gmail.com y la contraseña de prueba.", ancho_cm=9.5)
    add_figura(doc, "03_selenium_app.png",
               "Figura 3. Aplicación con la sesión iniciada tras enviar el formulario: se "
               "observa el nombre del usuario en la barra superior.", ancho_cm=15.5)

    # ================= 6. CYPRESS =================
    add_heading_custom(doc,
                       "6. Punto 3: Procedimiento para ejecutar el login vía Cypress",
                       level=2)
    add_paragraph(doc,
                  "La prueba con Cypress verifica el mismo login exitoso, pero desde un "
                  "framework de pruebas de extremo a extremo escrito en JavaScript.")

    add_heading_custom(doc, "6.1 Descripción de la prueba", level=3)
    add_paragraph(doc,
                  "El archivo 8_pruebaUICypress.cy.js visita la raíz del sitio, comprueba que "
                  "la vista de login sea visible, escribe el correo y la contraseña y envía el "
                  "formulario. Luego verifica que la vista de la aplicación y los datos del "
                  "usuario sean visibles y no estén vacíos.")
    add_code_block(doc, [
        "cy.visit(\"/\");",
        "cy.get(\"#vista-login\").should(\"be.visible\");",
        "cy.get(\"#correo-login\").type(\"pedrito@gmail.com\");",
        "cy.get(\"#contrasena-login\").type(\"bolivia123\",",
        "                                  { log: false });",
        "cy.get(\"#form-login\").submit();",
        "cy.get(\"#vista-app\").should(\"be.visible\");",
        "cy.get(\"#usuario-nombre\").should(\"be.visible\")",
        "                            .and(\"not.be.empty\");",
    ], title="Fragmento: 8_pruebaUICypress.cy.js")

    add_heading_custom(doc, "6.2 Configuración de Cypress", level=3)
    add_paragraph(doc,
                  "El archivo cypress.config.js define la dirección base de la aplicación y lee "
                  "las credenciales del archivo usuarios_prueba.json dentro de la función "
                  "setupNodeEvents, de modo que la prueba no tenga las credenciales escritas en "
                  "el propio archivo de prueba:")
    add_code_block(doc, [
        "module.exports = defineConfig({",
        "  e2e: {",
        "    baseUrl: \"http://localhost:5000\",",
        "    specPattern: \"8_pruebaUICypress.cy.js\",",
        "    setupNodeEvents(on, config) {",
        "      config.env = { ...config.env, ...credenciales };",
        "      return config;",
        "    },",
        "  },",
        "});",
    ], title="Fragmento: cypress.config.js")

    add_heading_custom(doc, "6.3 Procedimiento paso a paso", level=3)
    add_bullets(doc, [
        "Paso 1. Instalar Node.js y las dependencias del proyecto con npm install.",
        "Paso 2. Confirmar que la aplicación Flask esté activa en el puerto 5000.",
        "Paso 3. Verificar el archivo de soporte cypress/support/e2e.js.",
        "Paso 4. Ejecutar la prueba en modo consola indicando el archivo de prueba.",
        "Paso 5. Observar el resumen con el resultado de la ejecución.",
    ])
    add_code_block(doc, [
        "npm install",
        "npx cypress run --spec 8_pruebaUICypress.cy.js",
        "# o simplemente:",
        "npm run test:cypress",
        "# modo interactivo (opcional):",
        "npx cypress open",
    ])

    add_heading_custom(doc, "6.4 Resultado esperado", level=3)
    add_paragraph(doc,
                  "Cypress abre un navegador controlado, ejecuta el caso y muestra el resumen "
                  "con todos los pasos aprobados. La consola informa que la prueba pasó (All "
                  "specs passed). La evidencia se muestra en la Figura 4.")

    add_figura(doc, "04_cypress_login.png",
               "Figura 4. Ejecución del login vía Cypress: la prueba del caso de inicio de "
               "sesión finaliza aprobada.")

    # ================= 7. RESULTADOS =================
    add_heading_custom(doc, "7. Resultados y evidencias (capturas)", level=2)
    add_paragraph(doc,
                  "En esta sección se resumen los resultados obtenidos en cada una de las "
                  "pruebas ejecutadas. Todas las ejecuciones se realizaron contra la aplicación "
                  "local en http://localhost:5000 con la cuenta pedrito@gmail.com.")
    add_table_with_data(
        doc,
        ["Prueba", "Herramienta", "Comando", "Resultado"],
        [
            ["Login y productos (API)", "pytest + requests",
             "pytest 4_test_api_productos.py", "15 aprobadas"],
            ["Autenticación (unitarias)", "pytest",
             "pytest 5_test_autenticacion.py", "13 aprobadas"],
            ["Login (interfaz)", "Selenium",
             "pytest 7_pruebaUISelenium.py", "1 aprobada"],
            ["Login (interfaz)", "Cypress",
             "cypress run --spec 8_...cy.js", "1 aprobada"],
        ],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT] * 4,
        title="Tabla 1. Resumen de resultados de las pruebas ejecutadas.",
    )

    add_paragraph(doc,
                  "Como demostración del funcionamiento, las Figuras 1 a 4 presentan, de forma "
                  "ordenada, la ejecución del login por API (Figura 1), el formulario de inicio "
                  "de sesión diligenciado con Selenium (Figura 2), la aplicación autenticada "
                  "tras el login con Selenium (Figura 3) y la ejecución de la prueba con "
                  "Cypress (Figura 4).")

    # ================= 8. DIFICULTADES =================
    add_heading_custom(doc, "8. Dificultades encontradas", level=2)
    add_paragraph(doc,
                  "La principal dificultad no estuvo en el código de las pruebas, sino en la "
                  "preparación del entorno. Selenium intentaba descargar automáticamente su "
                  "controlador a través de Selenium Manager y la descarga se quedaba detenida; "
                  "se resolvió indicando explícitamente el navegador y el chromedriver ya "
                  "disponibles en el equipo mediante el archivo conftest.py.")
    add_paragraph(doc,
                  "En Cypress, la versión fijada en package.json utilizaba una versión de "
                  "Electron que se cerraba inesperadamente al iniciar; se actualizó Cypress a "
                  "una versión compatible. Además, la versión nueva dejó de admitir la lectura "
                  "de variables con Cypress.env en el archivo de prueba, por lo que las "
                  "credenciales se colocaron de forma directa en el archivo de la prueba.")

    # ================= 9. CONCLUSIONES =================
    add_heading_custom(doc, "9. Conclusiones", level=2)
    add_paragraph(doc,
                  "Se logró levantar el sistema de forma local y ejecutar con éxito el login "
                  "desde los tres enfoques solicitados. La prueba de API confirmó el "
                  "funcionamiento del endpoint /api/sesion; la prueba de Selenium confirmó el "
                  "ingreso a través de la interfaz gráfica con un navegador real; y la prueba "
                  "de Cypress confirmó el mismo recorrido desde un framework de pruebas de "
                  "extremo a extremo.")
    add_paragraph(doc,
                  "La práctica permitió comprobar que un mismo caso de prueba puede verificarse "
                  "en distintos niveles de automatización y que la mayor parte del esfuerzo se "
                  "concentra en dejar el entorno reproducible. Documentar cada paso, desde la "
                  "base de datos hasta la ejecución de las pruebas, facilita repetir el "
                  "procedimiento y garantiza que los resultados sean verificables.")

    # ================= 10. ANEXOS =================
    add_heading_custom(doc, "10. Anexos", level=2)
    add_paragraph(doc,
                  "En este apartado se incluye el código de los archivos empleados en la "
                  "práctica. Cada anexo presenta el nombre del archivo y el espacio donde se "
                  "coloca la captura de su código.")

    anexos = [
        ("Anexo 1. Archivo 4_test_api_productos.py",
         "Prueba del login y de los productos vía API (Punto 1)."),
        ("Anexo 2. Archivo api_login_demo.py",
         "Script de demostración que ejecuta el login por API y muestra la sesión activa."),
        ("Anexo 3. Archivo conftest.py",
         "Configuración del navegador y del chromedriver para las pruebas con Selenium."),
        ("Anexo 4. Archivo 7_pruebaUISelenium.py",
         "Prueba de login a través de la interfaz gráfica con Selenium (Punto 2)."),
        ("Anexo 5. Archivo 8_pruebaUICypress.cy.js",
         "Prueba de login con Cypress (Punto 3)."),
        ("Anexo 6. Archivo cypress.config.js",
         "Configuración de Cypress (dirección base y credenciales)."),
    ]
    for titulo, pie in anexos:
        add_heading_custom(doc, titulo, level=3)
        add_paragraph(doc, pie)
        add_image_placeholder(
            doc, f"<< PEGAR AQUI LA CAPTURA DEL CODIGO: {titulo} >>")

    salida = os.path.join(BASE_DIR,
                          "Informe_Testing_Login_API_Selenium_Cypress.docx")
    doc.save(salida)
    print(f"Documento generado: {salida}")


if __name__ == "__main__":
    main()
