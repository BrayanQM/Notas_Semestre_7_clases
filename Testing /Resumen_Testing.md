# RESUMEN DE MATERIA: TESTING DE SOFTWARE

> Resumen de todas las clases (.md) con objetivo, palabras clave y contenido de cada tema.
> Incluye las imágenes de los enlaces citados en las notas.

---

## 1. Fundamentos de calidad y testing (17 de agosto)

**Objetivo:** Comprender los conceptos base del testing (errores, defectos, fallos, riesgos), diferenciar verificación de validación, conocer el costo de la calidad, la norma ISO 25010 y los principios del testing (ISTQB).

**Palabras clave:** error, defecto, bug, fallo, riesgo, verificación, validación, CoQ (costo de la calidad), Ley de Boehm, ISO 25010, ISTQB, 7 principios.

### 1.1 Conceptos base
1. **Error humano:** acción de una persona al escribir código, diseñar o implementar un requisito (ocurre ANTES de entregar).
2. **Defecto (bug):** anomalía en el software causada por un error (se encuentra DESPUÉS de la entrega).
3. **Fallo:** comportamiento incorrecto del sistema cuando se ejecuta (efecto visible DESPUÉS de entregar).
4. **Riesgo:** posibilidad de que ocurra un fallo con cierto impacto.

> El **error es humano**, el **defecto está en el código**, el **fallo es lo que ve el usuario**.

### 1.2 Verificación vs Validación
* **Verificación (¿lo construimos bien?)**
  - Pregunta: ¿cumple con lo que se pidió?
  - Métodos **estáticos**: revisión de código, inspección de documentos de requisitos, pruebas estáticas (recorrido mental sin ejecutar).
- **Validación (¿satisface las necesidades reales?)**
  - Pregunta: ¿el sistema satisface las necesidades reales del usuario?
  - Métodos **dinámicos**: probar el software funcionando, pruebas de aceptación de usuario (UAT), pruebas exploratorias.

### 1.3 Costo de la calidad (CoQ)
> ¿Cuánto cuesta un bug? → **Ley de Boehm: corregir un defecto en fases tempranas cuesta 1 unidad; en producción cuesta hasta 100 unidades.**

![Ley de Boehm - costo de cambio](https://storage.ghost.io/c/e2/0b/e20b1dc7-7596-416c-bbad-2be3126c3a68/content/images/2024/06/costofchangeboehm.jpeg)

1. **Costo de prevención:** gastos para evitar que los errores sucedan.
   - Capacitación del equipo, revisiones formales (pair programming), estándares de codificación, análisis estático (SonarQube).
2. **Costo de evaluación:** gastos para medir y revisar que los productos estén bien.
   - Pruebas unitarias (devs), integración y aceptación, pruebas de sistemas y regresión, licencias de herramientas (Jira/Xray).
3. **Costo de fallos internos:** errores detectados antes de entregar.
   - Tiempo arreglando bugs del sprint, rehacer funcionalidades, horas extra para parchear.
4. **Costo de fallos externos:** errores detectados por el cliente.
   - Pérdida de ventas, call center saturado, pérdida de imagen de marca, penalizaciones (SLA).

### 1.4 Modelo de calidad ISO 25010
**Objetivo:** responder "¿cuánto podemos decir que este software es de calidad?" (8 características).

1. **Funcionalidad:** ¿hace lo que debe? → pruebas funcionales (clic en "agregar al carrito" y el producto aparece).
2. **Eficiencia de rendimiento:** rendimiento adecuado con los recursos usados (tiempo, memoria) → pruebas de carga y estrés (1000 logins a la vez en < 2s). Nota: la variable debe vivir mientras necesite existir (buena práctica en memoria, notable en software embebido).
3. **Compatibilidad:** intercambiar información con otros sistemas/entornos → pruebas de integración y navegación (Chrome, Firefox, Edge, Safari, Android).
4. **Usabilidad:** comprendido, aprendido, usado y atractivo → pruebas UX/UI y exploratorias (¿registro en menos de 2 min sin manual? ¿botones del tamaño de un dedo?).
5. **Fiabilidad:** mantener rendimiento bajo condiciones específicas → pruebas de recuperación y robustez (¿se corta la luz mientras guarda un pedido? ¿se corrompe?). Nota: backup diferencial (cambio desde la anterior) vs total (copia completa).
6. **Seguridad:** proteger la información → pruebas de seguridad (OWASP top 10), intentar `OR 1=1`, acceder a `/admin` sin loguear. Nota: no hardcodear código/credenciales.
7. **Mantenibilidad:** ser modificado eficaz y eficiente → análisis de deuda técnica y regresión (IVA 21%→22% centralizado en una constante = mantenible; repetido en 100 sitios = no).
8. **Portabilidad:** transferido de un entorno a otro → pruebas de instalación y configuración (Windows → Linux).

### 1.5 Principios ISTQB
**Objetivo:** conocer los fundamentos (leyes) que todo tester debe respetar.
1. El testing muestra la **presencia** de defectos, no su ausencia.
2. Es **imposible probar todo** → priorizar por análisis de riesgo.
3. **Pruebas tempranas** → involucrar a los testers desde el inicio.
4. **Agrupación de defectos** → pocos módulos concentran la mayoría de bugs (analizar los críticos).

### 1.6 Los 7 principios del testing
1. **Paradoja del pesticida:** repetir las mismas pruebas deja de encontrar bugs: revisar, modificar y crear nuevas pruebas regularmente.
2. **El testing depende del contexto:** no es lo mismo un videojuego, un sistema médico o una red social.
3. **La ausencia de errores es una falacia:** puede funcionar bien pero no cumplir las necesidades del negocio; es preferible con bugs pero que resuelva el problema.

---

## 2. Estrategia de testeo (24 de agosto)

**Objetivo:** entender cuándo y qué tipo de pruebas hacer (shift-left), la pirámide de pruebas, el anti-patrón "copa de helado", el rol del QA (tradicional vs ágil) y los cuadrantes de testing.

**Palabras clave:** shift-left, pruebas estáticas, BDD, pirámide de pruebas, copa de helado, QA ágil, cuadrantes Q1/Q2/cuadrante de negocio, criterios de aceptación.

### 2.1 Shift-left y pruebas estáticas
* El testeo crece igual que Boehm: cuanto más a la izquierda (temprano), más barato.

![Shift-left](https://storage.ghost.io/c/56/e6/56e6bee2-64b3-46fc-9f38-839cefa57dd7/content/images/2023/04/image1-1.png)

* **Pruebas estáticas:** revisión de requerimientos, especificaciones y código antes de ejecutar.
* **BDD (Behavior Driven Development):** se escriben escenarios de prueba en lenguaje natural ANTES de que el desarrollador escriba el código.

### 2.2 Pirámide de pruebas (correcta)
```bash
        PRUEBAS EXPLORATORIAS
        PRUEBAS AUTOMATIZADAS
        PRUEBAS DE ACEPTACIÓN
        PRUEBAS UNITARIAS
```
* Notas: las unitarias son rápidas, baratas y las ejecutan los DEVS (es la base, mayor cantidad).

![Pirámide de pruebas de Mike Cohn](https://abstracta.us/es/wp-content/uploads/2019/12/piramide-automatizacion-pruebas-funcionales-mike-cohn-1024x559.png)

### 2.3 Anti-patrón "copa de helado" (incorrecta)
```bash
        PRUEBAS EXPLORATORIAS
        PRUEBAS AUTOMATIZADAS
        PRUEBAS INTEGRACIÓN DE COMPONENTES
        PRUEBAS UNITARIAS
```
* Nota: se enfoca demasiado en la parte visual del usuario; error común en equipos pequeños y novatos (muchas pruebas UI y pocas unitarias).

### 2.4 Rol del Analista de Calidad (Tester)
| Tradicional | Ágil |
|---|---|
| Enemigos: equipo de pruebas separado | Parte del equipo multidisciplinario |
| Pruebas al final de lo funcional | Pruebas a través del desarrollo |
| Trabajan solos | Colaboran con Dev, Ops, Stakeholders |
| Actúan como filtros para detectar bugs | Detectan y evitan bugs, levantan riesgos |
| Sin contacto con el negocio | Contacto directo con el negocio |
| Sin idea de la planificación | Participa en release y sprint planning |

### 2.5 Cuadrantes de testing (Q1 y Q2)
![Cuadrantes de testing ágil](https://federico-toledo.com/wp-content/uploads/2017/09/Agile-Testing-Quadrants.png)

* **Q1 (Técnico / apoya al equipo):** pruebas unitarias (devs) → ejemplo: carrito con descuento.
  - Ejemplo tabla: 3 artículos × 10bs con 10% = 27bs; 0 artículos = 0bs; 3 artículos con 100% = 0bs.
* **Q2 (Negocio / apoya al equipo):** pruebas funcionales → ejemplo login.
  - Historia: "como usuario registrado quiero iniciar sesión con mi email (e) y contraseña (c)".
  - Tabla de casos de login:

| valor | signo | valor | resultado | mensaje |
|---|---|---|---|---|
| e = v | ^ | c = v | camino feliz | dashboard |
| e = f | ^ | c = v | mensaje | correo no registrado |
| e = v | ^ | c = f | mensaje | contraseña incorrecta |
| e = f | ^ | c = f | mensaje | correo no registrado |
| e = f | ^ | c = N intentos | mensaje | bloquear cuenta temporalmente |

* **Criterios de aceptación (AC):** con email y contraseña correctos redirige a dashboard. Las pruebas Q2 ejecutan los AC manualmente.

---

## 3. Cuadrantes Q3/Q4, esfuerzo, integración del QA y DoR (31 de agosto)

**Objetivo:** aplicar los cuadrantes extendidos (Q3 negocio crítico y Q4 técnico), la distribución de esfuerzo, cómo integrar al QA en el equipo, el concepto de Definition of Ready (DoR) y un ejercicio hands-on (recuperación de contraseña).

**Palabras clave:** Q3, Q4, UAT, pruebas exploratorias, Jmeter, OWASP ZAP, distribución de esfuerzo, Daily Scrum, Sprint Planning, retrospectiva, pair testing, code review, DoR, criterios de aceptación, datos de prueba, mocks.

![Cuadrantes de testing ágil](https://federico-toledo.com/wp-content/uploads/2017/09/Agile-Testing-Quadrants.png)

### 3.1 Cuadrante Q3 (Negocio / apoya al producto)
* **Quién lo hace:** QA, PO, usuarios finales.
* **Qué apoya:** al producto asegurando que sea útil y usable.
* **Acción del QA:** pruebas exploratorias guiadas por la experiencia del usuario (¿y si el usuario hace clic aquí sin querer?).
* **Ejemplo (historial de pedidos):** ¿usuario sin pedidos? ¿100 pedidos carga rápido? ¿se ordenan por fecha? ¿botones fáciles de encontrar? ¿diseño intuitivo?
* **UAT:** el PO envía a 5 usuarios reales a probar la funcionalidad y da feedback sobre la experiencia.

### 3.2 Cuadrante Q4 (Técnico / no funcional)
* **Quién lo hace:** especializados en Devops con apoyo del QA.
* **Qué apoya:** la supervivencia del producto en producción.
* **Pruebas:**
  1. **Rendimiento/carga:** Jmeter simula 1000 usuarios en login simultáneo; medir tiempo de respuesta (< 2 s).
  2. **Seguridad:** OWASP ZAP escanea la app por SQL injection y XSS.
  3. **Resiliencia:** cómo responde el sistema cuando la BD crece de 100 a 10 000 registros.

### 3.3 Distribución de esfuerzo (importancia de los cuadrantes)
| Cuadrante | % de esfuerzo | Quién lo hace |
|---|---|---|
| Q1 (unitarias) | 40% | Dev |
| Q2 (funcionales) | 30% | QA (manual + automatización) |
| Q3 (exploratoria) | 20% | QA + PO |
| Q4 (no funcional) | 10% | QA especializados + Devops |

* **Error común:** 80% del esfuerzo en Q2, 10% en Q3, 10% en Q1 y Q4 inexistente → bugs en producción por rendimiento y seguridad.

### 3.4 Cómo integrar al QA en el equipo
1. **Daily Scrum:** reporta avances, bloqueos y riesgos de pruebas.
2. **Sprint Planning:** estima el esfuerzo de pruebas y negocia el alcance.
3. **Retrospectivas:** propone mejoras en el proceso de pruebas y calidad del equipo.
4. **Pair testing:** QA y Dev prueban juntos una historia completa.
5. **Code reviews:** el QA revisa el código y sugiere dónde añadir unit tests o mejorar la testeabilidad.
6. **Prevención:** el QA hace preguntas como "¿cuánto tiempo debe ser válida la recuperación?".

### 3.5 Definition of Ready (DoR)
**Objetivo:** condiciones que debe cumplir una Historia de Usuario para ser considerada lista e incluida en un Sprint. Los criterios de aceptación deben validarse ANTES para considerarse terminada.

**Condiciones mínimas desde la visión QA:**
1. **Criterios de aceptación claros y testeables** (no vale "rápido"; vale "carga en < 2s"; no vale "puede iniciar sesión"; vale "con contraseña incorrecta muestra credenciales incorrectas").
2. **Datos de prueba definidos:** qué usuarios existen, qué roles, qué condiciones previas, disponibilidad de datos.
3. **Dependencias externalizadas:** si depende de una API externa, debe existir un mock disponible.
4. **Diseño de interfaz aprobado:** mockups/UX aprobados y accesibles.
5. **Nota:** en pruebas de sistema en desarrollo NO se usan datos reales, solo de prueba.

### 3.6 Hands on: recuperación de contraseña (escenario completo)
> Historia: "como usuario quiero recuperar mi contraseña cuando la olvide".

![Escenario de fallo](assets/WhatsApp%20Image%202026-08-31%20at%2020.41.44.jpeg)

**Escenario:** el usuario solicita recuperar contraseña → el sistema dice que envió un correo → el usuario hace clic en el enlace → el enlace dice "token inválido o expirado".

* **Error:** ventana de tiempo de 4 minutos.
* **Defecto:** no se consideró el tiempo que tarda en abrir el correo.
* **Fallo:** el usuario no puede recuperar su contraseña y se frustra.

**CoQ - Prevención:** ¿si tarda en revisar el correo? ¿cuánto debe ser válido el enlace? ¿hay normativa?
**CoQ - Evaluación:** prueba de expiración de token: (a) solicitar, (b) esperar el tiempo definido (5 min), (c) clic. Verificar token válido dentro del tiempo, que expire correctamente y mensaje de error claro con opción de nuevo enlace.
**Fallos internos:** audiencia necesita 2 horas → el equipo ajusta a 24 horas (sugerencia OWASP); sprint se retrasa 1 día pero el producto es usable.
**Fallos externos:** bug llega a producción → quejas en redes, soporte saturado, usuarios abandonan la app.

**ISO 25010 afectada:**
* **Funcionalidad:** requisito no funcional no cumplido.
* **Seguridad:** el token no debe reutilizarse tras usarse; enviar el correo EXACTAMENTE al correo registrado; mensaje genérico ("si el correo existe te enviaremos un enlace") para no exponer la existencia del correo; token aleatorio de largo ≥ 32 caracteres y encriptado (no `?token=123`); invalidar tras expiración, cambio de contraseña o nueva solicitud.

**Criterios de aceptación:** al hacer clic en "¿Olvidaste tu contraseña?" muestra un formulario de un solo campo ("Correo electrónico registrado") y botón "Enviar enlace de recuperación". Probar en Chrome/Firefox/Safari, PC/tablet/móvil (iPhone, Samsung).

---

## 4. Calidad de software y SQA (10 de agosto)

**Objetivo:** definir calidad, los atributos que la miden, por qué asegurar el software y la función/rol del SQA y sus documentos.

**Palabras clave:** aseguramiento, calidad, atributos, defecto/fallo, SQA, plan de calidad, ISO 27001, ISO 9001, auditorías.

### 4.1 ¿Por qué asegurar el software?
1. Preservar información.
2. Pérdidas económicas.
3. Posibles problemas legales.
4. Seguridad.
5. Reputación.

### 4.2 Significado de calidad
* Bien hecho, confiable, durable, garantizado, disponible.
* Lo **subjetivo debe cuantificarse**:
  1. Ausencia de errores.
  2. Adecuación a las necesidades del usuario.
  3. Eficiencia en tiempo, espacio y recursos.
  4. Cumplimiento de estándares.
  5. Dentro del presupuesto.
  6. Dentro del cronograma.
* **Medición cuantitativa:** ej. 200 errores/4 pruebas = 50 errores por prueba; iteración 3 reduce la tasa.
* **Calidad (ISO 9001):** conjunto de características inherentes para satisfacer requerimientos.
* **Calidad de software:** cumplir los RF y los RNF + estándares de desarrollo + características implícitas (ej. responsivo).
* **Estandares:** ISO 27001 (seguridad) e ISO 9001 (calidad) facilitan procesos legales y evitan demandas.

### 4.3 Atributos e actividades de calidad
* **Atributos de calidad:** correctitud, confiabilidad, robustez, reusabilidad, usabilidad, rendimiento, performance, portabilidad, mantenibilidad, disponibilidad, amigabilidad.
* **Calidad de proceso:** todo proceso debe estar definido, documentado, practicado y medido.

### 4.4 SQA (Software Quality Assurance)
* **Definición:** guía planificada y sistemática de todas las acciones necesarias para proveer evidencia adecuada de que el producto cumple los requisitos técnicos establecidos; conjunto de actividades para evaluar el proceso.
* **Funciones SQA:** actúa durante todo el ciclo de vida del proyecto, mejorando la calidad del proceso de desarrollo y mantenimiento.
* **Actividades SQA:** proveer resultados de las revisiones al equipo y escalar problemas no resueltos al nivel apropiado.
* **Documentos del SQA (Plan de calidad):**
  1. **Sección de gestión:** tareas, actividades, roles y responsabilidades.
  2. **Sección de documentación:** se documenta el proyecto desde los requisitos.
  3. **Sección de estándares y convenciones:** revisión de código y estándares.
  4. **Sección de revisiones y auditorías:** revisiones durante el proceso y responsables (el QA también hace pruebas de estrés).
  5. **Sección de pruebas:** plan de pruebas donde el QA ejecuta y obtiene resultados.
  6. **Sección de métodos y herramientas:** herramientas que soportan las actividades del SQA.

---

## 5. Seguridad en bases de datos (borrador)

**Objetivo:** complementar el testing con seguridad sobre recursos de BD más allá del CRUD.

**Palabras clave:** índices, backups, recuperación, redundancia, objetos de BD, autorización.

1. **Gestión de índices:** controlar quién crea/modifica índices (mejoran velocidad pero afectan rendimiento si se administran mal).
2. **Procedimientos de mantenimiento:** restringir acceso a backups, tareas de recuperación ante fallos y configuraciones de redundancia.
3. **Seguridad de los objetos:** proteger tablas y otros objetos internos que interactúan en la gestión diaria contra alteraciones o eliminaciones no autorizadas.

---

## 6. Recordatorios
Archivo `Recordatorios.md`: plantilla de tareas pendientes (sin contenido aún).

---

# 7. CÓMO HACER UN PROYECTO DE TESTING (PASO A PASO)

> Guía para aplicar toda la materia en un proyecto real de software.

### Paso 1. Contexto y requerimientos
1. Recopilar la **historia de usuario** (Como…, quiero…, para…).
2. Aclarar las **reglas de negocio** (ej. login sin auto-registro, correo institucional otorgado por la universidad).
3. Escribir los **Requerimientos Funcionales (RF)** y **No Funcionales (RNF)**.

### Paso 2. Definition of Ready (DoR) — antes del Sprint
1. Redactar **criterios de aceptación (AC)** claros y testeables (medibles, no "que sea rápido").
2. Definir **datos de prueba** (usuarios, roles, condiciones previas).
3. Verificar **dependencias** externas (¿hay mock de la API?).
4. Aprobar el **diseño de interfaz** (mockups/UX) y la accesibilidad.
5. NO usar datos reales en desarrollo: solo datos de prueba.

### Paso 3. Estimación y planificación (Sprint Planning)
1. El QA estima el esfuerzo de pruebas por AC.
2. Distribuir esfuerzo según cuadrantes: **Q1 40% / Q2 30% / Q3 20% / Q4 10%**.
3. Incluir al QA en Daily, planning y retrospectivas.

### Paso 4. Diseño de las pruebas
1. **Pruebas unitarias (Q1):** lógica pura (validadores, dominio, hash) → las ejecutan los DEVS, rápidas y baratas.
2. **Pruebas funcionales (Q2):** casos de prueba en tabla (valores válidos/inválidos → resultado → mensaje) y ejecutar cada AC.
3. **Pruebas exploratorias (Q3):** preguntarse "¿y si el usuario hace clic aquí sin querer?"; UAT con usuarios reales.
4. **Pruebas no funcionales (Q4):** carga/estrés (Jmeter), seguridad (OWASP ZAP), resiliencia.

### Paso 5. Ejecución y seguimiento
1. Aplicar **pruebas tempranas (shift-left)** para reducir costos (Ley de Boehm).
2. Registrar resultados: error humano → defecto en código → fallo visible al usuario.
3. Levantar **riesgos** y escalar problemas no resueltos.
4. Clasificar defectos según **costo de calidad** (prevención, evaluación, fallos internos/externos).

### Paso 6. Métricas y criterios de calidad (ISO 25010)
1. Verificar las **8 características**: funcionalidad, eficiencia, compatibilidad, usabilidad, fiabilidad, seguridad, mantenibilidad, portabilidad.
2. **Verificar (métodos estáticos):** revisiones y BDD. **Validar (métodos dinámicos):** pruebas ejecutadas y UAT.
3. Medir cuantitativamente: errores por prueba, tiempo de respuesta, % de casos pasados.

### Paso 7. Definition of Done y entrega
1. Confirmar que se cumplen **todos los AC**.
2. Ejecutar **pruebas de regresión** ante cualquier cambio.
3. Documentar en el **plan de calidad** (gestión, documentación, estándares, auditorías, pruebas, herramientas).
4. Repetir: el testing muestra **presencia de defectos**, mantener las pruebas actualizadas (paradoja del pesticida).

### Paso 8. Post-entrega y mejora continua
1. Monitorear **fallos externos** (soporte, redes, SLA).
2. Retrospectiva: ajustar procesos, tiempo de expiración de tokens, etc.
3. Volver a planificar el siguiente ciclo con mejoras.

> **Resumen:** un proyecto de testing se basa en pruebas tempranas, una buena pirámide (más unitarias que UI), criterios de aceptación claros, datos de prueba definidos, priorización por riesgo y mejora continua del proceso.