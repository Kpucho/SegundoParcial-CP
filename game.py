import pygame
from config import *


class Generador (pygame.sprite.Sprite):

    def __init__(self, posy, T = "Enemys"):
        pygame.sprite.Sprite.__init__(self)
        self.dir = 0 #direccion Abajo
        self.image = pygame.Surface([100,100])
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.Type = T
        if Type == "Enemys":
            self.temp = random.randrange(Temp0,Temp1)
        elif Type == "Obstaculos":
            self.temp = random.randrange(2*Temp0,3*Temp1)

    def update(self):
        self.temp-=1

    def getPosGenetation(self):
        return self.rect.y

class Enemy(pygame.sprite.Sprite):

    def __init__(self, posy, tipo):
        pygame.sprite.Sprite.__init__(self)

        self.tipo = tipo
        self.color = [AZUL, ROJO]
        self.image = pygame.Surface([64,64])
        self.image.fill(self.color[self.tipo])

        # self.image = pygame.image.load('images/sprites/cars.png')
        # self.image = self.image.subsurface(0, 310, 140, 50)

        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.rapidez = 3
        self.velx = 0
        self.vely = 0
        self.estado = 0 # animacion 0 izq  1: abajo 2: arriba
        self.via = posy
        self.temp_giro = random.randrange(Temp0,Temp1) #asegurar que sea cada segundo


    def update_giro(self):

        if self.tipo == 1:
            if self.temp_giro < 0:
                #Verifica a donde ir
                if self.rect.top <= self.via:
                    self.estado = 1
                    self.vely = self.rapidez
                elif self.rect.bottom >= self.via + 128:
                    self.estado = 2
                    self.vely = - self.rapidez
                self.temp_giro = random.randrange(Temp0,Temp1)
            elif self.vely != 0 and self.estado != 0:
                #No salirse de su carril
                if self.rect.top <= self.via:
                    self.estado = 0
                    self.vely = 0
                    self.rect.top = self.via
                elif self.rect.bottom >= self.via + 128:
                    self.estado = 0
                    self.vely = 0
                    self.rect.bottom = self.via + 128
            else:
                self.temp_giro -= 1



    def update(self, fondo_velx):
        self.velx = - self.rapidez + fondo_velx
        self.rect.x += self.velx
        self.rect.y += self.vely

        self.update_giro()

class Obstaculo(pygame.sprite.Sprite):

    def __init__(self, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([64,64])
        self.image.fill(BLANCO)

        # self.image = pygame.image.load('images/sprites/obstaculos.png')
        # self.image = self.image.subsurface(0, 530, 80, 115)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.velx = 0
        self.vely = 0

    def update(self, fondo_velx):
        self.velx = fondo_velx
        self.rect.x += self.velx

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32,32])
        self.image.fill(VERDE)
        # self.original_image = pygame.image.load('images/sprites/cars3.png')
        # self.image = self.original_image.subsurface(0, 0, 110, 80)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO/2
        self.velx = 0
        self.vely = 0
        self.rapidez = 7
        self.vida = 3
        # self.dir = 1
        # self.bloques = None


    def update_rapidez(self):

        #Penalizacion por fango o arena
        if self.rect.top <= Vias[1] and self.rect.bottom >= Vias[0]:
            self.rapidez = 4
        elif self.rect.top <= Vias[5] and self.rect.bottom >= Vias[4]:
            self.rapidez = 4
        elif self.rect.top > Vias[0] and self.rect.bottom < Vias[5]:
            self.rapidez = 7

    def update_vel(self):

        if j.vely > 0:
            j.vely = j.rapidez
        elif j.vely < 0:
            j.vely = - j.rapidez

        if j.velx > 0:
            j.velx = j.rapidez
        elif j.velx < 0:
            j.velx = - j.rapidez


    def update(self):
        self.rect.x += self.velx

        self.rect.y+=self.vely

        # """Direcciones: 1 horizontal, 2 hacia abajo, 3 hacia arriba """
        # if self.dir == 1:
        #     j.image = j.original_image.subsurface(0, 0, 110, 80)
        # elif self.dir == 2:
        #     j.image = j.original_image.subsurface(224, 0, 120, 80)
        # elif self.dir == 3:
        #     j.image = j.original_image.subsurface(115, 0, 110, 80)


        #Franjas negras
        if self.rect.bottom >= Vias[5]:
            self.vely=0
            self.rect.bottom = Vias[5]
        if self.rect.top <= Vias[0]:
            self.vely=0
            self.rect.top = Vias[0]

        # limites del jugador en pantalla
        if self.rect.left < 30:
            self.rect.left = 30
        if self.rect.right > 650:
            self.rect.right = 650

        self.update_rapidez()
        self.update_vel()



"""                          WORLD                                        """

def draw_text(msj, font, color, surface, cord):
    object = font.render(msj, True, color)
    surface.blit(object, cord)

if __name__ == '__main__':

    ventana = pygame.display.set_mode([ANCHO,ALTO])

    """                       MENU                                        """
    pygame.font.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    fuente = pygame.font.Font(None, 40)
    fondo  = pygame.image.load('images/fondo.png')
    musica = pygame.mixer.Sound('sonidos/menu.wav')
    fin = False
    previo = False
    click = False
    musica.play(-1)
    while (not fin) and (not previo):

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        ventana.blit(fondo, [0,0])
        mx, my = pygame.mouse.get_pos()
        draw_text('Satanic Cars Alv', fuente, BLANCO, ventana, [250, 50])
        boton1 = pygame.Rect(250, 150, 220, 50)

        boton2 = pygame.Rect(250, 250, 220, 50)
        if boton1.collidepoint((mx, my)):
            if click:
                previo = True
        if boton2.collidepoint((mx, my)):
            if click:
                fin = True
        pygame.draw.rect(ventana, LIGHT_PINK, boton1)
        draw_text('Iniciar', fuente, BLANCO, ventana, [320, 160])
        pygame.draw.rect(ventana, LIGHT_PINK, boton2)
        draw_text('Salir', fuente, BLANCO, ventana, [320, 260])

        click = False


    """//////////////                      JUEGO                            ///////////"""
    musica.stop()


    Jugadores = pygame.sprite.Group()
    Generadores = pygame.sprite.Group()
    Enemys = pygame.sprite.Group()
    Obstaculos = pygame.sprite.Group()

    j = Player()
    Jugadores.add(j)

    """Construcion de generadores"""
    for i in range(6):
        Aux = Vinicial+i*TamVias
        Vias.append(Aux)
        if i < 5:
            if i in [1,2,3]:
                Type = "Enemys"
            else:
                Type = "Obstaculos"
            G = Generador(Aux, Type)
            Generadores.add(G)

    #Carga del mapa
    fondojuego = pygame.image.load('carmap.png')
    fondo_info = fondojuego.get_rect()
    fondo_posx = 0
    limFondo = ANCHO - fondo_info[2]


    reloj = pygame.time.Clock()
    fin_juego = False

    """Eventos"""
    while not fin and (not fin_juego):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    j.velx = 0
                    j.vely = j.rapidez
                    # j.dir = 2

                if event.key == pygame.K_UP:
                    j.velx = 0
                    j.vely = - j.rapidez
                    # j.dir = 3

                if event.key == pygame.K_RIGHT:
                    j.velx = j.rapidez
                    j.vely = 0
                    # j.dir = 1

                if event.key == pygame.K_LEFT:
                    j.velx = - j.rapidez
                    j.vely = 0
                    # j.dir = 1



        #CONTROL
        """Activacion generadores"""
        for g in Generadores:
            if g.temp < 0:
                if g.Type == "Enemys":
                    # probabilidad = 30  "enemigo color rojo"
                    e = Enemy(g.getPosGenetation(), prob2(30))
                    e.velx = - e.rapidez
                    Enemys.add(e)
                    g.temp = random.randrange(Temp0,Temp1)
                if g.Type == "Obstaculos":
                    o = Obstaculo(g.getPosGenetation())
                    o.velx = fondo_velx
                    Obstaculos.add(o)
                    g.temp = random.randrange(2*Temp0,3*Temp1)

        """Eliminacion de enemy fuera de pantalla"""
        for e in Enemys:
            if e.rect.right < 0:
                Enemys.remove(e)

        for o in Obstaculos:
            if o.rect.right < 0:
                Obstaculos.remove(o)

        fondo_velx = - j.rapidez
        fondo_posx += fondo_velx

        Jugadores.update()
        Enemys.update(fondo_velx)
        Obstaculos.update(fondo_velx)
        Generadores.update()

        #Dibujado
        ventana.fill(NEGRO)

        ventana.blit(fondojuego, [fondo_posx,0])
        Jugadores.draw(ventana)
        Enemys.draw(ventana)
        Obstaculos.draw(ventana)
        Generadores.draw(ventana)
        pygame.display.flip()
        reloj.tick(FPS)
