## convertir varias imagenes en un solo archivo .csv (para Google Colab)

esta instruccion es para correr el codigo en Google Colab, cada bloque ```py``` es una celda separada, osea pegas un bloque en cada celda nueva de colab y las vas ejecutando en orden.

lo que hace el codigo:
* toma todas las imagenes de la carpeta **fruits**
* las convierte a escala de grises **GRAY**
* las reducir a tamaño **88px * 88px** (88 pixeles)
* al tener el tamaño reducido se convierte en **Vector** por fila, como son 88*88 el vector debe dar **7744** valores
* al final del vector se le agrega el numero de la carpeta (ej: banana = **1**, kiwi = **2**, mango = **3**, papaya = **4**, peach = **5**) osea el vector de banana queda **7744 + 1 = 77441**
* al final todo se guarda en un archivo **.csv**

formato de las carpetas y su numero:
1. Banana1
2. Kiwi2
3. Mango3
4. Papaya4
5. Peach5

## como subir los archivos a colab

* subes la carpeta **fruits** a google drive
* en colab montas google drive y ya apuntas a la ruta
* o si no, puedes subir el zip directo a colab con `files.upload()`

---

## celda 1 - imports
```py
#imagen para convertir una imagen a vector matris de fila
import cv2
import numpy as np
import os
import csv
from google.colab import files
```

## celda 2 - montar google drive
```py
#1 Montar google drive para usar la carpeta fruits
from google.colab import drive
drive.mount('/content/drive')

#2 Ruta donde esta la carpeta fruits (cambiala si la tienes en otra parte)
RUTA_FRUTAS = "/content/drive/MyDrive/fruits"
```

si no quieres usar drive, usa esta otra celda subiendo un zip:
```py
#1 Subir el zip con las imagenes y descomprimirlo
from google.colab import files
import zipfile

zip_subido = files.upload()          # te sale el cuadro para elegir el zip
nombre_zip = list(zip_subido.keys())[0]

with zipfile.ZipFile(nombre_zip, 'r') as z:
    z.extractall("fruits_zip")

#2 Ruta donde quedaron las imagenes
RUTA_FRUTAS = "fruits_zip/fruits"
```

## celda 3 - configuracion de carpetas y tamaño
```py
#1 Tamaño de la imagen, 88 pixeles por lado
TAMANIO = 88
PIXELES = TAMANIO * TAMANIO          # 88*88 = 7744

#2 Las carpetas con el numero que le asignamos a cada fruta
#   el orden es importante porque ese numero va al final del vector
CARPETAS = [
    ("Banana", 1),
    ("Kiwi",   2),
    ("Mango",  3),
    ("Papaya", 4),
    ("Peach",  5),
]

#3 Verificar que la carpeta existe y mostra las carpetas encontradas
print("carpeta base:", RUTA_FRUTAS)
for carpeta, numero in CARPETAS:
    ruta = os.path.join(RUTA_FRUTAS, carpeta)
    if os.path.isdir(ruta):
        total = len([f for f in os.listdir(ruta) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
        print(f"{carpeta} -> numero {numero} -> {total} imagenes")
    else:
        print(f"NO EXISTE: {ruta}")
```

## celda 4 - la funcion que convierte una imagen en vector
```py
#1 Cargar imagen a colores
#2 Covertir a blanco y negro a esacalas de grisis
#3 Reducir a 88px * 88px
#4 Convertir en vector por fila (7744 valores) y agregar al final el numero de la carpeta
def imagen_a_vector(ruta_imagen, numero):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        return None

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    reducida = cv2.resize(gris, (TAMANIO, TAMANIO), interpolation=cv2.INTER_AREA)

    vector = reducida.flatten().tolist()   # 7744 valores por fila
    vector.append(numero)                  # el numero de la carpeta al final, ej: 77441

    # nombre de salida igual que el de la imagen pero con el numero, ej: Banana_0.png.1
    nombre = os.path.basename(ruta_imagen) + "." + str(numero)
    return nombre, vector
```

## celda 5 - recorrer todas las carpetas y todas las imagenes
```py
#1 lista donde se guardan todos los renglones del csv
filas = []
errores = []

#2 recorrer cada carpeta en el orden que definimos
for carpeta, numero in CARPETAS:
    ruta_carpeta = os.path.join(RUTA_FRUTAS, carpeta)
    if not os.path.isdir(ruta_carpeta):
        continue

    #3 tomar las imagenes una por una, ordenadas para que siempre salga igual
    imagenes = sorted([f for f in os.listdir(ruta_carpeta)
                       if f.lower().endswith((".png", ".jpg", ".jpeg"))])

    for imagen in imagenes:
        ruta = os.path.join(ruta_carpeta, imagen)
        resultado = imagen_a_vector(ruta, numero)
        if resultado is None:
            errores.append(ruta)            # si la imagen no se pudo leer se anota
            continue

        nombre, vector = resultado
        filas.append([nombre] + vector)

    print(f"{carpeta} listo, llevo {len(filas)} vectores")

print("total de vectores:", len(filas))
print("imagenes con error:", len(errores))
```

## celda 6 - guardar el archivo .csv
```py
#1 nombre del archivo de salida
NOMBRE_CSV = "matriz_imagenes_frutas.csv"

#2 el encabezado es: nombre, 0, 1, 2, ... hasta 7743, y la etiqueta al final
encabezado = ["nombre"] + [str(i) for i in range(PIXELES)] + ["etiqueta"]

#3 escribir el csv con todas las filas
with open(NOMBRE_CSV, "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(encabezado)
    escritor.writerows(filas)

print("archivo guardado:", NOMBRE_CSV)
print("total de filas:", len(filas))
print("columnas por fila:", len(encabezado))   # debe dar 7746
```

## celda 7 - revisar y descargar el csv
```py
#1 ver las primeras filas del csv
with open(NOMBRE_CSV, "r") as f:
    for i, linea in enumerate(f):
        print(linea[:120], "...")
        if i >= 3:
            break

#2 descargar el archivo a tu compu
files.download(NOMBRE_CSV)
```

## resultado esperado
* un archivo **matriz_imagenes_frutas.csv**
* cada fila es una imagen: el nombre, los **7744** pixeles en escala de grises y al final el **etiqueta/numero** de la carpeta
* ejemplo Banana: el vector terminaria en **77441** (7744 pixeles + el numero 1)
* ejemplo Peach: el vector terminaria en **77445** (7744 pixeles + el numero 5)
