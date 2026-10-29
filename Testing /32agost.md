E# Cuadrante Q3 Negocio Critico.
* **Quien lo hace** Qa, Po , usuarios finales
* **que apoya** AL producto asegurando que sea util y usable.
* **Accion del QA** Realiza pruebas exploratorias guiadas por la experiencia del usuario, preguntarse y el usuario hace clic aqui sin querrer
---
![](https://federico-toledo.com/wp-content/uploads/2017/09/Agile-Testing-Quadrants.png)
## ejemplo Q3 (negocio ayuda al producto)
* **historia** el usuario puede ver el historial de pedidos.
* **Pruebas Q3 exploratorias** 
* el Qa se pregunta " Y el usuario no tienen pedidos ? Se muestra un mensaje ?
* Y el usuario tiene  100 pedidos, la pagina carga rapido ?
* puedo ordenar los pedidos por fecha?
* los botones son faciles de encontrar? 
* El diseño es intuitivo o el ususario se perderia
* **Uat:** el PO invia a 5 usuarios reales a probar la fucnionalidad de feedback sobre la experiencia
# El cuadrante Q4 (Tecnico/no funciona)
* **Quien lo hace** especializado en Devops, con apoyo del QA.
* **Que apoya?** Al producto asegurando su supervivencia en produccion.
* **Accion QA** ejecutar pruebas de cargo con Jmeter o pruebas de seguridad con OWASP ZAP.
## Prubas de Q4
* **Rendimiento/carga** el QA usa Jmeter para simular 1000 usuarios haciendo login simultaneamnete. Mide el Tiempo de respuesta, (debe se <2 segundos>)
* **Seguridad** El QA usa OWASP ZAP  para escanear al aplicacion en busca de vulneravilidades (SQL injection, XSS). 
* **Resilencia** EL QA prueba comio se prueba el sistema vuando la base de datos de 100 a 10,000 registros
* **Importancia de los cuadrantes**
---
### tabla de destribucion de esfuerzo
|cuadrante|% de esfuerzo|Quien lo hace|
|---|---|---|
|q1 (unitarias)| 40%| quien lo hace?|
|q2 (funcionales)|30%| QA (manual + automatizacion)|
|q3 (exploratoria)| 20%| QA+PO|
|q4 (no fucnional)| 10%| QA especializados+Devops|
---
### error comun!
en muchos el 80% del esfuerzo esta en q2, el 10% en q3, y el 10% en q1, q4 es inexistente. el resultado: 
* debugs en priduccion por rendimiento y seguridad
---
# Como integrar al QA en el equipo
* **el qa participa en el Daily Scrum** reposta evances, bloqueos y riesgos de pruebas.
* **el Qa participa en el Sprint Plannig** estima el esfuerzo de pruebas y negocia el alcance del Sprint
* **qa participa en las retorspectivas** propone mejoras en el procesode pruebas y en la caliadad del equipo
* **qa participa en el retrospectiva** propone mejoras en el proceso de pruebas y en la caidad del equipo
* **pair testing** el qa y el dev prueba juntos una historia completa
* **code reviews** el qa revisa el codigo del dev y sugiere donde añadir unit test o mejorar la testeabilidad
-  que hace el QA en prevencion son preguntas que hace elQa para el desarolllo cuanto tiempo debed e ser valido de recuperacion.
# El concepto de DEfinition of Ready (Dor)?
- es el conjunto de condiciones que debe cumplir una Historia de Usuarios para que el equipo la considera lsuita para er incluida de un Sprint.
- se especifica **Criterios de aceptacion** que se deben validadr para que la tarea se consideren terminada **Notas** los criterios de aceptacion debe de estar antes de la validacion.
## Condiciones minimas de la Dor desde la vision QA
* **1. Criterios de acpetacion AC, claros y testeables** 
- no vale el sistema debe de ser raido
- vale la pagina de inicio debe de cargar menos de 2 segundos
- no vale el susuario puede iniciar sesion
- vale el susuario puede iniciar sesion con email si la contraseña es incorecta muestra credenciales incorectas.
```bash
Caso 
    1. Datos correctoss
        --> Dashboard
    2. Datos incorectos 
        1. -->usuer bien
           -->pass: mal
        2.  -->user mal
            -->pass bien
            Mensaje de error
```
# Condiciones de la Dor desde la vision qa
* **datos de pruebas definidos**
qque  usuarios exite? que Roles? Que condiciones previas ?. El Qa debe asegurra que los datos necesarios estan disponibilidad o se pueden crear facilmente
* **dependencias externalizadas**
la historia no debe depender de otro quipo o servicios que no este lisrto, si depende de una API externa, debe haber un mosck disponible para pribar.
* **diseno de interfaz** si aplica los mockups o diseños UX deben estar aprobados y accesisbilidad.
* **Notas** en un prueba de sistema en desarrollo no se usan datos reales, solo son de pruebas
# hands On!
- analizar el caso de uso
- como usuario quier poder recuperar mi contraseña cuando la olvide
- realizar las siguientes.
* **Realizar las siguientes tareas**
1. describir un escenario e identificar el error , defecto y fallo.
2. analizar fallo interno y fallo externo.
3. defina al menos 2 caracteristicas de la ISO25010 que estarian siendo afectada y una forma de protegerla.
4. establecer al emnso 2 criterios de aceptacion y sus correspondientes datos de prueba.

![alt text](<assets/WhatsApp Image 2026-08-31 at 20.41.44.jpeg>)
 # Escenario de fallo
 - el usuario solita recuperrar su contraseña 
 - el sistema le indica que le ha enviado un correro con un enlace.
 - el usuario abre el navegador y entra a su correo en un enlace.
 - el ususario ve elcorreo con el enlace le hace clic.
 - el enlace dice tokken inavlido o expiradio
 * **error** ventana de tiempo de 4 minutos
 * **defecto** no se considero el tiempo que se tarda en abrir el correo
 * **fallo** el usuario no puede recuperar su contraseña y se frustra
 ## 1. analisis CoQ - prevencion
 - que pasa si el susuario tarda en revisar su correo?
 - cuanto tiempo debe ser valido el enlace de recuperacion? 
 - existe alguna normativa que sugiere un tiemop razonable de espera? 
 ## 2. analisis de CoQ  Evaluacion
 * **Prueba de expiracin de token**
 - (a) solicita recuperacion
 - (b) espera el tiempo defenido(ej: 5 min)
 - (c) hace clic en el enlace
 
* **Verifica que**
 - 1. el token a un funcione si esta dentro del teimpo.
 - 2. el token expirecorrectamente despues del tiempo.
 - 3. el mensaje de error que sea claro y permita solicitar un nuevo enlace.
 ## 3. Fallo interni analisis CoQ
 - el token expira en 5 minutos, pero los usuarios de nuestra audiencia objetivi(profesionales que revisan correo en horarios especificos) necesitan al menos 2 horas.
 - El quipo ajusta el tiempo a 24 hotas (suegerencia de OWASP) y se vuelve a probar el Sprint se retrasa 1 dia, pero el producto final es usuable.
 ## Analisis de CoQ falo Externo
 * **Bug lelga a produccion**
 - los usuarios registra en redes sociales "la recuperacion de contraseña de esa app e sun chiste, el enlace expira antes de que abra el correo".
 - EL soporte tecnico reciebe cientos de llamadas.
 - los usuarios frsutarados abandonan la app.
 - la app pierde ingresos y reputacion
 ### QUe caracteristicas de la ISO25010 afectada?
 * **funcionalidad** esta afectada por unrequisito no funcional.
 - la **seguridad** el tokken puedes volver en la que no se reuse el token despues de uasarce.
 - vereficae que el sistema envia el correo de recuperacion **exactamente** al correo registrado del usuario, no a otro.
 ## EN que afecta la seguridad ISO25010 afectada
 - **Dimension Seguridad**
 - Como prevenir?
 - Vereficar que el mensaje sea generico SI el correo existe, te enviaremos un enlace de recuperacion, Evitar exponer la existencia del correo.
 - vereficar que el token sea aleatorio, de larga longitud(>= 32 caracyteres) y este encriptado en enlace (no sea predecible como ? token=123).
 - Verificar que el tokken se invalide despoues de:
 1. tiempo de expiracion.
 2. cambio de contraseña exitosa
 3. nueva solicitud de recuperacion
 ## Criterios de Aceptacion
 los criterios de aceptacion deben de ser espeficos claras y notables.
 -  EL usuario esta en la pagina de inicon de session, cuando hace clic en. Olvidaste tu contraseña?. entoces el sistemadebe mostrar un formulario con un uncio campo de texto. Correo eletronico registrado", un button "Enviar enlace de recuperacion.
 ## Criterios de Acepatacion
 - **AC-1 datos de rueba**
 - Navegador Chromev12, Firefox, Safari.
 - Dispositivos: PC, tablet, movil, (iphone, samsung)
 - el enlace . Olvidaste tu conteraseña ?. debe ser visible y funcional en todos los casos.