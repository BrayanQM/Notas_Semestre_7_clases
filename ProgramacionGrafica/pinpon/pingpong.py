import pygame
import random
import sys

# Configuracion general
ANCHO, ALTO = 900, 600
FPS = 60
FONDO = (20, 24, 33)
BLANCO = (235, 235, 235)
ROJO = (231, 76, 60)
AZUL = (52, 152, 219)
NARANJA = (243, 156, 18)
VERDE = (46, 204, 113)
LINEA = (70, 80, 100)

VEL_PALETA = 8
VEL_PELOTA = 6

ROBOT_KEY = pygame.K_r       # Activa / desactiva modo Robots
REINICIAR_KEY = pygame.K_n   # Nueva partida


class Paleta:
    def __init__(self, x, y, ancho=14, alto=110, color=BLANCO):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.vel = VEL_PALETA
        self.es_robot = False
        self.arriba = pygame.K_w
        self.abajo = pygame.K_s

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=6)

    def mover(self, direccion):
        self.y += direccion * self.vel
        self.y = max(0, min(ALTO - self.alto, self.y))

    def mover_robot(self, pelota):
        objetivo = pelota.y - self.alto / 2 + pelota.radio
        if self.rect.centery < objetivo - 8:
            self.y += self.vel - 2
        elif self.rect.centery > objetivo + 8:
            self.y -= self.vel - 2
        self.y = max(0, min(ALTO - self.alto, self.y))


class Pelota:
    def __init__(self):
        self.radio = 12
        self.x = ANCHO / 2
        self.y = ALTO / 2
        self.vx = VEL_PELOTA
        self.vy = VEL_PELOTA
        self.resetear()

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio,
                           self.radio * 2, self.radio * 2)

    def resetear(self, hacia="auto"):
        self.x = ANCHO / 2
        self.y = ALTO / 2
        if hacia == "izquierda":
            self.vx = -VEL_PELOTA
        elif hacia == "derecha":
            self.vx = VEL_PELOTA
        else:
            self.vx = VEL_PELOTA * random.choice([-1, 1])
        self.vy = VEL_PELOTA * random.choice([-1, 1])

    def mover(self):
        self.x += self.vx
        self.y += self.vy

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, NARANJA, (int(self.x), int(self.y)), self.radio)
        pygame.draw.circle(pantalla, BLANCO, (int(self.x), int(self.y)), self.radio, 2)

    def rebotar_pared(self):
        if self.y - self.radio <= 0 or self.y + self.radio >= ALTO:
            self.vy = -self.vy
            self.y = max(self.radio, min(ALTO - self.radio, self.y))
            return True
        return False

    def colisiona_paleta(self, paleta):
        if self.rect.colliderect(paleta.rect):
            if (self.vx < 0 and self.x - self.radio <= paleta.rect.right
                    and self.x > paleta.x) or \
               (self.vx > 0 and self.x + self.radio >= paleta.rect.left
                    and self.x < paleta.x + paleta.ancho):
                self.vx = -self.vx
                desplazamiento = (self.y - paleta.rect.centery) / (paleta.alto / 2)
                self.vy = desplazamiento * 10
                self.vy = max(-12, min(12, self.vy))
                self.vx = (VEL_PELOTA + abs(self.vy) / 6) * (1 if self.vx > 0 else -1)
                return True
        return False


def fuentes(size):
    return pygame.font.SysFont("arial", size, bold=True)


def mostrar_pantalla_inicio(pantalla, reloj):
    fuente_titulo = fuentes(70)
    fuente_info = fuentes(28)
    fuente_peque = fuentes(22)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return
        pantalla.fill(FONDO)
        titulo = fuente_titulo.render("PING PONG", True, BLANCO)
        pantalla.blit(titulo, (ANCHO / 2 - titulo.get_width() / 2, 110))
        lineas = [
            ("ROBOT (azul):  Movimiento automatico", AZUL),
            ("JUGADOR (rojo):  FLECHAS arriba / abajo", ROJO),
            ("ACTIVAR/DESACTIVAR ROBOT:  R", NARANJA),
            ("NUEVA PARTIDA:  N", VERDE),
            ("Presiona ESPACIO para jugar", BLANCO),
        ]
        y = 220
        for texto, color in lineas:
            sup = fuente_info.render(texto, True, color)
            pantalla.blit(sup, (ANCHO / 2 - sup.get_width() / 2, y))
            y += 55
        pygame.display.flip()
        reloj.tick(FPS)


def mostrar_game_over(pantalla, reloj, marcador, gana_azul=True):
    fuente_titulo = fuentes(80)
    fuente_info = fuentes(30)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == REINICIAR_KEY:
                    return
        pantalla.fill(FONDO)
        texto = "GANA EL ROBOT" if gana_azul else "GANA EL JUGADOR"
        sup = fuente_titulo.render(texto, True, AZUL if gana_azul else ROJO)
        pantalla.blit(sup, (ANCHO / 2 - sup.get_width() / 2, 180))
        marc = fuente_info.render("Marcador: {} - {}".format(marcador[0], marcador[1]), True, BLANCO)
        pantalla.blit(marc, (ANCHO / 2 - marc.get_width() / 2, 300))
        rein = fuente_info.render("Presiona ESPACIO para jugar de nuevo", True, VERDE)
        pantalla.blit(rein, (ANCHO / 2 - rein.get_width() / 2, 380))
        pygame.display.flip()
        reloj.tick(FPS)


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ping Pong - Modo Robots")
    reloj = pygame.time.Clock()

    paleta_izq = Paleta(25, ALTO / 2 - 55, color=AZUL)
    paleta_izq.es_robot = True
    paleta_izq.arriba = pygame.K_w
    paleta_izq.abajo = pygame.K_s
    paleta_der = Paleta(ANCHO - 25 - 14, ALTO / 2 - 55, color=ROJO)
    paleta_der.arriba = pygame.K_UP
    paleta_der.abajo = pygame.K_DOWN

    marcador = [0, 0]
    GOL = 10
    pelota = Pelota()
    modo_robot = True
    en_juego = True
    fuente_marcador = fuentes(60)
    fuente_estado = fuentes(26)

    mostrar_pantalla_inicio(pantalla, reloj)

    while en_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_juego = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == ROBOT_KEY:
                    modo_robot = not modo_robot
                    paleta_izq.es_robot = modo_robot
                if evento.key == REINICIAR_KEY:
                    marcador = [0, 0]
                    pelota.resetear()
                    modo_robot = True
                    paleta_izq.es_robot = True

        # Controles manuales
        teclas = pygame.key.get_pressed()
        if paleta_izq.es_robot:
            paleta_izq.mover_robot(pelota)
        else:
            if teclas[paleta_izq.arriba]:
                paleta_izq.mover(-1)
            if teclas[paleta_izq.abajo]:
                paleta_izq.mover(1)

        if teclas[paleta_der.arriba]:
            paleta_der.mover(-1)
        if teclas[paleta_der.abajo]:
            paleta_der.mover(1)

        # Movimiento de la pelota y colisiones
        pelota.mover()
        pelota.rebotar_pared()
        pelota.colisiona_paleta(paleta_izq)
        pelota.colisiona_paleta(paleta_der)

        # Puntos
        if pelota.x - pelota.radio <= 0:
            marcador[1] += 1
            pelota.resetear(hacia="derecha")
        elif pelota.x + pelota.radio >= ANCHO:
            marcador[0] += 1
            pelota.resetear(hacia="izquierda")

        # Dibujo
        pantalla.fill(FONDO)
        pygame.draw.line(pantalla, LINEA, (ANCHO / 2, 0), (ANCHO / 2, ALTO), 3)
        for y in range(10, ALTO, 40):
            pygame.draw.circle(pantalla, LINEA, (ANCHO / 2, y), 5)
        paleta_izq.dibujar(pantalla)
        paleta_der.dibujar(pantalla)
        pelota.dibujar(pantalla)

        marc_sup = fuente_marcador.render("{}    {}".format(marcador[0], marcador[1]), True, BLANCO)
        pantalla.blit(marc_sup, (ANCHO / 2 - marc_sup.get_width() / 2, 15))

        estado_texto = "ROBOT AZUL: ON" if modo_robot else "ROBOT AZUL: OFF"
        estado_sup = fuente_estado.render(estado_texto, True, NARANJA if modo_robot else LINEA)
        pantalla.blit(estado_sup, (ANCHO - estado_sup.get_width() - 25, 15))

        pygame.display.flip()
        reloj.tick(FPS)

        if marcador[0] >= GOL or marcador[1] >= GOL:
            gana_azul = marcador[0] > marcador[1]
            mostrar_game_over(pantalla, reloj, marcador, gana_azul)
            marcador = [0, 0]
            pelota.resetear()
            modo_robot = True
            paleta_izq.es_robot = True

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
