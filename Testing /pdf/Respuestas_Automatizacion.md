# Respuestas: ¿Se debe automatizar? (Tema 4 - Matriz de decisión)

## 1. Login con usuario y contraseña válidos.
- **¿Se debe automatizar?** SÍ
- **Justificación:**
  - **Frecuencia:** Se ejecuta constantemente (smoke, regresión, cada release), por lo que el costo de automatizar se recupera rápido.
  - **Estabilidad:** El flujo de login es estable y rara vez cambia, por lo que el mantenimiento del test es bajo.
  - **Complejidad técnica:** Es viable automatizarlo con herramientas estándar (Selenium, Playwright) y no requiere juicio humano.
- **Nivel de pirámide:** API o UI (E2E), según dónde se verifique.

## 2. Método que calcula impuestos.
- **¿Se debe automatizar?** SÍ
- **Justificación:**
  - **Criticidad:** Si falla, afecta directamente al negocio (cálculos de dinero), por lo que duele si se rompe.
  - **Frecuencia:** Se ejecuta muchas veces con datos variados (data-driven), ideal para pruebas unitarias.
  - **Estabilidad:** La lógica de cálculo es estable y no depende de la UI.
- **Nivel de pirámide:** **Unitario** (es la base de la pirámide).

## 3. Cambio de color del botón "Comprar" (rediseño cada sprint).
- **¿Se debe automatizar?** NO
- **Justificación:**
  - **Estabilidad:** El diseño cambia cada sprint, el test se rompería constantemente y el mantenimiento costaría más que el beneficio.
  - **Requiere juicio humano:** Evaluar el color es una decisión de estética/UX subjetiva que una máquina no puede juzgar bien.
  - **Costo:** El costo de automatizar y mantener supera el beneficio esperado.
- **Nivel de pirámide:** UI (pero probar el color no vale la pena; se puede validar visualmente de forma manual).

## 4. Prueba exploratoria de la nueva pantalla de «Mis materias» en la plataforma.
- **¿Se debe automatizar?** NO
- **Justificación:**
  - **Exploratoria:** Su objetivo es descubrir bugs nuevos, y para eso la máquina es "pobre" según la tabla Manual vs. Automatizado.
  - **Frecuencia:** Es de una sola ejecución / ejecución puntual, no es repetitiva.
  - **Requiere juicio humano:** El tester explora, observa y decide qué probar, algo que un script no puede replicar.
- **Nivel de pirámide:** UI (prueba manual).

## 5. Registro de 10.000 usuarios concurrentes.
- **¿Se debe automatizar?** SÍ (con herramientas de carga, ej. JMeter, k6)
- **Justificación:**
  - **Frecuencia/Volumen:** Alto volumen de ejecución; una persona no puede registrar 10.000 usuarios de forma manual.
  - **Complejidad técnica:** Es viable (y necesario) automatizar con herramientas de prueba de carga distribuyendo las peticiones.
  - **Ejecutable sin juicio humano:** El resultado es medible (tiempos de respuesta, errores) y comparable contra un esperado.
- **Nivel de pirámide:** **API** (pruebas de rendimiento/API y algunos casos E2E).

## 6. Validación de que el total del carrito suma bien.
- **¿Se debe automatizar?** SÍ
- **Justificación:**
  - **Criticidad:** Si el total se calcula mal, hay pérdida directa de dinero y confianza del cliente.
  - **Frecuencia:** Se repite cada release y con datos variados (distintos ítems, descuentos, impuestos), ideal para data-driven.
  - **Estabilidad:** La lógica es estable; el costo de mantenimiento es bajo.
- **Nivel de pirámide:** **Unitario / API** (lógica de cálculo) + un E2E de humo para integrar.

## 7. Prueba de usabilidad de una pantalla con 5 usuarios reales.
- **¿Se debe automatizar?** NO
- **Justificación:**
  - **Requiere juicio humano:** La usabilidad depende de emociones, percepción y comportamiento; una máquina no puede "sentir" si la pantalla es fácil de usar.
  - **Exploratoria:** Se observa cómo reaccionan personas reales, algo irrepetible con scripts.
  - **Costo:** Automatizar esto aportaría poco valor y perdería el objetivo de la prueba.
- **Nivel de pirámide:** UI (prueba 100% manual).

## 8. Envío de email de confirmación de compra.
- **¿Se debe automatizar?** SÍ
- **Justificación:**
  - **Criticidad:** Un email de confirmación que no llega duele mucho (cliente no confía, reclamos).
  - **Frecuencia:** Se ejecuta en cada compra/regresión, es repetitiva.
  - **Ejecutable sin juicio humano:** Se puede verificar la entrega con APIs de email (Mailosaur, Mailtrap) comparando el resultado esperado.
- **Nivel de pirámide:** **API / Integración**.

## 9. Verificación de que el logo aparece en el header.
- **¿Se debe automatizar?** NO
- **Justificación:**
  - **Estabilidad:** Sufre rediseños frecuentes; el selector del logo cambiaría y rompería el test constantemente.
  - **Costo:** El costo de mantener un test frágil supera el beneficio, ya que es una verificación de un solo clic.
  - **Ejecutable sin juicio humano (poco peso):** Si bien es verificable, el valor de automatizarlo no justifica el esfuerzo.
- **Nivel de pirámide:** UI (prueba manual de humo, rápida de hacer).

## 10. Regresión completa antes de cada release.
- **¿Se debe automatizar?** SÍ
- **Justificación:**
  - **Frecuencia:** Se ejecuta antes de cada release, es el caso más repetitivo de la lista.
  - **Regresión:** La tabla Manual vs. Automatizado indica que la regresión es tediosa manualmente e ideal automatizada.
  - **Velocidad:** Una máquina ejecuta miles de comprobaciones en minutos, mientras que manualmente tomaría horas o días.
- **Nivel de pirámide:** Mixto: **Unitario + API + UI** (toda la pirámide, según la capa).