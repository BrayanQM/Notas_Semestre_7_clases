#imagen para convertir una imagen a vector matris de fila
import cv2
import numpy as np 
#1 Cargar imagen a colores
imagen = cv2.imread("linusTorvalds.png")
#2 Covertir a blanco y negro a esacalas de grisis
gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)