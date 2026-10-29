# Que es Automatizar
Uso de software para ejecutaer pruebas, comparar resultados esperados vs, reales y **reportar sin intrvencion humana**
automatizar todo lo repetitivo.
- **Procesi repetitivo**
- el proceso repetitivo debe de ser cofiabe y sostenible.
- el objetivo no es ejecutar mas es **ejecutar lo repetitivo** de forma mas confiable y sostenible.
## Pasos de Pruebas
### **Preparar los datos**
los datos de prueba son YUsuarios en la que podamos probar en donde se usan usuarios de pruebas como **users**.
### **Pruebas Manuales**
* 1. *Preparar Datos*
* 2. *Ejecutar datos*
* 3. *OBserbar los resultados*
* 4. *Comparar Resultados* Tener en mente que lo esperado y lo que se obtiene.
* 5. *Registrar Resultados*
---
Las pruebas automaticos hacen el mismo paso. que las manuales.
## Que No es Automatizar.
Existen herramientas como **Selenium** en la que es posible graar los pasos que realiza elprograma.
---
*Prueba*
- 1. Hacer clic ala textbox user
- 2. ingresar texti user
- 3. clictexbox pass
- 4. ingresar pass
- 5. clic button session
---
### - *Hacer que la maquina haga todo*
La maquina no puede hacer todo
### - *Eliminar completamente al tester*
El tester en donde los que hacen las pruebas lo hacen el de **QA**
### - *Covertir cualquier prueba manual en un script*
Se debe de decir cuando **Automatizar es una decision de ingenieria** 
### *Automatizar las pruebas manuales*

|Ejecucion|Manual|Automatica|
|--|--|--|
|ejecucion|lenta|rapida|
|Costo Inicial|baja|Alta|
|Mantenimiento|baja|Alta|
|Deteccion bugs|Excelente|Pobre|
|regresion|Tediosa|ideal|
|Pruebas Exploratorias|ideal|inviable|
### *Por que Automatizamos?*
1. *Repetitivo*: Una prueba que ejecutamos muchas veces puede ser una buena candidata.

**Ejemplo Repetitivos**
1. login Inicio Session
2. Cerrar Sesion
3. Cambio Contraseña
4. Actualizacion CRUD
5. Sistema de

**Entonces Por que Automatizamos**

**Repeticion**

Una prueba que ejectamos muchas veces oeude ser unavueba candidata.

**Regresion**

Permite volver a ejecutar pruebas despues de cambios

**Velocidad**

Una Maquina Puede ejecutar muchas comprobaciones rapidamente.

**Repetibilidad**

elmismonprocedimineto puede ejecutarse de forma consistente
### EJEMPLO 1
    "UN usuario puede iniciar session corectamente"

1. **Se ejecuta**
- 1 vez

2. **No aprece Un problema**

- 10 veces

3. **Todavia manejable**

- 100 veces

4. **Empieza a ser tedioso**

- 1.000 veces

5. ***Esto Muestra el sentido de automatizar***

### Cuanto Tarda prueba MAnual
*Caso de prueba* "Verificar que un usuario puede inisiar session corectamente"

1. **Prueba MAnual**
2. **Llenar formulario**
- 2 minutos
3.  **Frecuencia**
- 200 ejecuciones
4. **Tiempo Total**
```math
2*200 = 400 minutos
= 6 horas 40 minutos
```
## Automatizar Tambien Cuesta

**Costos iniciales**
- Tiempo del QA
- Diseño del Test
- Programacion
- COnfugurarlo
- datos de prueba
- aprendizaje de herramientas

**Y despues**

- Mantenimiento
## Fallo de test
- El dev Cambia el button *Ingresar* POr *Inicar session*
- el teste fallo por *Error del Test Automatizado*
## La automtizacion como ubversion
**INVERSION**
```math
 Tiempo+desarrollo+mantenimineto
```
**BENEFICIO**
```math
Menor esfuerzo de ejecucion + Mayor Velocidad + Repetibilidad + Regresion mas rapida
```
## ROI Retorno OPtimo de Inversion
```math
ROI = (Beneficio - inversion)/Inversion
```
- No necesitamos convertir todo a dinero

- En testing nos preguntarnos:

- el valor que obtendremos justifica el costo de automatiza y manetner la prueba ?

**CUrva de ROI**
![](https://imgs.search.brave.com/5D7P5k3Pyo2cI7rr2gWxDXgcXbSf2egcafRIKbUd-8k/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jbC5h/YnN0cmFjdGEudXMv/d3AtY29udGVudC91/cGxvYWRzLzIwMjAv/MDQvcmV0b3Juby1p/bnZlcnNpb24tYXV0/b21hdGl6YWNpb24t/cHJ1ZWJhcy5qcGc)

## Cunado SI y Cuando NO
1. **Criterio para Si automatizar**
- repetitiva(Regresion, smoke)
- estable(no cambia cada sprint)
- Critica para el negocio
- condatos variados (data-driven)
- ejecutable sin juicio humano
- de alto volumne

2. **Motivos para No Automatizar**
- cambia mucho (UI en redisiño constante)
- Exploratoria o de usabilidad
- De una sola ejecucion
- Requiere juicio Humano(estetica, UX, accs\esibilidad subjetiva)
- Costo de Automatizar > beneficio esperado
- Pruebas de **una vez en la vida**
## Matriz de decision
|Criterio|Peso|Pregunta|
|--|--|--|
|freceunecia de ejecucion|alta|Cuantas veces se ejecutrara?|
|Estabilidad|alta|cmabia mucho?|
|criticidad| medio| si falla, duele?|
|Complejidad tecnica|medio|es viable automatizarlo?|
|costo de automatizar|alto|cuanto cuesta vs. Beneficios?|

### MORALEJA
NO se debe de automatizar todo, pero vale en partes automatizalo

EL tester que automatiza no ses que graba clics, es el que decide que vale la pena automatizar.
```math
AUTOMATIZAR!=Automatizar- TODO
```
Una buena estrategias de automatizacion busca:
```Math
MAXIMIZAR-EL- VALOR
```
y 
```Math
Minimizar-el-esfuerzo-y-mantenimiento
```
## HASNDS ON!
- Formar grupos de 2 personas y con base en la matriz de desicion
- Cuando no requiere intervencion Humana
##




