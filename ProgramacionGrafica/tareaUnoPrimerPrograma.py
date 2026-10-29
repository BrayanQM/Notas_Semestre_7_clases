import pygame
import sys

pygame.init()

ANCHO = 800
ALTO = 600

ventana = pygame.display.set_mode((ANCHO, ALTO))

NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

colores = [ROJO, VERDE, AZUL]
indice_color = 0
color_actual = colores[indice_color]
radio = 50
velocidad = 5

centro_x = ANCHO // 2
centro_y = ALTO // 2

reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    centro_x += velocidad

    if centro_x + radio >= ANCHO or centro_x - radio <= 0:
        velocidad = -velocidad
        radio += 10
        if radio >= 100:
            radio = 20
        centro_x = max(radio, min(ANCHO - radio, centro_x))

        indice_color = (indice_color + 1) % len(colores)
        color_actual = colores[indice_color]

    ventana.fill(NEGRO)

    pygame.draw.circle(ventana, color_actual, (centro_x, centro_y), radio, width=3)
    pygame.draw.circle(ventana, color_actual, (centro_x, centro_y), radio)

    pygame.display.flip()
    reloj.tick(60)
