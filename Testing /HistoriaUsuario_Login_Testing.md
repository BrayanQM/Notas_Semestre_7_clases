# Historia de Usuario: Login con correo estudiantil

---

## 1. Historia de Usuario

> **Como** estudiante activo de la universidad,
> **quiero** iniciar sesión en el sistema usando el correo estudiantil que la universidad me otorga y mi contraseña,
> **para** poder acceder a mi información académica (horarios, notas, matrícula).

### Nota de negocio (importante)
- **El login NO es un registro.** El usuario no puede crear su propia cuenta desde la pantalla de login.
- El correo estudiantil lo **crea y otorga la universidad** (área de registro académico) cuando el estudiante es admitido/matriculado.
- El login solo acepta correos del **dominio institucional** (ej: `@universidad.edu.bo` o `@est.universidad.bo`).
- Si el estudiante no tiene correo, debe solicitarlo a la universidad; el sistema NO ofrece opción de auto-registro.

---

## 2. Errores, defectos y fallos (escenario de login)

> Escenario: el estudiante ingresa su correo estudiantil y contraseña.

* `Error (humano)` → El desarrollador no validó el dominio del correo ni los intentos fallidos al escribir el código.
* `Defecto (bug)` → Anomalía en el software: se aceptan correos personales (`@gmail.com`) y no se bloquea la cuenta tras 3 intentos fallidos.
* `Fallo` → El usuario ve "Sesión iniciada" con un correo que no es institucional, o un estudiante puede intentar contraseñas infinitas (riesgo de fuerza bruta).
* `Riesgo` → Cuenta de otro estudiante comprometida por no limitar intentos ni exigir dominio institucional.

> El **error es humano**, el **defecto está en el código**, el **fallo es lo que ve el usuario**.

---

## 3. Costo de la calidad (CoQ)

### Ley de Boehm
> Corregir un defecto en fases tempranas cuesta **1 unidad**; en producción cuesta **hasta 100 unidades**.

### Costos de prevención (evitar que el error suceda)
* Capacitación del equipo en autenticación segura (OWASP).
* Definición de estándar: login siempre valida dominio institucional y contraseñas con hash.
* Revisión formal de código (pair programming) en el módulo de login.
* Análisis estático (SonarQube) buscando credenciales hardcodeadas.

### Costos de evaluación (medir que esté bien)
* Pruebas unitarias del validador de dominio y de la lógica de contraseña.
* Pruebas de integración y aceptación (login → dashboard).
* Pruebas de regresión al cambiar la política de contraseñas.
* Herramientas de testing (Jira/Xray).

### Costos de fallos internos (detectados antes de entregar)
* Tiempo del equipo arreglando el bug de bloqueo de cuenta reportado en el sprint.
* Rehacer el login porque no cumplía el requisito de "solo correo institucional".

### Costos de fallos externos (detectados por el cliente)
* Estudiante frustrado que no logra entrar y migra a otra plataforma.
* Call center saturado por quejas de "no me deja entrar".
* Pérdida de imagen de la institución en redes sociales.
* Penalizaciones por incumplir el SLA de disponibilidad del sistema.

---

## 4. ISO 25010 aplicada al login

* **Funcionalidad** → ¿Hace lo que debe? Al ingresar correo y contraseña correctos, redirige al dashboard. Si la contraseña es incorrecta, muestra "credenciales incorrectas".
* **Eficiencia de rendimiento** → 1000 estudiantes hacen login a la vez y el servidor responde en menos de 2 segundos. Buena práctica: las variables usadas en la validación se crean solo cuando se necesitan para no consumir memoria.
* **Compatibilidad** → El login funciona en Chrome, Firefox, Edge, Safari, y en la app Android/iOS.
* **Usabilidad** → Un estudiante nuevo puede iniciar sesión en menos de 1 minuto sin leer el manual; el botón "Iniciar sesión" tiene el tamaño adecuado en móvil.
* **Fiabilidad** → Si se corta la luz mientras se valida la sesión, el sistema no corrompe datos y se recupera (disaster recovery); la sesión se guarda correctamente.
* **Seguridad** → Intento de SQL injection (`OR 1 = 1`) en el campo de correo no debe autenticar a nadie; acceso directo a `/admin` sin login debe redirigir al login.
* **Mantenibilidad** → La política de dominio y de intentos está en una constante centralizada; cambiarla no obliga a tocar 100 archivos.
* **Portabilidad** → El login se comporta igual instalado en servidor Windows o Linux.

---

## 5. Principios ISTQB y los 7 principios (aplicados al login)

### Principios ISTQB
* **El testing muestra la presencia de defectos**, no su ausencia: que el login pase todas las pruebas no significa que no tenga bugs.
* **Es imposible probar todo**: priorizar por riesgo → validar dominio, bloqueo de cuenta y recuperación de contraseña.
* **Pruebas tempranas**: el tester participa desde el análisis de la historia de login.
* **Agrupación de defectos**: el módulo de autenticación concentra la mayoría de bugs; requiere mayor análisis.

### Los 7 principios del testing
* **Paradoja del pesticida**: repetir los mismos casos de login deja de encontrar bugs; se deben revisar y crear nuevas pruebas.
* **El testing depende del contexto**: no es lo mismo probar el login de un sistema bancario que una red social; aquí el dominio (universidad) y el riesgo definen la prueba.
* **La ausencia de errores es una falacia**: el login puede funcionar técnicamente pero no cumplir la necesidad del negocio (no permitir auto-registro, exigir correo institucional).

---

## 6. Verificación vs Validación

* **Verificación (¿lo construimos bien? — métodos estáticos)**: revisión de código del login, inspección del documento de requisitos, recorrido mental (walkthrough) del flujo de autenticación, BDD escrito antes del código.
* **Validación (¿satisface las necesidades reales? — métodos dinámicos)**: pruebas del software funcionando, UAT (5 estudiantes reales prueban el login), pruebas exploratorias.

---

## 7. Estrategia de testeo: pirámide de pruebas del login

```bash
        PRUEBAS EXPLORATORIAS / UAT (Q3)
        PRUEBAS DE ACEPTACIÓN (Q2)
        PRUEBAS DE INTEGRACIÓN (componentes: login → API → BD)
        PRUEBAS UNITARIAS (validador de dominio, hash de contraseña)
```

* Nota: muchas pruebas unitarias, son rápidas y baratas, las ejecuta el DEV.
* **Anti-patrón "copa de helado"**: error común en equipos pequeños es llenar el proyecto de pruebas de UI (solo la parte visual) y dejar sin pruebas unitarias. Se debe evitar.

---

## 8. Cuadrantes de testing aplicados al login

| Cuadrante | % esfuerzo | Quién lo hace | En el login |
|---|---|---|---|
| **Q1 (unitarias/tecnico)** | 40% | Dev | Validar que el dominio `@universidad.edu.bo` se acepta y `@gmail.com` se rechaza; que el hash de contraseña es correcto |
| **Q2 (funcionales)** | 30% | QA (manual + automatización) | Ejecutar los casos de prueba del login y verificar cada AC |
| **Q3 (exploratoria)** | 20% | QA + PO + usuarios finales | ¿Qué pasa si un estudiante deja el correo en blanco? ¿Y si escribe mayúsculas? ¿Y si el DOM actual cambió? |
| **Q4 (no funcional)** | 10% | QA especializado + Devops | Jmeter: 1000 alumnos en login simultáneo (< 2s). OWASP ZAP: SQL injection, XSS. Resiliencia: 100 → 10 000 registros de alumnos |

### Pruebas Q3 (exploratorias) — "el usuario hace clic y ni se da cuenta"
* ¿Pega el correo con espacios y no lo entiende?
* ¿El teclado de la app móvil muestra `@` correctamente?
* ¿La contraseña visible por defecto o con "mostrar"? ¿Es intuitivo?
* ¿El error "credenciales incorrectas" se entiende o el usuario se pierde?

### Pruebas Q4
* **Rendimiento**: Jmeter simula 1000 logins simultáneos; tiempo de respuesta < 2 segundos.
* **Seguridad**: OWASP ZAP busca SQL injection, XSS y fuerza bruta.
* **Resiliencia**: el login responde igual con la base de datos de 100 o 10 000 registros.

---

## 9. Definition of Ready (DoR) desde la visión del QA

Condiciones que debe cumplir la historia de login antes de entrar al Sprint:

1. **Criterios de aceptación claros y testeables**
   - NO vale: "el usuario puede iniciar sesión".
   - SÍ vale: "si el correo institucional es correcto pero la contraseña es incorrecta, muestra 'credenciales incorrectas'".
   - SÍ vale: "la página de login carga en menos de 2 segundos".
2. **Datos de prueba definidos**: qué estudiantes existen, qué dominios, qué contraseñas, condiciones previas (cuenta activada).
3. **Dependencias externalizadas**: si el login depende de una API de autenticación institucional, debe existir un mock para probar.
4. **Diseño de interfaz aprobado**: mockups del login aprobados y accesibles.
5. **Nota**: en pruebas en desarrollo no se usan datos reales de estudiantes, solo de prueba.

---

## 10. Criterios de Aceptación (AC) del Login

* **AC-1**: Con correo estudiantil y contraseña correctos, el sistema redirige al dashboard.
* **AC-2**: Con correo estudiantil correcto y contraseña incorrecta, muestra "Contraseña incorrecta".
* **AC-3**: Con correo que **no** es del dominio institucional (ej: `@gmail.com`), muestra "El correo no pertenece a la universidad".
* **AC-4**: Con correo estudiantil no registrado, muestra "Correo no registrado".
* **AC-5**: Si el correo o la contraseña están vacíos, muestra "Campos obligatorios" y NO envía el formulario.
* **AC-6**: Tras 5 intentos fallidos consecutivos, la cuenta se bloquea temporalmente por 15 minutos con mensaje claro.
* **AC-7**: Después de iniciar sesión, al intentar acceder a una URL interna sin autenticación, redirige al login.
* **AC-8**: El campo de correo rechaza inyecciones SQL (`OR 1=1`) y XSS.

### Datos de prueba
* Navegadores: Chrome, Firefox, Edge, Safari.
* Dispositivos: PC, tablet, móvil (iPhone, Samsung).
* Correos de prueba: `est1234@universidad.edu.bo` (activo), `invitado@gmail.com` (no institucional), `noexiste@universidad.edu.bo` (no registrado).
* Contraseñas de prueba: `Correcta123`, `Incorecta!`, `""` (vacía).

---

## 11. Casos de prueba (login)

> e = correo / c = contraseña / v = válido / f = inválido

| # | correo | contraseña | resultado | mensaje |
|---|---|---|---|---|
| CP-01 | e = v (institucional) | c = v | Camino feliz | → Dashboard |
| CP-02 | e = v | c = f | Mensaje | Contraseña incorrecta |
| CP-03 | e = f (dominio no institucional) | c = v | Mensaje | El correo no pertenece a la universidad |
| CP-04 | e = f (no registrado) | c = v | Mensaje | Correo no registrado |
| CP-05 | e = f | c = f | Mensaje | Correo no registrado |
| CP-06 | e = v | c = v (5 intentos fallidos previos) | Bloqueo | Cuenta bloqueada temporalmente (15 min) |
| CP-07 | e = vacío | c = v | Mensaje | Campos obligatorios |
| CP-08 | e = v | c = vacío | Mensaje | Campos obligatorios |
| CP-09 | e = `OR 1 = 1` | c = x | Mensaje | No autentica (seguridad SQL injection) |
| CP-10 | e = `<script>` | c = x | Mensaje | Se rechaza (XSS) |

### Flujo esperado
```
Login
  1. Datos correctos
        → Dashboard
  2. Datos incorrectos
      2.1 correo bien / contraseña mal → mensaje de error
      2.2 correo mal / contraseña bien → mensaje de error
      2.3 5 intentos fallidos → bloqueo temporal de la cuenta
```

---

## 12. Rol del QA en el equipo (login)

* Participa en el **Daily Scrum**: reporta avances, bloqueos y riesgos de las pruebas de login.
* En el **Sprint Planning**: estima el esfuerzo de probar los AC y negocia el alcance.
* En la **retrospectiva**: propone mejoras en el proceso de pruebas del módulo de autenticación.
* **Pair testing**: QA y Dev prueban juntos la historia completa de login.
* **Code review**: el QA revisa el código del Dev y sugiere dónde añadir unit tests (validador de dominio, bloqueo de cuenta).
* **Pregunta de prevención del QA**: ¿cuánto tiempo debe ser válida la sesión? ¿cuándo expira? ¿qué pasa si el estudiante cierra el navegador?

---

## 13. Conclusión

> El login no es un registro: la universidad otorga el correo estudiantil y el sistema solo valida credenciales de ese dominio. Toda la estrategia de testing (CoQ, ISO 25010, pirámide, cuadrantes, DoR, AC y casos de prueba) se enfoca en garantizar que el acceso sea seguro, funcional, usables y sin auto-registro.