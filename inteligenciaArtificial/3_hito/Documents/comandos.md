## este es el codigo del ingeniero de la clase de hoy 
```py
#imagen para convertir una imagen a vector matris de fila
import cv2
import numpy as np
```
```py
#1 Cargar imagen a colores
imagen = cv2.imread("linusTorvalds.png")
#2 Covertir a blanco y negro a esacalas de grisis
gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
```
este codigo esta incompleto, pero debes de preparar para monton de archivos 
## siguiente trabajo
* agregar numero a las carpetas en la cual es la siguiente formato.
1. Banana1
2. Kiwi2
3. Mango3
4. Papaya4
5. Peach5
* el orden es importante ya que debe de seguir el siguiente formato  de trabajo ya usando como base el codigo py que describi en la linia 3/12, debe de hacer esto.
1. tomar las imagenes una por una en donde si es posible de manera que todas tomar la imagen y convertirlo en escala de **GRAY**, al tener el tamaño original individual de las imagenes reducir a todas las imagenes a tamaño  de **88px*88px** en si 88 pixeles, al tener el tamaño reducido de la imagen GRAY, se deve de convertir en **Vector**, en donde el vector es por fila cada imagen tiene un vector y como es por carpeta se le debe de nombrar al final el numero de la carpeta ejemplo **Banana/banana_0.png.1** en si el vector debde de numerar al final el nuemro que le asignamos, y como esta el tamaño de 88 pixeles y en vector debe de dar resultado de 7744 y agregar al final el numero de la carpeta 77441 el numero 1 es el ejemplod e las imagenes de banana, etc, despues de tener los vectores se debe de convertir en archivo .csv
