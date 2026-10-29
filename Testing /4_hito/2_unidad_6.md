# Unidad 6 Papel del Tester
## Para que el QA lee la historias
El Qa analiza historias futuras para anticipar
* **Datos de prueba** necesarios hay usuarios de prueba ??, hay Transiciones Semilla 
## Tareas de3 QA en e3 Sprint planning 
el El Sprint plnnig es planecion de sprints **planificar** tambien el uso de se basa a historias, 
1 **Estimar Ezfuerzo de QA en horas/puntos , por historia y por timepo**
tipo de prueba
- Diseño de cassos 
estimar horas de esfuerzos 

POr historia y por prueba 
- Diseño de casos (hrs)
-ejmp manual, o automatica (horas)
-  Regresion de Historias, anteriores.
- documentacion de bugs , (hrs)
- margen para entrevistos (20:30%)
## 2 **Negociar en % de tiempos de sprint en pruebas aut y amnuales**
"Necesitamos 2 hors para actuaizar los sprints rotos del sprint anterior"
## 3. El QA negiocia alcance no solo timepo, si hay sobrecargo, el QA propone
- Reducir el alcance de pruebas (solo critico)
-  Pedir apoyo (mas personal)
-  Devidir las tareas **devidir sprint**
## 4. El qa debe de dejar margen para regresion si hay cambios en modulos existententes
- re-ejecutar casos de scripts (regresion incremental)
* caso embebidos
- la estimacion incluye 
- timepode flasheo
-  montaje
- medicion
**La automatizacion es HLL (hadware in the loop)**
o escrips sobre uart, meno frecuete y mas costosa, 
-  mayor margen (30-40% ) por improvisto de hw
-  la negozacion puede incluir ventas de cesion , de hw (xuando puedo usar la placa)
## tareas del QA durante el script 
1 testing en paralelo pobra apenas se marque Ru
- el fedback llega temprano (el dev corrige durante el sprint)
- el qa nose acumula trabajo para el final 
- si una historia falla, hay tiempo para retrabajarla 
## 2. Smoke testing diariocada mañana
- Snoke flujos criticos, minutos no haras
- antes de empezar el trabajo del dia 
- si falal se detine el pipeline y se alerta el equipo.
## 3 regresion incremental
- no se corre too el codigo
- regresion completa ? al final del script 
## 4  el QA reporta bugs a medida que aparecen bug tiene
- titulo claro, pasos de reproduccion esperados vs rel, severida evidencial (caoturas, log etc)
- prioridad critico (bloquea) mayor afecta (funcionalidad ) 
menor (Cosmetico)


## Para software embebido
testing en paralelo: el dia es mas lento por que se require flasehar, montar, medir se hace la 2 historas por da
- smoke diario verificar que el firware arrancar, que los LEDS de estado enciendan, que uart responde , que el sensor lee.
- Bugss: incluyen condiciones fisicas (temperatura, voltaje, tiempo) evidencia (captura del osciloscopuo o logs de uARt)
# Tareas Del QA
## Tareas de Qa a mitad del sprint (chekpoint)
1. evaluar si vamos a tiempo a mitatd del sprint el QA hace corte de control
2. Cuantosnhistorias se probaron vs cuantas se planearon
3. cuantos bugs criticas / mayores estanabiertas?
4. la regresion incrementalesta al dia
5. la regresion incremental esta al dia
6. la automatizacion avanza o se estanca
## Si hay muchos bugs se alerta al equipo para reducir alcance 
1. trabajr mas horas
2. negociar que se posterg
* **Como?**
- reducir el alcance de pruebas 
- postergar historias de menos valor
- pedir apoyo (pair testing)
- mover automatizacin al prox sprint


El chekpoint es una conversacion, no un cobertura y  el QA **lleva datos** (numeros bugs, cobertura) y **proponen una decision**
el equipo decide
## Tareas del QA al final de Sprint
1. Code Freeze:  apartir de cierto dia no se aceptan mas cmabios de codigo (salvo bugs criticos) para estabilixar el Build para demo/ relase 
**Ejecuta** **Pruebas exploratorias profundas** guiado por heuristica, interupciones 
* Experiencias de usuario: 
1. Que haria un Usuario Torpe?
2. Que hari un usuario malisiioso?


**ejecuta suite completade regresion**
2. Hardning: endureciomienti del producto, Se buscan cassos borde condiciones de estres escenarios no contemplados, 
3. Preparaciiiion de la Demo:
* Verifica que lo que se va mostrar FUNCIONE
* Usa datos Realistas, en el entorno de demo
**Un bug en la demo es un fracaso visible**