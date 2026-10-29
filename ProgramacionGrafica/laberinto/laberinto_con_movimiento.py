import pygame
# Colores
NEGRO = (0, 0, 0) 
BLANCO = (255, 255, 255) 
AZUL = (0, 0, 255)
impacto = 0;
# Dimensiones de la pantalla
LARGO_PANTALLA  = 800
ALTO_PANTALLA = 600
pul =""
class Kate(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.sheet = pygame.image.load('kate.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.frame = 0
        self.punto = 0
        self.bandera1 = [0,0]
        self.bandera2 = [0,0]
        self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) }
        self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.up_states = { 0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76) }
        self.down_states = { 0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76) }
        self.cambio_x = 0
        self.cambio_y = 0
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    #coliciones
    def cambiovelocidad(self, x, y):
        """ Cambia la velocidad del protagonista. """
        self.cambio_x += x
        self.cambio_y += y
    def ban(self,uno,dos):
        self.bandera2[0]=uno
        self.bandera2[1]=dos
        if(self.bandera2 != self.bandera1):
            print(self.bandera1)
            print(self.bandera2)
            self.punto += 0.5
            self.bandera1[0]=uno
            self.bandera1[1]=dos
    def ban2(self,uno,dos):
        self.bandera2[0]=uno
        self.bandera2[1]=dos
        if(self.bandera2 != self.bandera1):
            print(self.bandera1)
            print(self.bandera2)
            self.punto += 1
            self.bandera1[0]=uno
            self.bandera1[1]=dos
    #fin coliciones
    def update(self, direction):
        self.rect.x += self.cambio_x
        
        # Hemos chocado contra la pared después de esta actualización?
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.paredes, False)
        if lista_impactos_bloques:
            self.ban(self.rect.x,self.rect.y)
        for bloque in lista_impactos_bloques:
            #Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado izquierdo del objeto que hemos tocado-
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            else:
                # En caso contrario, si nos desplazamos hacia la izquierda, hacemos lo opuesto.
                self.rect.left = bloque.rect.right
        # Desplazar arriba/izquierda
        self.rect.y += self.cambio_y

        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.paredes, False)
        for bloque in lista_impactos_bloques:
            # Reseteamos nuestra posición basándonos en la parte superior/inferior del objeto.
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top 
            else:
                self.rect.top = bloque.rect.bottom
        if lista_impactos_bloques:
            self.ban2(self.rect.x,self.rect.y)
        if direction == 'left':
            self.clip(self.left_states)
        if direction == 'right':
            self.clip(self.right_states)
        if direction == 'up':
            self.clip(self.up_states)
        if direction == 'down':
            self.clip(self.down_states)

        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    #def handle_event(self, event):
        
class Pared(pygame.sprite.Sprite):
    """ Pared con la que el Kate puede encontrarse. """
    def __init__(self, x, y, largo, alto):
        """ Constructor para la pared con la que el Kate puede encontrarse """
        #  Llama al constructor padre
        super().__init__()
 
        # Construye una pared azul con las dimensiones especificadas por los parámetros
        self.image = pygame.Surface([largo, alto])
        self.image.fill(AZUL)
 
        # Establece como origen la esquina superior izquierda.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
# Llamamos a esta función para que la biblioteca Pygame pueda autoiniciarse.
pygame.init()
 
# Creamos una pantalla de 800x600
pantalla = pygame.display.set_mode([LARGO_PANTALLA, ALTO_PANTALLA])
 
# Creamos el título de la ventana
pygame.display.set_caption('Test')
 
# Lista que almacena todos los sprites
listade_todoslos_sprites = pygame.sprite.Group()
 
# Construimos las paredes. (x_pos, y_pos, largo, alto)
pared_list = pygame.sprite.Group()
#laterales 4 lados
pared = Pared(0,0,10,600)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
 
pared = Pared(0,0,800,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
 
pared = Pared(0,590,800,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
 
pared = Pared(790,0,10,100)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(790,200,10,400)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)

# paredes del laberinto horizontales
pared = Pared(100,100,300,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(500,100,110,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(0,200,100,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(300,200,200,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(600,200,200,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(200,300,200,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(200,400,110,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(600,400,100,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(500,300,100,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(100,500,100,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(300,500,410,10)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
# paredes del laberinto verticales

pared = Pared(100,200,10,200)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(200,100,10,200)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(300,300,10,100)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(200,400,10,200)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(400,400,10,100)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(500,100,10,300)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(600,0,10,100)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(600,300,10,100)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(700,100,10,200)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
pared = Pared(700,400,10,100)
pared_list.add(pared)
listade_todoslos_sprites.add(pared)
# Creamos al objeto para Kate
protagonista = Kate(32,250)
protagonista.paredes = pared_list
print(protagonista)
listade_todoslos_sprites.add(protagonista)
 
reloj = pygame.time.Clock()
 
hecho = False
while not hecho:
     
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                pul='left'
                protagonista.cambiovelocidad(-3,0)
            elif evento.key == pygame.K_RIGHT:
                pul='right'
                protagonista.cambiovelocidad(3,0)
            elif evento.key == pygame.K_UP:
                pul='up'
                protagonista.cambiovelocidad(0,-3)
            elif evento.key == pygame.K_DOWN:
                pul='down'
                protagonista.cambiovelocidad(0,3)
                 
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                pul='stand_left'
                protagonista.cambiovelocidad(3,0)
            elif evento.key == pygame.K_RIGHT:
                pul='stand_right'
                protagonista.cambiovelocidad(-3,0)
            elif evento.key == pygame.K_UP:
                pul='stand_up'
                protagonista.cambiovelocidad(0,3)
            elif evento.key == pygame.K_DOWN:
                pul='stand_down'
                protagonista.cambiovelocidad(0,-3)
    pygame.display.set_caption("luego de laberinto " + str(protagonista.rect.x) +" "+  str(protagonista.rect.y) +" Impactos "+ str(int(protagonista.punto)))
 
    #protagonista.handle_event(evento)
    pantalla.fill(pygame.Color('gray'))
    pantalla.blit(protagonista.image, protagonista.rect)
    listade_todoslos_sprites.draw(pantalla)
    pygame.display.flip()
    listade_todoslos_sprites.update(pul)

 
    reloj.tick(30)
pygame.quit()
