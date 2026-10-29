# METODOLOGÍA DE DESARROLLO DE SOFTWARE: SCRUM

## Caso: Aplicación Móvil Híbrida de Marketplace Universitario con Red Social — CampusMarket
## Universidad Privada Franz Tamayo (UNIFRANZ) — El Alto, 2026

---

## 1. Introducción

El presente documento describe la metodología de desarrollo de software Scrum aplicada al proyecto **CampusMarket**, una aplicación móvil híbrida de marketplace universitario con red social, chat en tiempo real y sistema de reputación, desarrollada con React Native y Expo SDK 56.

Scrum se organiza en tres fases principales que conforman su ciclo de vida:

- **Pregame (Planificación):** Se define la visión del producto, se construye y prioriza el Product Backlog, se estiman los ítems, se diseña la arquitectura y se planifican los Sprints.
- **Game (Desarrollo):** Ejecución iterativa e incremental de los Sprints (en este proyecto, 5 Sprints).
- **Postgame (Cierre):** Integración final, pruebas integrales y entrega del producto.

El presente documento se enfoca en la **fase PREGAME**.

---

## 2. Objetivo y Objetivos del Proyecto

### 2.1 Objetivo General

| Aspecto | Descripción |
|---|---|
| **Objetivo General** | Desarrollar una aplicación móvil híbrida de marketplace universitario que integre una red social con feed multimedia, chat en tiempo real y sistema de reputación, utilizando React Native y Expo SDK 56, para facilitar las transacciones seguras entre los estudiantes de la UNIFRANZ. |

**Tabla 1.** Objetivo general del proyecto.

### 2.2 Objetivos Específicos

| N.° | Objetivo Específico | Módulo/Área | Estado |
|---|---|---|---|
| 1 | Implementar un módulo de autenticación con Firebase Auth que soporte registro con email y Google OAuth. | Auth | Aplica al Sprint 1 |
| 2 | Desarrollar un feed social con publicaciones multimedia, sistema de likes/dislikes y comentarios anidados. | Feed | Aplica al Sprint 2 |
| 3 | Implementar un marketplace con CRUD de productos, búsqueda por texto y galería de imágenes. | Market | Aplica al Sprint 3 |
| 4 | Desarrollar un sistema de chat en tiempo real con Firestore onSnapshot que soporte mensajes de texto, stickers y GIFs. | UserChat | Aplica al Sprint 4 |
| 5 | Implementar un sistema de seguimiento de cuentas con persistencia local. | Team | Aplica al Sprint 5 |
| 6 | Diseñar un layout responsive de tres columnas para escritorio y una columna para móvil. | UI/UX | Aplica al Sprint 1 |
| 7 | Implementar 98 pruebas automatizadas distribuidas entre caja blanca y caja negra con cobertura superior al 70%. | Testing | Aplica al Sprint 5 |
| 8 | Documentar todos los módulos del sistema siguiendo el estándar del proyecto. | Documentación | Aplica a todos los Sprints |

**Tabla 2.** Objetivos específicos del proyecto.

---

## 3. Equipo Scrum (Involucrados)

| Rol | Responsable | Responsabilidades Principales |
|---|---|---|
| **Product Owner (PO)** | **UNIFRANZ** | Definir la visión del producto, priorizar el Product Backlog, representar a los stakeholders (estudiantes y docentes), validar los incrementos y asegurar que se entregue el valor esperado. |
| **Scrum Master (SM)** | **Ing. Marisol** | Facilitar y mentorizar al equipo, asegurar que se sigan los principios y valores de Scrum, eliminar obstáculos, facilitar los eventos (Sprint Planning, Daily Scrum, Sprint Review, Retrospectiva) y garantizar la transparencia del proceso. |
| **Equipo de Desarrollo** | **Brayan Quispe** | Diseñar, desarrollar, probar y documentar todos los módulos del sistema (autenticación, feed, marketplace, chat, seguimiento, pruebas automatizadas, etc.), autoorganizarse y estimar el esfuerzo de los ítems del backlog. |

**Tabla 3.** Equipo Scrum del proyecto CampusMarket.

---

## 4. Fase PREGAME de Scrum

La fase Pregame es la etapa de planificación inicial del proyecto. Se divide en dos etapas principales:

| Etapa | Descripción | Entregables |
|---|---|---|
| **Planificación (Planning)** | Se define la visión del producto, se identifica al alcance y límites, se construye el Product Backlog en base a los requerimientos funcionales y no funcionales, se estiman los ítems y se define el plan de releases y Sprints. | Visión del producto, Product Backlog priorizado, estimaciones, plan de Sprints. |
| **Arquitectura (Architecture)** | Se define el diseño de alto nivel del sistema: arquitectura en capas, tecnologías, estructura de directorios, esquema de base de datos y definición de la Definición de Hecho (DoD). | Diseño de arquitectura, stack tecnológico definido, DoD. |

**Tabla 4.** Etapas de la fase Pregame.

### 4.1 Planificación (Planning)

#### 4.1.1 Visión del Producto

| Aspecto | Descripción |
|---|---|
| **Nombre del producto** | CampusMarket |
| **Caso de estudio** | Universidad Privada Franz Tamayo (UNIFRANZ), sede El Alto |
| **Descripción** | Aplicación móvil híbrida de marketplace universitario que integra red social con feed multimedia, chat en tiempo real y sistema de reputación. |
| **Usuarios objetivo** | Estudiantes universitarios verificados de la UNIFRANZ |
| **Problema que resuelve** | Falta de un espacio seguro y verificado para compra/venta de artículos académicos, sin sistema de reputación ni canal de comunicación integrado. |
| **Tecnologías principales** | React Native, Expo SDK 56, Firebase Auth, Firestore, Cloudinary, pnpm |
| **Metodología** | Scrum (5 Sprints) |

**Tabla 5.** Visión del producto.

#### 4.1.2 Product Backlog

El Product Backlog se elaboró a partir de los requerimientos funcionales (RF) y no funcionales (RNF) identificados en el proyecto. Contiene los ítems priorizados que dirigirán el desarrollo de los Sprints.

**Ítems funcionales (historias de usuario):**

| ID | Ítem del Backlog | Prioridad | Valor | Esfuerzo (Puntos) | Sprint | Criterios de Aceptación |
|---|---|---|---|---|---|---|
| RF-001 | Registro de usuario | Alta | Medio | 8 | Sprint 1 | El usuario puede registrarse con email y contraseña o Google OAuth |
| RF-002 | Inicio de sesión | Alta | Alto | 8 | Sprint 1 | Valida credenciales y mantiene la sesión persistente (onAuthStateChanged) |
| RF-003 | Publicación en feed | Alta | Alto | 13 | Sprint 2 | Permite crear posts con texto, imágenes y video |
| RF-004 | Like/Dislike en posts | Alta | Medio | 8 | Sprint 2 | Votación positiva/negativa con toggle atómico mediante transacciones |
| RF-005 | Comentarios en posts | Alta | Medio | 8 | Sprint 2 | Comentarios anidados con autor y fecha |
| RF-006 | Publicación de productos | Alta | Alto | 13 | Sprint 3 | Productos con título, descripción, precio e imagen |
| RF-007 | Listado de productos | Alta | Medio | 8 | Sprint 3 | Grid de productos con búsqueda por texto |
| RF-008 | Detalle de producto | Media | Medio | 5 | Sprint 3 | Información completa, imagen y comentarios |
| RF-009 | Chat en tiempo real | Alta | Alto | 13 | Sprint 4 | Mensajes de texto, stickers y GIFs con Firestore onSnapshot |
| RF-010 | Seguir cuentas | Media | Medio | 5 | Sprint 5 | Seguir/dejar de seguir cuentas con persistencia en localStorage |
| RF-011 | Perfil de usuario | Media | Medio | 5 | Sprint 5 | Muestra posts y productos del usuario, opción de seguir |
| RF-012 | Subida multimedia | Alta | Alto | 8 | Sprint 2 | Imágenes y videos subidos a Cloudinary (máx. 100 MB) |
| RF-013 | Seed de datos | Media | Bajo | 5 | Sprint 5 | 20 posts y 7 productos precargados en colecciones vacías |
| RF-014 | Layout responsive | Alta | Alto | 8 | Sprint 1 | 3 columnas en escritorio, 1 columna en móvil (breakpoint 900 px) |
| RF-015 | Tema oscuro | Media | Bajo | 3 | Sprint 1 | Interfaz dark mode estilo X/Grok |

**Tabla 6.** Product Backlog — Ítems funcionales.

**Ítems no funcionales:**

| ID | Categoría | Ítem del Backlog | Métrica | Prioridad | Sprint |
|---|---|---|---|---|---|
| RNF-001 | Rendimiento | Carga del feed en menos de 1 segundo | < 1000 ms | Alta | Todos |
| RNF-002 | Rendimiento | Soporte para 100 usuarios concurrentes | 100 usuarios | Media | Todos |
| RNF-003 | Seguridad | Autenticación con Firebase Auth (OAuth 2.0) | OAuth 2.0 | Alta | Sprint 1 |
| RNF-004 | Compatibilidad | Android 10 o superior (API 29+) | API 29+ | Alta | Todos |
| RNF-005 | Compatibilidad | Web con navegadores modernos | Chrome, Firefox | Media | Todos |
| RNF-006 | Usabilidad | Registro en menos de 2 minutos | < 2 min | Media | Sprint 1 |
| RNF-007 | Mantenibilidad | Cobertura de pruebas > 70% | > 70% | Media | Sprint 5 |
| RNF-008 | Almacenamiento | Tamaño máximo de archivo | 100 MB | Media | Sprint 2 |
| RNF-009 | Disponibilidad | Firestore SLA | 99.95% | Alta | Todos |
| RNF-010 | Persistencia | Datos offline con Firestore cache | Cache local | Media | Todos |

**Tabla 7.** Product Backlog — Ítems no funcionales.

#### 4.1.3 Planificación de Sprints

Se planificaron **5 Sprints** con duración de **2 semanas** cada uno (estimación). Cada Sprint entrega un incremento del producto potencialmente funcional.

| Sprint | Duración Estimada | Objetivo del Sprint | Historias de Usuario / Entregables | Incremento |
|---|---|---|---|---|
| **Sprint 1** | 2 semanas | Autenticación y configuración inicial del proyecto | RF-001, RF-002, RF-014, RF-015, RNF-003, RNF-004, RNF-005, RNF-006 | Configuración del proyecto (Expo SDK 56, pnpm, Firebase), login con email y Google OAuth, layout responsive y tema oscuro |
| **Sprint 2** | 2 semanas | Implementación del feed social | RF-003, RF-004, RF-005, RF-012, RNF-001, RNF-008 | Feed multimedia, likes/dislikes, comentarios anidados, subida de media a Cloudinary |
| **Sprint 3** | 2 semanas | Implementación del marketplace | RF-006, RF-007, RF-008 | CRUD de productos, grid con búsqueda, detalle de producto con comentarios |
| **Sprint 4** | 2 semanas | Desarrollo del chat en tiempo real | RF-009, RNF-001, RNF-009 | Chat con mensajes de texto, stickers y GIFs, lista de conversaciones |
| **Sprint 5** | 2 semanas | Pruebas, seed de datos y documentación | RF-010, RF-011, RF-013, RNF-007 | Seguimiento de cuentas, perfil, seed de datos, 98 pruebas automatizadas y documentación final |

**Tabla 8.** Planificación de los 5 Sprints (fase Pregame).

#### 4.1.4 Estimación del Esfuerzo

| Técnica de Estimación | Aplicación |
|---|---|
| **Planning Poker** | Estimación de puntos de historia para los ítems funcionales del Product Backlog |
| **Estimación por tamaño (S/M/L)** | Categorización de ítems no funcionales y tareas de menor complejidad |
| **Velocity estimada** | Aproximadamente 40–50 puntos por Sprint, ajustada en base a la capacidad del desarrollo (equipo de 1 desarrollador) |

**Tabla 9.** Técnicas de estimación utilizadas en Pregame.

### 4.2 Arquitectura (Architecture)

#### 4.2.1 Stack Tecnológico

| Herramienta | Versión | Propósito |
|---|---|---|
| Expo SDK | 56.0.8 | Framework de desarrollo y herramientas |
| React Native | 0.85.3 | Framework de desarrollo móvil |
| Firebase | 12.14.0 | Backend, autenticación y base de datos |
| pnpm | v11 | Gestor de paquetes |
| TypeScript | 5.9.2 | Tipado estático |
| Jest | 29.7.0 | Framework de pruebas |
| ts-jest | 29.4.11 | Integración TypeScript con Jest |
| Cloudinary | 5.9.2 | Almacenamiento de imágenes y videos |
| Expo Router | 56.2.8 | Navegación basada en archivos |
| Git | v2.x | Control de versiones |

**Tabla 10.** Stack tecnológico definido en la fase Pregame.

#### 4.2.2 Arquitectura en Capas

| Capa | Componentes | Descripción |
|---|---|---|
| **Presentación** | Pantallas y componentes UI | Login, feed, marketplace, detalle de producto, chat, perfil, configuración |
| **Aplicación** | Módulos `db.ts` | CRUD de posts, productos, comentarios, mensajes, seguimiento, subida multimedia |
| **Datos** | Firestore, Firebase Auth, localStorage, Cloudinary | Colecciones `posts`, `products`, `conversations` con subcolecciones, autenticación, caché offline |

**Tabla 11.** Arquitectura en capas del sistema.

#### 4.2.3 Definición de Hecho (Definition of Done — DoD)

| # | Criterio |
|---|---|
| 1 | Código desarrollado, tipado y revisado según estándares del proyecto |
| 2 | Ítems del backlog completados y verificados localmente |
| 3 | Pruebas automatizadas (caja blanca y caja negra) aprobadas |
| 4 | Documentación del módulo actualizada |
| 5 | Incremento integrado sin romper funcionalidades previas |
| 6 | Presentado y validado en el Sprint Review con el Product Owner |

**Tabla 12.** Definición de Hecho (DoD) acordada en Pregame.

---

## 5. Resumen de la Fase Pregame

| Actividad | Entregable | Responsable Principal |
|---|---|---|
| Definición de la visión del producto | Visión de CampusMarket | Product Owner (UNIFRANZ) |
| Recolección de requerimientos | Requerimientos funcionales y no funcionales | Product Owner + Desarrollo |
| Construcción y priorización del Product Backlog | Product Backlog priorizado | Product Owner + Desarrollo (Brayan Quispe) |
| Estimación del esfuerzo | Puntos de historia por ítem | Desarrollo (Brayan Quispe) |
| Diseño de arquitectura | Arquitectura en capas y stack tecnológico | Desarrollo (Brayan Quispe) |
| Planificación de releases | 5 Sprints definidos | Scrum Master (Ing. Marisol) + Equipo |
| Definición de DoD | Criterios de aceptación y calidad | Scrum Master (Ing. Marisol) + Equipo |

**Tabla 13.** Resumen de actividades de la fase Pregame y responsables.

---

## 6. Referencias

- Schwaber, K., & Sutherland, J. (2024). *The Scrum Guide*. https://scrumguides.org
- Guía Scrum European Scrum. (2024). *Guía Scrum v.1.0*. www.europeanscrum.org
- Proyecto Integrador CampusMarket. (2026). *Aplicación móvil híbrida de marketplace universitario con red social*. UNIFRANZ.