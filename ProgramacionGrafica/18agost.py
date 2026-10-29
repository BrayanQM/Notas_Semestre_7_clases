import pygame
import sys

pygame.init()

WIN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tic Tac Toe Brayan")

FONDO = (10, 10, 30)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 128, 255)
BLANCO = (255, 255, 255)

GROSOR = 3

tablero = [["" for _ in range(3)] for _ in range(3)]
turno = "X"
juego_terminado = False

# Centros de cada celda: fila 0,1,2 y columna 0,1,2
CENTROS = [
    [(200, 300), (400, 300), (600, 300)],
    [(200, 300), (400, 300), (600, 300)],
    [(200, 300), (400, 300), (600, 300)],
]
# Coordenadas correctas por celda (col, fila)
CENTROS = {}
for fila in range(3):
    for col in range(3):
        cx = 200 + col * 200
        cy = 300 - 100 + fila * 100
        CENTROS[(fila, col)] = (cx, cy)


def obtener_celda(x, y):
    for fila in range(3):
        for col in range(3):
            cx, cy = CENTROS[(fila, col)]
            if cx - 100 < x < cx + 100 and cy - 100 < y < cy + 100:
                return fila, col
    return None


def verificar_ganador():
    for i in range(3):
        if tablero[i][0] and tablero[i][0] == tablero[i][1] == tablero[i][2]:
            return True
        if tablero[0][i] and tablero[0][i] == tablero[1][i] == tablero[2][i]:
            return True
    if tablero[0][0] and tablero[0][0] == tablero[1][1] == tablero[2][2]:
        return True
    if tablero[0][2] and tablero[0][2] == tablero[1][1] == tablero[2][0]:
        return True
    if all(tablero[f][c] for f in range(3) for c in range(3)):
        return "empate"
    return False


def dibujar_tablero():
    WIN.fill(FONDO)
    pygame.draw.line(WIN, ROJO, (100, 200), (700, 200), GROSOR)
    pygame.draw.line(WIN, VERDE, (100, 400), (700, 400), GROSOR)
    pygame.draw.line(WIN, AZUL, (300, 100), (300, 500), GROSOR)
    pygame.draw.line(WIN, ROJO, (500, 100), (500, 500), GROSOR)


def dibujar_x(cx, cy):
    pygame.draw.line(WIN, BLANCO, (cx - 40, cy - 80), (cx + 40, cy), 5)
    pygame.draw.line(WIN, BLANCO, (cx + 40, cy - 80), (cx - 40, cy), 5)


def dibujar_o(cx, cy):
    pygame.draw.circle(WIN, AZUL, (cx, cy), 40, 5)


def dibujar_marcas():
    for fila in range(3):
        for col in range(3):
            valor = tablero[fila][col]
            cx, cy = CENTROS[(fila, col)]
            if valor == "X":
                dibujar_x(cx, cy)
            elif valor == "O":
                dibujar_o(cx, cy)


def reiniciar():
    global tablero, turno, juego_terminado
    tablero = [["" for _ in range(3)] for _ in range(3)]
    turno = "X"
    juego_terminado = False


WIN.fill(FONDO)
dibujar_tablero()
pygame.display.update()

jugando = True

while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

        if event.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
            x, y = pygame.mouse.get_pos()
            celda = obtener_celda(x, y)
            if celda:
                f, c = celda
                if tablero[f][c] == "":
                    tablero[f][c] = turno
                    resultado = verificar_ganador()
                    if resultado:
                        juego_terminado = True
                    else:
                        turno = "O" if turno == "X" else "X"
            dibujar_tablero()
            dibujar_marcas()
            pygame.display.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reiniciar()
                dibujar_tablero()
                pygame.display.update()

pygame.quit()
sys.exit()
