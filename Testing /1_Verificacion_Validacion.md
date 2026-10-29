# 17 de agosto
la calidad no debe de tener fallos,
  * [1]   **error hu8mano** accion de una persdona al escribir un codigo diseñar implementar unrequesito (ANTES DE ENTREGAR)
  * [2]   **defecto bug** Anomalia en el software causada por un error (despues de la entrega )
  * [3]   **fallo** compprtamiento incorrecto del sistema cuando se ejecuta el efecto (despues de entregar)
  * [4]   **riesgo** posibilidad de que ocurra un fallo con cierto impacto
     **error/defecto** el error es antes de tener el proyecto y el defecto encontrarlo despues.
        **error es humano, el efecto esta en el codigo, el fallo es lo que ve el usario**
        
## Verificacion vs validacion
 
    [requisito cumple]  => [revision] => [verificaion =>]
    [requesitos funcionales]
    #Verificacion
    
* **lo contruimos bien?** fase de pregunta [cumple con lo  que se pidio]
* **como se hace metodo estaticos** 
    * [1] revision de codigo 
    * [2] inspecciones de documentos de requesitos
    * [3] preubas estaticas recorrido mental de codigo sin ejecutarlo
* **ejemplo**:
    al hacer un testing de prueba donde los requerimientos cumple lo que el usario necesita
    
        [programador] programa a base de RF
        [tester]    testea lo del programador
    
* **validacion**
    [validacion usabilidad] la cotruccion de si el proceso de evaluacion de que el sistema satisface las necesidades reales del usuario 
    
* **como se hace metodos dinamicos**
            [1] probar el sorftwaere funcionando
            [2] prueba DE ACPETACION DE USUARIO (uat)
            [3] Pruebas exploratorias
            
            [digite numero] aceptado por testing de 8 digitos
            [codigo][digite numero] ACPETACION por el usario            
# costo de la calidad
[cuanto cuesta un bug?]
* **la ley de boehm**   corregir un defecto en fases tempranas que cuesta 1 unidad de produccion de 100 unidades
![](https://storage.ghost.io/c/e2/0b/e20b1dc7-7596-416c-bbad-2be3126c3a68/content/images/2024/06/costofchangeboehm.jpeg)
* **costo de prevencion** gastos para evitar errores de que sucedan
* **en que invertir**
    * [1] capacitacion del equipo en nuevas tecnologias
    * [2] revisiones formales de codigo(pair programing)
    * [3] definicion de estandar de codifcacion
    * [4] herramientas de analisis estaticos (sonar cube)
* **costos de evalacion**   gastos para medir y revisar que los productos esten bien
* **en que invertir?**
    * [1] ejecucion de pruebas unitarias (por devs)
    * [2] pruebas de integracion y ACPETACION
    * [3] pruebas de siste,as y regresion
    * [4] compra de licencias de herramientas de testing(como jira, xray)
* **costos de fallos internos*** errores dedectados antes de entregar el producto al comprador, desperdicios de material, reparaciones.
* **provoca**
    * [1] tiempo de los desarrolladores arreglados bugs reportados en el sprint
    * [2] reacer funcionalidades por que no cumplian los requisitos
    * [3] tiempom extra(horas extra) para parchear el sistema antes de re;ease
* **costos de fallos externos** errores detectados por el cliente recibir el proeducto
* **ejemplo**
    * [1] perdida de ventas(wl usuario se va ala competencia)
    * [2] quejas al servidorde atencion al cliente ( call center saturado)
    * [3] perdidad de imagen de la marca (mala publicidad de redes sociales)
    * [4] penalizaciones economicas (contratos de nivel servicios-SLA)
# modelo de lalidad ISO 25010
    metricas de calidad
    * **que son la iso 25010**
    * [1] es un estandar intercinakl que difine un modelo de calidad de producto
    * [2] no ayuda a responder : cuanto podemos decir que este software es de calidad
    * [3] se divide en 8 caracter , Un software de calidad debe de cumplir con ellas.
    
* **funcionales hace lo que debe?**
    * [1] capacidades del producto para proporcionar funciones de satisfaccion explicita y emplicita
    * [2] son las prubas funcionales
    * [3] verifica que la hcer clic en " agregar a; carrito", el producto aparece en el carrito.
# eficiencia de rendimiento
    * [1]capacidades del producto para proporcionar un rendimiento adecuado , en relacion con la cantidad de recursos utilizados(tiempo, memoria).
    * [2]son las pruebas de carga y estres
    * [3]verificar que 1000, hacer login a la vez sin que el servidor tarde mas de 2 segundos en responder.
    **nota** la variable deve vivir mientras necesite existir, creacion de variables en la    que evite el cosumo de memoria, antes de un for antes de una funcion, esas son una de las buenas practicas, poir ejemplo en software embebebido es notable el consumo de memoria.

# compatibilidad  funciona en todos lados
    * [1]capacidad del producto para inetercambiar informacion con otros sistemaS Y/O ejecuatrce en diferentes entornos.
    * [2]pruebas de integracion y pruebas de navegacion
    * [3]probar la weben chrome, firefos, edge, safari, como tambien en apks de android
#  usabilidad es facil de usar?e4
    * [1]capacidad del producto para ser comprendido aprendido, usando y ser atractivo apara el usuario
    * [2]pruebas de UX/UI y pruebas exploratorias
    * [3] un usarion nuevo puede completar el registro en menos de 2 minutos sin leer el manual?, los botones tienen el tamaño adecuado para und edo movil.
# fiabilidad la informacion se guarda correctemente
    * [1]capacidad del producto para mantener su nivel de rendimiento cuando se usa bajo conduciones especificas durante un perido
    * [2]pruebas de recupercacion y robustez
    * [3] que pasa si se cuerta ;a luz mientras el sistema guarda un pedido?, se corrompe de datos?, el sistema se recuperra todo?, (pruebas de diasaster recovery)
**notas** diferncial es el que se gaurda de la anterior copia al actual
        total es una copia completa de la base.
# seguridad, es protegido
    * [1]capacidad del producto para proteger la informacion y los datos
    * [2]pruebas de seguridad (OWASP top 10)
    * [3]intentar inyectar un campo de busqueda(OR 1 = 1) intentar acceder a la url del admin sin estar logeado
**nota** el codigo duro 
    
# mantenibilidad
* [1] capacidad del producto para ser modificado, eficaz y eficiente
* [2]analisis de deuda yecnica y prubas de regresion al hacer cambios
* [3] si cambiamos el porcentaje de IVA del 21% al 22% cuantas linias de codigo hay que tocar si esta centrealizado en una constante, es mantenible, si esta repetido en 100 sitios, no lo es.
# protabilidad 
* [1]capaciadad del producto para ser transferido de un entorno hadware, software o de uso a otros
* [2]prueas de instalacion y configueracion
* [3]usar aplicacion de servidpor windows a un linux la instalacion es sencilla 
**notas** principiso de certificado ISTQB
# principios ISTQB
* [1] istqb (inernacional de software testing) que da pasos a leyes que todo tester debe de conocer
* **testing muestra la presencia de efectos** no ausencia para todas las pruebas , no bugs no hemos encontrado lo que tenemos
* **rs imposible usar todo** usamos analisis de riesgo priorizar lo mas critico y lo que mas falla
* **pruebas tempranas** involucrar a lso tester desde el inicio de los proyectos
* **agrupacion de efectos** pocos modulos concentran la mayoria de los bugs se debe ana;lizar los modulos criticos
# los 7 principios del testing
* **paradoja pestecida** : si repites las mismas pruebas, dejan de encontrar nuevos bugs, se debe de revisar, modificar y crear nuevas pruebas regulamente/
* **el testing depende del contexto** no es lo mismo probar un videojuego que un isstema medico o una rede social: depende del dominio y del riesgo
* **la ausencia de errores es una falacia** el software puede funcionar bien pero no cumplir las necesidades del negocio, es preferible con bugs pero que resuelva el problema.
