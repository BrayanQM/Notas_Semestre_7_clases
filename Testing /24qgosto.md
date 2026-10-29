# ESTARTEGIA DE TESTEO 24 de agosto
* **Shift-left** el testeo crece al igual que Boehm.
* **ejemplo**
### imagen
![screenshot](https://storage.ghost.io/c/56/e6/56e6bee2-64b3-46fc-9f38-839cefa57dd7/content/images/2023/04/image1-1.png)

* **preubas estaticas** Revision de Requerimientos, especificaciones y codigo antes de ejecutar.
* **ejemplo*
BDD (Behavier Driver Development)/ escrie escenarios de prueba en lenguaje natural antes de que el desarolllador escriba el codigo/
## La piramide de pruebas
```bash
            PRUEBAS EXPLORATORIOS    
            PRUEBAS AUTOMATIZADAS son las pruebas mas caras , debiles
            PRUEBAS DE ACEPTACION Apis
            PRUEBAS UNITARIAS
```
![](https://abstracta.us/es/wp-content/uploads/2019/12/piramide-automatizacion-pruebas-funcionales-mike-cohn-1024x559.png)
* **Notas** pruebas de funcionalidad/ en la que se hacen pruebas pequeñas de todas que se le esten desarrollando. 
1. Son rapidas
2. baratas
3. se ejecuta por DEVS
## El anti patron "copa de helado"
```bash
            preubas exploratorias
            PRUEBAS AUTOMATIZADAS
            PRUEBAS INTEGRACION DE COMPONENTES
            PRUEBAS UNIT
```
* **notas** en esta prueba se encargan mas en la parte de visualizacion del usuario/ error comun en equipos pequeños y novatos muchas pruebas UI en la que este piramide es la incorecta
## El rol de analista de calidad Tester
| Tradicional | Agil |
| --- | --- |
| **Enemigos** Equipos de preubas separado | Parte del quipo discriptivo |
| Se hacen las pruebas al funcional | las pruebas son atarvez del desarrollo |
| trabajan solos | Colaboran con el Dev, Ops, Stanholders |
| actuan como filtros para detectar bugs | **Consejos** detectan y evitan bugs , levantan riesgos |
| No tiene contacto con el negocio | contacto diractemente con el negocio |
| No tienen idea de la planificacion | Participa activamente del relase y sprint planning |

# cuadrates
### imagen
![alt text](https://federico-toledo.com/wp-content/uploads/2017/09/Agile-Testing-Quadrants.png)
### ejemplo
el carrito debe de poder calcular el numero de sprints por cada compra aplicando un descuento de 10%
| p | articulos | precio | decuento | total |
| --- | --- | --- | --- | --- |
| p1 | 3 articulos | 10bs | 10% | 27bs | 
| p1 | 0 articulos | 10%  | 0 |0bs
| p1 | 3 articulos | 10bs | 100% | 0bs |
### ejemplo 02
* **ejemplo** como usuario registrado quiero iniciar session con mie email (e), y contraceña (c)

| valor  | signo  | valor  | resultado | resultado | mensaje |
| --- | --- | --- | --- | --- | --- |
| e = v | ^ | c | = v | camino feliz | dashboard |
| e = f | ^ | c | = v | mensaje | correo no regisrado |
| e = v | ^ | c | = f | mensaje | contraceña incorecta|
| e = f | ^ | c | = f | mensaje | correo no registrado|
| e = f | ^ | c | Num intentos | mensaje |  bloquear mensaje temporalmente |
# Ejemplo 2 Q (negocio apoya al erquipo)
* **hitorial** como usuario registrado quiero iniciar session con mi coreo y contrseña
* **criterios de aceptacion** 
1. con email y contraseña rederige a dashboard
* **Pruebas Q2** las  pruebas ejecuta 4 ACs manualmente en 


