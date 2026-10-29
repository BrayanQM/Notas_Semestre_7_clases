UNIVERSIDAD PRIVADA FRANZ TAMAYO
SEDE EL ALTO

FACULTAD DE INGENIERIA

CARRERA DE INGENIERIA DE SISTEMAS
PROYECTO

"APLICACIÓN MÓVIL HÍBRIDA DE MARKETPLACE UNIVERSITARIO CON
RED SOCIAL"

CASO: Universidad Privada Franz Tamayo

AUTOR: Brayan Quispe Mamani

TUTOR: Ing. Juan Gabriel Lazcano Balanza
EL ALTO - BOLIVIA
2026

DEDICATORIA

A mis padres, por su apoyo incondicional durante

toda mi formación académica. Sin su sacrificio y
confianza, este logro no habría sido posible.

A mis hermanos, que siempre estuvieron ahí cuando más
los necesitaba.

A todos los estudiantes que, como yo, creen que la
tecnología puede transformar la forma en que nos
conectamos y colaboramos dentro de la universidad.

AGRADECIMIENTO
por

Agradezco a la Universidad Privada Franz Tamayo

brindarme

necesarios

para

las

mi

herramientas
desarrollo

y

conocimientos

profesional.

A

mis

docentes, que con paciencia y dedicación compartieron
su experiencia a lo largo de la carrera.

A mi tutor Ing. Juan Gabriel Lazcano Balanza, por

su guía y orientación a lo largo de la elaboración de este
proyecto integrador. Sus observaciones fueron clave para
mejorar tanto el enfoque técnico como la documentación
del trabajo.
A

mis

compañeros

de

curso,

con

quienes

compartimos largas horas de estudio, debates técnicos y
momentos de frustración que al final valieron la pena.

Finalmente, agradezco a la comunidad open

source que hizo posible este proyecto. React Native,

Expo, Firebase y todas las herramientas utilizadas son
producto del trabajo colaborativo de desarrolladores
alrededor del mundo.

RESUMEN

El presente proyecto consiste en el diseño y desarrollo de una aplicación móvil

híbrida de marketplace universitario que integra una red social, un sistema de chat

en tiempo real y un mecanismo de reputación basado en calificaciones. La
plataforma, denominada CampusMarket, permite a los estudiantes universitarios

publicar y vender artículos académicos y personales (apuntes, libros, calculadoras,
electrónicos, muebles, entre otros) dentro de un entorno cerrado y verificado
mediante correo institucional.
A

diferencia

de

las

plataformas

de

compra-venta

convencionales,

CampusMarket incorpora un feed social con publicaciones multimedia (imágenes y
video), un sistema de votación (likes y dislikes), comentarios anidados y un sistema
de seguimiento de cuentas. El chat en tiempo real permite coordinar entregas
directamente dentro del campus. La aplicación está desarrollada con React Native y

Expo SDK 56, utilizando pnpm como gestor de paquetes, Firebase Firestore como

base de datos NoSQL con sincronización en tiempo real, Firebase Auth para
autenticación con email y Google OAuth, y Cloudinary para el almacenamiento de
imágenes y videos.

El proyecto implementa 98 pruebas automatizadas distribuidas entre pruebas

de caja blanca y caja negra, cubriendo todos los módulos de la aplicación. Los
resultados muestran que la arquitectura modular basada en componentes y el uso de
Firestore como backend permiten un desarrollo ágil y escalable.

Palabras clave: marketplace universitario, red social, chat en tiempo real,

React Native, Expo, Firebase Firestore, Cloudinary, pruebas automatizadas, caja
blanca, caja negra.

ABSTRACT

This project consists of the design and development of a hybrid mobile

application for a university marketplace that integrates a social network, a real-time

chat system, and a reputation mechanism based on ratings. The platform, called
CampusMarket, allows university students to publish and sell academic and personal
items (notes, books, calculators, electronics, furniture, among others) within a closed
and verified environment through institutional email.

Unlike conventional buying and selling platforms, CampusMarket incorporates

a social feed with multimedia posts (images and video), a voting system (likes and

dislikes), nested comments, and an account follow system. The real-time chat allows
coordinating deliveries directly within the campus. The application is developed with

React Native and Expo SDK 56, using pnpm as package manager, Firebase
Firestore as NoSQL database with real-time synchronization, Firebase Auth for
authentication with email and Google OAuth, and Cloudinary for image and video
storage.

The project implements 98 automated tests distributed between white-box and

black-box tests, covering all modules of the application. The results show that the

modular architecture based on components and the use of Firestore as backend
allow agile and scalable development.

Keywords: university marketplace, social network, real-time chat, React Native,

Expo, Firebase Firestore, Cloudinary, automated testing, white-box, black-box.

TABLA DE CONTENIDO

DEDICATORIA...................................................................................................2
AGRADECIMIENTO...........................................................................................3
RESUMEN ......................................................................................................... 4
ABSTRACT........................................................................................................5
TABLA DE CONTENIDO ................................................................................... 6
MARCO INTRODUCTORIO...............................................................................2
1.1 Introducción .............................................................................................. 2
1.2 Antecedentes............................................................................................2
1.2.1 Antecedentes Internacionales ............................................................ 2
1.2.2 Antecedentes Nacionales...................................................................3
1.2.3 Antecedentes Locales ........................................................................ 4
1.3 Planteamiento del Problema.....................................................................4
1.3.1 Identificación de la Situación Problémica...........................................4
1.3.2 Formulación del Problema..................................................................4
1.3.3 Problemas Específicos.......................................................................5
1.4 Objetivos...................................................................................................5
1.4.1 Objetivo General.................................................................................5
1.4.2 Objetivos Específicos ......................................................................... 5
1.5 Justificación .............................................................................................. 6
1.5.1 Justificación Técnica...........................................................................6
1.5.2 Justificación Social ............................................................................. 6
1.5.3 Justificación Económica ..................................................................... 6
1.6 Alcances y Límites....................................................................................7
1.6.1 Alcance...............................................................................................7

1.6.2 Límites................................................................................................7
MARCO TEÓRICO Y CONCEPTUAL................................................................9
2.1 Desarrollo Móvil Híbrido con React Native...............................................9
2.2 Ecosistema Expo SDK 56.........................................................................9
2.3 Firebase Firestore como Base de Datos ................................................ 10
2.4 Cloudinary para Almacenamiento Multimedia ........................................ 10
2.5 Chat en Tiempo Real con Firestore........................................................11
2.6 Metodología de Desarrollo: Scrum ......................................................... 11
2.7 Gestión de Paquetes con pnpm..............................................................11
2.8 Arquitectura de la Aplicación .................................................................. 12
2.9 Tema Visual y Estilo ............................................................................... 12
MARCO METODOLÓGICO.............................................................................14
3.1 Enfoque de Investigación........................................................................14
3.2 Arquitectura de la Solución.....................................................................14
3.3 Arquitectura en Capas............................................................................14
3.3.1 Capa de Presentación......................................................................14
3.3.2 Capa de Aplicación...........................................................................14
3.3.3 Capa de Datos..................................................................................15
3.4 Firebase como Backend.........................................................................15
3.5 Módulo de Seed de Datos ...................................................................... 15
3.6 Diseño Responsive y Navegación..........................................................16
3.7 Pruebas y Testing...................................................................................16
3.8 Herramientas de Desarrollo....................................................................17
MARCO PRÁCTICO ........................................................................................ 19
4.1 Análisis de Requerimientos .................................................................... 19

4.1.1 Requerimientos Funcionales............................................................19
4.1.2 Requerimientos No Funcionales.......................................................20
4.2 Implementación del Sistema...................................................................20
4.2.1 Módulo de Autenticación .................................................................. 21
4.2.2 Módulo Feed.....................................................................................21
4.2.3 Módulo Marketplace ......................................................................... 21
4.2.4 Módulo de Chat ................................................................................ 22
4.2.5 Módulo de Seguimiento (Team) ....................................................... 22
4.3 Estructura de Directorios ........................................................................ 22
CONCLUSIONES Y RECOMENDACIONES...................................................25
5.1 Conclusiones .......................................................................................... 25
5.1.1 Conclusiones Técnicas.....................................................................25
5.1.2 Conclusiones Metodológicas............................................................25
5.1.3 Conclusiones de Impacto Social.......................................................26
5.2 Recomendaciones..................................................................................26
5.2.1 Recomendaciones Técnicas.............................................................26
5.2.2 Recomendaciones Funcionales ....................................................... 26
5.2.3 Recomendaciones de Seguridad ..................................................... 27
5.3 Conclusión Final ..................................................................................... 27
BIBLIOGRAFÍA ................................................................................................ 28

CAPÍTULO 1

2

MARCO INTRODUCTORIO
1.1 Introducción
La transformación digital ha cambiado la forma en que los estudiantes

universitarios compran, venden e interactúan entre sí. En la mayoría de las

universidades, los estudiantes recurren a grupos de Facebook, WhatsApp o
aplicaciones de compra-venta genéricas para comercializar apuntes, libros y otros
artículos. Sin embargo, estas plataformas presentan problemas graves: no hay
verificación de identidad, no existe un sistema de reputación confiable, y la
información se pierde entre cientos de mensajes.

La idea de crear un marketplace exclusivo para universitarios nació de una

necesidad real. Durante los primeros semestres, varios compañeros compraban
libros usados por Facebook y terminaban estafados. No había forma de saber si el
vendedor era realmente un estudiante o si el producto existía. Fue entonces cuando

surgió la pregunta: ¿y si creamos una plataforma donde solo puedan participar
estudiantes verificados, con un sistema de reputación y un feed donde se pueda ver
la actividad de cada usuario?

CampusMarket nace de esa necesidad. La aplicación combina un marketplace

de productos con una red social donde los estudiantes pueden publicar contenido,

seguir a otros usuarios, dar like a publicaciones y chatear en tiempo real para
coordinar entregas. Todo dentro de un entorno verificado, con tema oscuro y una
interfaz responsive que funciona tanto en web como en dispositivos móviles.
1.2 Antecedentes
1.2.1 Antecedentes Internacionales
Zhang et al. (2024) realizaron un estudio sobre la integración de redes

sociales y comercio electrónico en comunidades universitarias de China. El estudio
demostró que los estudiantes confían tres veces más en recomendaciones de

compañeros que en publicidad tradicional. El modelo de social commerce incrementó

3
las transacciones en un 40% cuando los vendedores tenían verificación de identidad
(Zhang et al., 2024, p. 45).

Harpreet Kaur y Radhika Sapkota, de la Centria University of Applied Sciences

en Finlandia, realizaron una encuesta sobre tendencias de compras online en
jóvenes de 18 a 35 años en el sudeste asiático. Los resultados mostraron que el
72% de los jóvenes prefiere plataformas que combinen interacción social con
comercio electrónico, frente al 28% que usa plataformas tradicionales de ecommerce (Kaur & Sapkota, 2024, p. 12).

En Estados Unidos, la aplicación Depop demostró que el modelo de mercado

con perfil social funciona. Los vendedores con más seguidores venden un 60% más

que aquellos sin presencia social. Sin embargo, Depop no está diseñada
específicamente para entornos universitarios y carece de verificación institucional.
1.2.2 Antecedentes Nacionales
En Bolivia, el comercio electrónico ha crecido sostenidamente. Según datos

del Instituto Nacional de Estadística (2026), las transacciones digitales en el país

aumentaron un 23% respecto al año anterior. Sin embargo, las plataformas

disponibles (Mercado Libre, Facebook Marketplace, grupos de WhatsApp) carecen
de mecanismos de verificación de identidad robustos.

En la Universidad Mayor de San Andrés (UMSA) se desarrolló un sistema web

progresivo de comercio electrónico con pasarela de pagos, pero el proyecto no
incluía una red social ni sistema de chat integrado. Tampoco contaba con pruebas
automatizadas. El proyecto se limitaba a la gestión de ventas e inventarios para una
empresa ferretera, no para la comunidad universitaria (Quispe, 2023, p. 34).

En la Universidad Privada Franz Tamayo, hasta la fecha no se ha desarrollado

una plataforma que combine marketplace, red social y chat en tiempo real para la

4
comunidad estudiantil. Los estudiantes continúan usando métodos informales para la
compra y venta de artículos académicos.
1.2.3 Antecedentes Locales
En la sede El Alto de la UNIFRANZ, los estudiantes han identificado la

necesidad de un espacio digital seguro para realizar transacciones. Durante una
encuesta informal realizada a 30 estudiantes de la carrera de Ingeniería de Sistemas,

el 85% manifestó haber tenido problemas con compras en plataformas no
especializadas, siendo los principales problemas la falta de verificación del vendedor
(65%) y la ausencia de un canal de comunicación directo (45%).
1.3 Planteamiento del Problema
1.3.1 Identificación de la Situación Problémica
Los estudiantes de la UNIFRANZ enfrentan dificultades para realizar

transacciones de compra y venta de artículos académicos dentro de un entorno
seguro y verificado. Las plataformas existentes presentan las siguientes deficiencias:

no verifican la identidad de los usuarios, carecen de un sistema de reputación
acumulativa, no ofrecen un canal de comunicación integrado, y la información de
productos y servicios se pierde en feeds no especializados.

El problema problema era que no existía una plataforma que hiciera todo esto

junto. Había marketplaces, pero sin red social. Había redes sociales, pero sin
marketplace. Y nada estaba pensado específicamente para una comunidad
universitaria cerrada. Cada vez que un estudiante quería vender un libro, tenía que
publicarlo en tres o cuatro grupos diferentes y esperar que alguien le creyera.
1.3.2 Formulación del Problema
¿Cómo desarrollar una aplicación móvil híbrida que integre un marketplace

universitario, una red social con feed de publicaciones multimedia, un sistema de
chat en tiempo real y un mecanismo de reputación, permitiendo a los estudiantes de
la UNIFRANZ realizar transacciones seguras dentro de un entorno verificado?

5
1.3.3 Problemas Específicos
•

¿Cómo implementar un feed social con publicaciones multimedia que

•

¿Cómo diseñar un sistema de chat en tiempo real que facilite la

permita la interacción entre estudiantes?

comunicación entre compradores y vendedores?

• ¿Cómo estructurar un sistema de verificación de usuarios mediante correo

institucional?
•

¿Cómo desarrollar un sistema de reputación acumulativa basado en

calificaciones?

• ¿Cómo implementar pruebas automatizadas de caja blanca y caja negra

que garanticen la calidad del software?
1.4 Objetivos
1.4.1 Objetivo General

Desarrollar una aplicación móvil híbrida de marketplace universitario que

integre una red social con feed multimedia, chat en tiempo real y sistema de
reputación, utilizando React Native y Expo SDK 56, para facilitar las transacciones
seguras entre los estudiantes de la UNIFRANZ.
1.4.2 Objetivos Específicos
1. Implementar un módulo de autenticación con Firebase Auth que soporte

registro con email y Google OAuth.

2. Desarrollar un feed social con publicaciones multimedia, sistema de

likes/dislikes y comentarios anidados.

3. Implementar un marketplace con CRUD de productos, búsqueda por texto y

galería de imágenes.

4. Desarrollar un sistema de chat en tiempo real con Firestore onSnapshot

que soporte mensajes de texto, stickers y GIFs.

5. Implementar un sistema de seguimiento de cuentas con persistencia local.

6. Diseñar un layout responsive de tres columnas para escritorio y una

columna para móvil.

6
7. Implementar 98 pruebas automatizadas distribuidas entre caja blanca y caja

negra con cobertura superior al 70%.

8. Documentar todos los módulos del sistema siguiendo el estándar del

proyecto.

1.5 Justificación
1.5.1 Justificación Técnica
El desarrollo se justifica por la madurez y accesibilidad de las tecnologías

seleccionadas. React Native con Expo SDK 56 permite desarrollar aplicaciones
nativas para Android y web con un solo código base. Firebase Firestore ofrece una
base de datos NoSQL con sincronización en tiempo real y persistencia offline, ideal

para una aplicación que necesita funcionar en entornos con conectividad variable. El
uso de pnpm optimiza los tiempos de instalación y el manejo de dependencias.

La verdad, al principio pensé que íbamos a necesitar un backend completo

con Node.js y Express. Pero resultó que Firebase cubría todo lo que necesitábamos:
autenticación, base de datos en tiempo real y almacenamiento. Eso simplificó
muchísimo la arquitectura y nos permitió enfocarnos en la lógica de la aplicación.
1.5.2 Justificación Social
La plataforma fomenta la colaboración entre estudiantes al facilitar la compra y

venta de artículos académicos dentro de un entorno verificado y confiable. El sistema

de reputación y el feed social permiten que la comunidad estudiantil se autorregule,

reduciendo el riesgo de fraudes y malas experiencias. Además, al estar diseñada
específicamente para el ámbito universitario, la plataforma fortalece el sentido de
comunidad entre los estudiantes.

1.5.3 Justificación Económica
El stack tecnológico elegido (React Native, Expo, Firebase, Cloudinary) utiliza

herramientas con planes gratuitos generosos. Firebase Spark Plan ofrece 1 GB de
almacenamiento, 10 GB de descarga y 50,000 lecturas diarias sin costo. Cloudinary

7
permite 25 GB de almacenamiento en su plan gratuito. Al no procesar pagos
internamente, se eliminan los costos asociados a pasarelas de pago y la complejidad
regulatoria que estas implican.

1.5.4 justificacion Geografica
El uso de este proyecto se limitara para el usoestudiantel en la siguiente

imagen muestra la ubicación geografica en la universidad de la sede del Alto
departamento de La Paz en la universidad privada Franz Tamayo.

8
1.6 Alcances y Límites
1.6.1 Alcance
El proyecto incluye:

• Aplicación móvil híbrida funcional para Android y web.
• Autenticación con email/contraseña y Google OAuth.

• Feed social con publicaciones multimedia (imágenes y video).

• Sistema de likes/dislikes y comentarios anidados en publicaciones.

• Marketplace con creación, listado, búsqueda y eliminación de productos.
• Chat en tiempo real con mensajes de texto, stickers y GIFs.
• Sistema de seguimiento de cuentas con persistencia local.

• Layout responsive (3 columnas en escritorio, 1 columna en móvil).
• 98 pruebas automatizadas (caja blanca y caja negra).
• Documentación completa del sistema.
1.7 Aportes
1.7.1. Aporte Social
La plataforma aporta una herramienta concreta para la inclusión digital de

vendedores informales bolivianos, reduciendo la brecha tecnológica y económica al
eliminar el papeleo y los requisitos formales que históricamente han excluido a este

sector del comercio electrónico. Al verificar la identidad mediante CI y reconocimiento
facial, el sistema genera un ecosistema de confianza que beneficia también a los
compradores, reduciendo el riesgo de fraudes que actualmente son comunes en
Facebook Marketplace y grupos de WhatsApp.
1.7.2. Aporte Académico
El proyecto contribuye al campo de la Ingeniería de Sistemas de UNIFRANZ
demostrando

la viabilidad de integrar multiples tecnologías emergentes (PWA, IA generativa,
biometría facial,

9
social commerce) en un proyecto universitario de alcance real. Constituye un caso de
estudio

reproducible para proyectos similares en Bolivia y sirve como base tecnica para
investigaciones

futuras en las areas de comercio electronico social, seguridad biometrica aplicada y
sistemas de

recomendacion con IA en contextos de mercados emergentes.

CAPÍTULO 2

11

MARCO TEÓRICO Y CONCEPTUAL
2.1 Desarrollo Móvil Híbrido con React Native
React Native es un framework de código abierto desarrollado por Meta que

permite la creación de aplicaciones nativas para Android e iOS utilizando JavaScript

y React (Meta Open Source, 2026). A diferencia del desarrollo web tradicional con

herramientas como Cordova o Ionic, React Native no renderiza componentes web

dentro de un WebView, sino que se comunica con los componentes nativos del
sistema operativo a través de un puente (bridge).

La arquitectura de React Native utiliza un hilo de JavaScript separado del hilo

de UI. El puente (bridge) serializa y deserializa los mensajes que viajan entre ambos
hilos, permitiendo que el código JavaScript controle componentes nativos reales.

Esto proporciona un rendimiento mucho más cercano al de una aplicación nativa
pura que el de las aplicaciones híbridas tradicionales (Eisenman, 2018, p. 23).

Se probó con React Native sin Expo al principio. La configuración del entorno

de desarrollo fue un dolor de cabeza: había que instalar Android Studio, configurar

variables de entorno, lidiar con versiones de JDK y SDK. Con Expo, todo se redujo a
instalar Node.js y ejecutar pnpm install. La diferencia es abismal.
2.2 Ecosistema Expo SDK 56
Expo es un conjunto de herramientas construidas alrededor de React Native

que simplifica el desarrollo, compilación y despliegue de aplicaciones móviles (Expo
Documentation, 2026). La versión SDK 56, lanzada en 2026, proporciona APIs preconstruidas para cámara, notificaciones push, almacenamiento local y reproducción
de video mediante expo-video.

Expo Router, utilizado en este proyecto, implementa un sistema de

navegación basado en archivos similar al App Router de Next.js. Cada archivo dentro
del directorio src/app/ se convierte automáticamente en una ruta de la aplicación.

12
Esto elimina la necesidad de configurar manualmente un stack de navegación y
facilita la organización del código (Expo Documentation, 2026).
2.3 Firebase Firestore como Base de Datos
Firebase Firestore es una base de datos NoSQL flexible y escalable

desarrollada por Google (Firebase Documentation, 2026). Los datos se almacenan

en documentos organizados en colecciones, y cada documento puede contener
objetos anidados complejos, arrays y subcolecciones. Firestore ofrece sincronización
en tiempo real mediante el método onSnapshot, que permite a los clientes recibir
actualizaciones automáticas cuando los datos cambian.

La estructura de datos del proyecto utiliza tres colecciones principales:
Tabla 1. Colecciones de Firestore del proyecto
Colección

Propósito

Estructura

products

Productos del marketplace

conversations

Conversaciones de chat

id, title, description, price,
image, author, created_at +
subcolección comments

posts

Publicaciones del feed social

id, title, body, media[], author,
likes, dislikes, likedBy[],
dislikedBy[], comments[]

id, participants[], lastMessage,
lastMessageTime +
subcolección messages[]

2.4 Cloudinary para Almacenamiento Multimedia
Cloudinary es un servicio de gestión de media en la nube que proporciona

almacenamiento, optimización y entrega de imágenes y videos (Cloudinary
Documentation, 2026). En este proyecto, se utiliza el upload preset sin firma
(unsigned) para simplificar la subida de archivos desde el cliente móvil.

El módulo de Cloudinary implementa dos estrategias de subida dependiendo

de la plataforma: en web, utiliza fetch con FormData y el objeto File del navegador;

en dispositivos móviles, lee el archivo como base64 mediante expo-file-system y lo
envía como data URI. El tamaño máximo permitido es de 100 MB por archivo.

13
2.5 Chat en Tiempo Real con Firestore
El sistema de chat utiliza Firestore con el método onSnapshot para

suscripciones en tiempo real. Cada conversación es un documento en la colección

conversations, y los mensajes se almacenan en una subcolección messages dentro
de cada conversación. Esta estructura permite escalar a miles de mensajes por
conversación sin afectar el rendimiento.

Lo que me sorprendió de Firestore para chat es que no necesitas un servidor

WebSocket aparte. Con onSnapshot, cualquier cambio en la colección se refleja
automáticamente

en

todos

los

clientes

conectados.

La

latencia

es

de

aproximadamente 200 ms en redes normales, que es aceptable para un chat
universitario.

2.6 Metodología de Desarrollo: Scrum
Scrum es un marco de trabajo ágil iterativo e incremental que organiza el

desarrollo en ciclos cortos llamados Sprints (Schwaber & Sutherland, 2024). Cada

Sprint tiene una duración de dos a cuatro semanas y produce un incremento de
producto potencialmente entregable. Scrum define tres roles principales: Product
Owner, Scrum Master y equipo de desarrollo.

Para este proyecto se planificaron 5 Sprints. El Sprint 1 cubrió autenticación y

configuración del proyecto. El Sprint 2 implementó el feed social. El Sprint 3 agregó

el marketplace. El Sprint 4 desarrolló el chat en tiempo real. El Sprint 5 se dedicó a
pruebas automatizadas, seed de datos y documentación.
2.7 Gestión de Paquetes con pnpm
yarn

pnpm es un gestor de paquetes que ofrece ventajas significativas sobre npm y
en

términos

de

velocidad

y

eficiencia

de

almacenamiento

(pnpm

Documentation, 2026). Utiliza un almacenamiento global único con enlaces

simbólicos, lo que evita la duplicación de dependencias entre proyectos. Además, la

14
estructura estricta de node_modules impide el acceso a dependencias no declaradas
explícitamente en package.json.

2.8 Arquitectura de la Aplicación
La aplicación sigue una arquitectura modular basada en componentes. El

directorio src/ contiene la configuración central (rutas, constantes, contextos, hooks y

librerías), mientras que el directorio modulos/ contiene módulos independientes con

su propia lógica de negocio y acceso a datos. Cada módulo expone un conjunto de
funciones db.ts que encapsulan todas las operaciones de Firestore relacionadas con
ese módulo.

Los módulos principales son:
Tabla 2. Módulos principales del proyecto
Módulo

Función

Archivos clave

feed

CRUD de posts, likes,
comentarios

index.tsx, db.ts, PostDetail.tsx,
FeedVideo.tsx

Comentarios de productos

index.tsx, db.ts

login

market

marketPost
UserChat

Autenticación email/password y
Google
CRUD de productos, búsqueda
Chat en tiempo real

team

Seguir/dejar de seguir cuentas

seed

Datos de prueba precargados

cloudinary
testing

Subida de media a Cloudinary
Pruebas y mocks de Firestore

index.tsx

index.tsx, db.ts

index.tsx, db.ts, ChatRoom.tsx,
ChatList.tsx
index.tsx, db.ts
index.ts
index.ts

__mocks__/, CajaBlanca/,
CajaNegra/

2.9 Tema Visual y Estilo
La aplicación utiliza un tema único dark mode estilo X/Grok. Los colores se

definen en una constante centralizada Colors dentro de src/constants/theme.ts. La

paleta incluye fondo negro (#000000), tarjetas gris oscuro (#16181c), bordes gris
(#2f3336), texto blanco suave (#e7e9ea), texto secundario gris (#71767b), acento

verde teal (#22C5AF) y color de peligro rojo (#ef4444). El diseño es responsive con
un breakpoint en 900 px de ancho.

CAPÍTULO 3

16

MARCO METODOLÓGICO
3.1 Enfoque de Investigación
El proyecto se desarrolló bajo un enfoque cuantitativo, ya que se definieron

métricas claras para evaluar el rendimiento y la calidad del software. Las pruebas
automatizadas proporcionan datos numéricos sobre la cobertura y la tasa de éxito de
las funcionalidades implementadas. Asimismo, el tipo de investigación es proyectiva,

pues se propone una solución tecnológica concreta a un problema identificado en la
comunidad universitaria (Hurtado, 2022, p. 67).
3.2 Arquitectura de la Solución
La plataforma sigue una arquitectura cliente-servidor con servicios en la nube

especializados. El cliente móvil se ejecuta en React Native con Expo SDK 56. El
backend se gestiona completamente con Firebase: Firestore para la base de datos,

Firebase Auth para la autenticación y Cloudinary como servicio externo para el
almacenamiento multimedia.
3.3 Arquitectura en Capas
3.3.1 Capa de Presentación
• Pantalla de login con toggle entre inicio de sesión y registro.

• Feed social con posts multimedia, likes, dislikes y comentarios.
crear.

• Marketplace con lista de productos en grid de 2 columnas y FAB para
• Detalle de producto con información completa y comentarios.

• Chat en tiempo real con lista de conversaciones y sala de chat.
• Perfil de usuario con sus posts, productos y opción de seguir.

• Panel de configuración con nombre de usuario y datos de cuenta.
3.3.2 Capa de Aplicación
• Módulo feed/db.ts: CRUD de publicaciones, likes, dislikes, comentarios.

• Módulo market/db.ts: CRUD de productos, búsqueda, filtrado por usuario.

17
• Módulo marketPost/db.ts: Comentarios de productos como subcolección

Firestore.

• Módulo UserChat/db.ts: Creación de conversaciones, envío de mensajes,

stickers.

• Módulo team/db.ts: Seguir y dejar de seguir cuentas con localStorage.

• Módulo cloudinary/index.ts: Subida de imágenes y videos a Cloudinary.
3.3.3 Capa de Datos
• Firestore: colecciones posts, products, conversations con subcolecciones.
• Firebase Auth: autenticación con email/contraseña y Google OAuth.
• localStorage: persistencia de cuentas seguidas en el navegador.
•

precargados.

Persistencia offline: Firestore persistentLocalCache() para datos

3.4 Firebase como Backend
Firebase se configuró mediante variables de entorno expo public firebase que

se cargan desde un archivo .env. La configuración incluye: API Key, Auth Domain,
Project ID, Storage Bucket, Sender ID y App ID. Para el Google Sign-In en
dispositivos móviles, se requiere adicionalmente expo public firebase client id.
Firestore

se

inicializa

con

persistencia

local

habilitada

mediante

persistentLocalCache(), lo que permite que la aplicación funcione sin conexión a
internet para datos previamente cargados. La autenticación persiste entre sesiones

gracias a onAuthStateChanged, que mantiene la sesión activa incluso después de
cerrar la aplicación.

3.5 Módulo de Seed de Datos
Para propósitos de demostración y desarrollo, el proyecto incluye un módulo

de seed (modulos/seed/index.ts) que genera datos de prueba precargados. El seed
se ejecuta automáticamente desde el layout principal cuando las colecciones están
vacías.

18
El seed genera 20 publicaciones con temáticas variadas (tecnología, comida,

compras, estafas, reseñas) y 7 productos (repostería, audífonos, smartwatch, ropa,

accesorios). Cada publicación incluye título, cuerpo, imágenes, autor, likes
aleatorios, dislikes y comentarios anidados. El seed utiliza addDoc directamente de
Firestore.

3.6 Diseño Responsive y Navegación
El layout de la aplicación se adapta al ancho de la pantalla utilizando

useWindowDimensions de React Native. En pantallas de 900 px o más, se muestran
tres columnas: panel izquierdo (información del usuario), columna central (feed o

marketplace) y panel derecho (seguidos y chats recientes). En pantallas más
pequeñas, los paneles laterales se ocultan y aparecen como drawers deslizantes con
overlay semi-transparente.

La navegación inferior en móvil utiliza el módulo butons-fantasma, que

muestra cinco botones: perfil, publicaciones, chat, marketplace y cuentas seguidas.
Cada botón cambia el módulo activo y actualiza la vista central.
3.7 Pruebas y Testing
El proyecto implementa 98 pruebas automatizadas con Jest 29.7.0 y ts-jest.

Las pruebas se organizan en dos categorías: Caja Blanca (white-box) que verifica la

lógica interna y el manejo de casos borde, y Caja Negra (black-box) que prueba las
funciones desde la perspectiva del consumidor.

Para las pruebas se desarrolló un mock completo de Firestore que simula en

memoria todas las operaciones: getDocs, getDoc, addDoc, setDoc, updateDoc,

deleteDoc, runTransaction, arrayUnion, arrayRemove, increment, onSnapshot,

orderBy, where, limit y serverTimestamp. Los mocks adicionales cubren Cloudinary,
expo-document-picker, expo-file-system y react-native.

19
Se utilizo pnpm jest, en la que corre las pruebas de caja negra como la

blanca.

Tabla 3. Distribución de pruebas automatizadas
Módulo

feed/db.ts

market/db.ts

marketPost/db.ts
UserChat/db.ts
team/db.ts

cloudinary/index.ts
seed/index.ts

systembuttons/index.tsx

exportArchive/index.ts
TOTAL

Pruebas Caja Blanca

Pruebas Caja Negra

Total

8

10

18

6

9

15

6

10

8
4
7
4
3
0
0

40

8
5

16
9

7

14

4

7

3

3

6

6

58

98

3.8 Herramientas de Desarrollo
Tabla 4. Herramientas de desarrollo
Herramienta

Versión

Propósito

Expo SDK

56.0.8

Framework de desarrollo y
herramientas

React Native

0.85.3

Firebase

12.14.0

pnpm

v11

Jest

29.7.0

TypeScript
ts-jest

Cloudinary

5.9.2

29.4.11

API REST

Expo Router

56.2.8

Git

v2.x

Framework de desarrollo móvil
Backend, autenticación y base
de datos
Gestor de paquetes principal
Tipado estático

Framework de pruebas

Integración TypeScript con Jest
Almacenamiento de imágenes
y videos
Navegación basada en
archivos
Control de versiones

CAPÍTULO 4

21

MARCO PRÁCTICO
4.1 Análisis de Requerimientos
Los requerimientos del sistema se identificaron a partir de la observación

directa de las necesidades de los estudiantes de la UNIFRANZ y del análisis de las
plataformas existentes en el mercado boliviano. A continuación se presentan los
requerimientos funcionales y no funcionales del sistema.
4.1.1 Requerimientos Funcionales
Tabla 5. Requerimientos funcionales
ID

Requerimiento

Descripción

RF-002

Inicio de sesión

Alta

Auth

RF-003

Publicación en
feed

Valida
credenciales y
mantiene sesión
persistente

Alta

Feed

RF-004

Like/Dislike en
posts

Crea posts con
texto, imágenes y
video

Alta

Feed

RF-005

Comentarios en
posts

Votación positiva
y negativa en
publicaciones

Alta

Feed

RF-006

Publicación de
productos

Comentarios
anidados con
autor y fecha

Alta

Market

RF-007

Listado de
productos

Productos con
título,
descripción,
precio e imagen

Alta

Market

RF-008

Detalle de
producto

Grid de productos
con búsqueda por
texto

Media

Market

RF-009

Chat en tiempo
real

Información
completa, imagen
y comentarios

Alta

Chat

RF-010

Seguir cuentas

Media

Team

RF-011

Perfil de usuario

Seguir y dejar de
seguir a otros
usuarios

Media

Perfil

RF-001

Registro de
usuario

Registro con
email, contraseña
o Google OAuth

Mensajes de
texto, stickers y
GIFs

Posts y productos

Prioridad
Alta

Módulo
Auth

22
RF-012

Subida
multimedia

RF-013

Seed de datos

RF-014

Layout
responsive

RF-015

Tema oscuro

del usuario

Imágenes y video
a Cloudinary

Alta

Cloudinary

20 posts y 7
productos
precargados

Media

Seed

Alta

UI/UX

Interfaz dark
mode estilo
X/Grok

Media

UI/UX

3 columnas
escritorio, 1
columna móvil

4.1.2 Requerimientos No Funcionales
Tabla 6. Requerimientos no funcionales
ID

Categoría

Requerimiento

Métrica

RNF-002

Rendimiento

100 usuarios

Media

RNF-003

Seguridad

Soporte para 100
usuarios
concurrentes

OAuth 2.0

Alta

RNF-004

Compatibilidad

Autenticación con
Firebase Auth

API 29+

Alta

RNF-005

Compatibilidad

Android 10 o
superior (API
29+)

Chrome, Firefox

Media

RNF-006

Usabilidad

Web con
navegadores
modernos

< 2 min

Media

RNF-007

Mantenibilidad

Registro en
menos de 2
minutos

> 70%

Media

RNF-008

Almacenamiento

Cobertura de
pruebas > 70%

100 MB

Media

RNF-009

Disponibilidad

Tamaño máximo
de archivo 100
MB

99.95%

Alta

RNF-010

Persistencia

Firebase SLA
99.95%

Datos offline con
Firestore cache

Cache local

Media

RNF-001

Rendimiento

Carga del feed en
menos de 1
segundo

< 1000 ms

Prioridad
Alta

23
4.2 Digrama DFD
Este es un digrama de flujo de datos, en la que se encarga de mostrar como

el usario usa el sistema del proyecto en la que muestre como es el uso del sistem,a
tanto en la web y en el movil, en diseño hibrido.

24
4.2.1 Implementación del Sistema
A

continuación

se

describen

los

implementación de cada módulo del sistema.

aspectos

más

relevantes

de

la

4.2.1 Módulo de Autenticación
El módulo login (modulos/login/index.tsx) implementa un formulario de

autenticación que permite al usuario registrarse o iniciar sesión con email y
contraseña, o mediante Google OAuth. El formulario tolglea entre modo de inicio de
sesión y registro con un solo botón.

Google Sign-In tiene dos implementaciones: en web usa signInWithPopup con

GoogleAuthProvider y browserPopupRedirectResolver; en dispositivos nativos usa

expo-web-browser para abrir una ventana de autenticación OAuth. Lo complicado del
Google Sign-In nativo fue que necesitábamos el CLIENT_ID_WEB, no el de Android.
Perdí como dos días en eso hasta que encontré la documentación correcta.
4.2.2 Módulo Feed
El feed social (modulos/feed/) es el módulo central de la aplicación. Permite

crear publicaciones con hasta 4 elementos multimedia (imágenes o videos), dar
like/dislike con toggle atómico mediante transacciones de Firestore, y comentar con
IDs incrementales.

La implementación de likes fue interesante. Al principio usamos updateDoc

directamente, pero descubrimos que si dos usuarios daban like al mismo tiempo, se
podía perder un voto. Cambiamos a runTransaction y el problema se solucionó.
Cosas que uno aprende en la práctica y no en los libros.
4.2.3 Módulo Marketplace
El marketplace (modulos/market/) implementa el CRUD de productos. Los

productos se muestran en un grid de 2 columnas con imagen, título y precio en

25
Bolivianos. La búsqueda se realiza del lado del cliente filtrando por título y
descripción.

Cada producto tiene un botón flotante (FAB) para crear nuevos productos. La

eliminación solo está disponible para el autor del producto. Los comentarios de

productos se almacenan en una subcolección separada de Firestore para permitir
escalabilidad.

4.2.4 Módulo de Chat
El chat en tiempo real (modulos/UserChat/) utiliza Firestore onSnapshot para

actualizaciones instantáneas. Soporta mensajes de texto, stickers (24 emojis

predefinidos) y GIFs. Las conversaciones tienen deduplicación: si ya existe una
conversación entre dos usuarios, se reutiliza en lugar de crear una nueva.

La deduplicación de conversaciones fue otro dolor de cabeza. Al principio,

cada vez que alguien hacía clic en Chatear, se creaba una nueva conversación.

Terminamos con 15 conversaciones entre los mismos dos usuarios en los datos de
prueba. La solución fue verificar si ya existía una conversación con los mismos
participantes antes de crear una nueva.

4.2.5 Módulo de Seguimiento (Team)
El módulo team implementa un sistema de seguimiento de cuentas usando

localStorage en lugar de Firestore. Esta decisión se tomó para mantener la
funcionalidad simple y evitar escrituras innecesarias en la base de datos. Las

cuentas seguidas se almacenan como un array JSON en localStorage y se ordenan
de más reciente a más antiguo.
4.3 Estructura de Directorios
El proyecto está organizado en la siguiente estructura de directorios:
proyectoII/

• src/ - Código fuente principal (rutas, constantes, contextos, hooks, lib)

26

datos

•

modulos/ - Módulos independientes con lógica de negocio y acceso a

• modulos/feed/ - Feed social con posts multimedia y comentarios
• modulos/market/ - Marketplace con productos y búsqueda
• modulos/marketPost/ - Comentarios de productos
• modulos/UserChat/ - Chat en tiempo real

• modulos/login/ - Autenticación con email y Google
• modulos/team/ - Seguimiento de cuentas

• modulos/cloudinary/ - Subida de imágenes y videos
• modulos/seed/ - Datos de prueba

• modulos/testing/ - Pruebas automatizadas y mocks
• modulos/account/ - Panel de perfil de usuario

• modulos/account-posts/ - Panel de seguidos y chats
• modulos/account-auto/ - Guard de sesión

• modulos/butons-fantasma/ - Barra de navegación inferior
• modulos/configuracion/ - Pantalla de configuración
• modulos/exportArchive/ - Selector de archivos

• modulos/system-buttons/ - Botón de retroceso nativo
• modulos/diagram/ - Generador de diagramas

• modulos/Android/ - Componentes específicos de Android
• doc/ - Documentación del sistema

CAPÍTULO 5

28

CONCLUSIONES Y RECOMENDACIONES
5.1 Conclusiones
5.1.1 Conclusiones Técnicas
Se logró desarrollar una aplicación móvil híbrida completamente funcional que

integra un marketplace universitario, una red social con feed multimedia, un sistema

de chat en tiempo real y un mecanismo de reputación basado en seguimiento de
cuentas.

La combinación de React Native con Expo SDK 56 demostró ser una

plataforma eficiente para el desarrollo de aplicaciones híbridas. El código base único

funcionó correctamente tanto en Android como en web, con solo pequeñas
adaptaciones para el manejo de archivos y la autenticación con Google.

Firebase Firestore, con su modelo de datos NoSQL y sus suscripciones en

tiempo real, proporcionó una base de datos adecuada para los tres casos de uso
principales: feed social, marketplace y chat. La persistencia offline habilitada permitió
que la aplicación funcionara en entornos con conectividad limitada.
5.1.2 Conclusiones Metodológicas
La metodología Scrum permitió un desarrollo iterativo con entregas

funcionales al final de cada Sprint. La organización en 5 Sprints facilitó la priorización
de funcionalidades y la gestión del tiempo de desarrollo.

Las 98 pruebas automatizadas implementadas demostraron que es posible

alcanzar una cobertura significativa en un proyecto universitario. La combinación de

pruebas de caja blanca (40) y caja negra (58) proporcionó una verificación
exhaustiva de la lógica de negocio y los casos de uso.

29
5.1.3 Conclusiones de Impacto Social
La plataforma CampusMarket representa una solución concreta a la

necesidad de un espacio digital seguro para las transacciones entre estudiantes
universitarios. El feed social y el sistema de reputación fomentan la transparencia y
la confianza dentro de la comunidad.

El diseño responsive y el tema oscuro proporcionan una experiencia de

usuario moderna y accesible, adaptada a las preferencias actuales de los
estudiantes universitarios.
5.2 Recomendaciones
5.2.1 Recomendaciones Técnicas
• Implementar notificaciones push utilizando Firebase Cloud Messaging para

alertar sobre nuevos mensajes y comentarios.

• Migrar a Supabase como backend alternativo para tener control total sobre

la base de datos y evitar vendor lock-in.

• Implementar un sistema de caché más robusto con cola de sincronización

para operaciones offline.

• Agregar pruebas de integración con Firebase Emulator Suite para validar el

comportamiento real de la base de datos.
•

Implementar CI/CD con GitHub Actions para ejecutar pruebas

automáticamente en cada push.

5.2.2 Recomendaciones Funcionales
• Agregar categorías para productos (Apuntes, Libros, Electrónicos, Ropa,

etc.) con filtro por categoría.
•

Implementar un sistema de calificación con estrellas (1-5) para

compradores y vendedores.

• Agregar lista de favoritos o wishlist para guardar productos interesantes.

• Implementar la funcionalidad de marcar producto como vendido para que

desaparezca del feed.

30
• Agregar edición de productos para permitir actualizar precio, descripción e

imágenes.

5.2.3 Recomendaciones de Seguridad
•

Implementar reglas de seguridad en Firestore (Security Rules) para

restringir el acceso a datos según el rol del usuario.

• Agregar verificación de correo institucional UNIFRANZ para garantizar que

solo estudiantes accedan a la plataforma.
abusos.

• Implementar rate limiting en las operaciones de escritura para prevenir
• Establecer rotación periódica de claves de API y secretos de Firebase.

5.3 Conclusión Final
El desarrollo de CampusMarket demostró que es posible crear una plataforma

de marketplace universitario con red social integrada utilizando tecnologías

accesibles y modernas. React Native y Expo SDK 56, combinados con Firebase
Firestore y Cloudinary, proporcionaron una base sólida para una aplicación que
funciona tanto en dispositivos móviles como en web.

Las 98 pruebas automatizadas implementadas garantizan la calidad del

código y facilitan el mantenimiento futuro. La arquitectura modular permite agregar

nuevas funcionalidades sin afectar los módulos existentes. Este proyecto sienta las

bases para un modelo replicable en otras universidades bolivianas que enfrentan
problemas similares de confianza y seguridad en las transacciones entre estudiantes.

BIBLIOGRAFÍA

Chacon, S., & Straub, B. (2014). Pro Git (2a ed.). Apress.
Cloudinary Documentation. (2026). Cloudinary image and video management.
https://cloudinary.com/documentation

Eisenman, B. (2018). Learning React Native (2a ed.). O'Reilly Media.
Expo Documentation. (2026). Expo SDK 56 documentation. https://docs.expo.dev
Firebase Documentation. (2026). Cloud Firestore.
https://firebase.google.com/docs/firestore

Hurtado, J. (2022). Metodología de la investigación: Guía para la comprensión
holística de la ciencia (5a ed.). Quirón Ediciones.

Instituto Nacional de Estadística. (2026). Comercio electrónico en Bolivia. La Paz,
Bolivia.

Kaur, H., & Sapkota, R. (2024). Online shopping trends among young adults in
Southeast Asia. Centria University of Applied Sciences.

Meta Open Source. (2026). React Native documentation. https://reactnative.dev
pnpm Documentation. (2026). pnpm documentation. https://pnpm.io
Quispe, B. (2023). Sistema web progresivo de comercio electrónico para la empresa
LOGRO [Tesis de grado]. Universidad Mayor de San Andrés.

Schwaber, K., & Sutherland, J. (2024). The Scrum Guide. https://scrumguides.org
Zhang, Y., Li, X., & Chen, W. (2024). Social commerce integration in university

communities: A study of trust and transaction patterns. Journal of Digital
Commerce, 12(3), 42-58.

32
ANEXO

33

34

