import pygame
import random
from config import *

class Generador (pygame.sprite.Sprite):
    def __init__(self, posy):
        pygame.sprite.Sprite.__init__(self)
        self.dir = 0 #direccion Abajo
        self.image = pygame.Surface([100,100])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.temp = random.randrange(Temp0,Temp1)

    def update(self):
        self.temp-=1

    def getPosGenetation(self):
        return (self.rect.y + 25)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.image.fill(LIGHT_PINK)
        self.rect = self.image.get_rect()
        self.rect.x = ALTO
        self.rect.y = posy
        self.velx = 0
        self.vely = 0

    def update(self):
        self.rect.x += self.velx

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32,32])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO/2
        self.velx = 0
        self.vely = 0
        self.rapidez = 7
        self.vida = 3
        # self.bloques = None

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

        #Franjas negras
        if self.rect.bottom >= 600:
            self.vely=0
            self.rect.bottom = 600
        if self.rect.top <= 100:
            self.vely=0
            self.rect.top = 100

        #Penalizacion por fango o arena
        if self.rect.top <= 200 and self.rect.bottom >= 100:
            self.rapidez = 2
        elif self.rect.top <= 600 and self.rect.bottom >= 500:
            self.rapidez = 2

        elif self.rect.top > 100 and self.rect.bottom < 600:
            self.rapidez = 7

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

    j = Player()
    Jugadores.add(j)

    """Construcion de generadores"""
    Generadores = pygame.sprite.Group()
    Enemys = pygame.sprite.Group()
    for v in Vias:
        G = Generador(v)
        Generadores.add(G)


    reloj = pygame.time.Clock()
    fin_juego = False


    while not fin and (not fin_juego):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    j.velx = 0
                    j.vely = j.rapidez
                if event.key == pygame.K_UP:
                    j.velx = 0
                    j.vely = - j.rapidez
                if event.key == pygame.K_RIGHT:
                    j.velx = j.rapidez
                    j.vely = 0
                if event.key == pygame.K_LEFT:
                    j.velx = - j.rapidez
                    j.vely = 0



        #CONTROL
        """Activacion generadores"""
        for g in Generadores:
            if g.temp < 0:
                #Direccion = random.randrange(500)
                e = Enemy(g.getPosGenetation())
                e.velx = -5
                Enemys.add(e)
                g.temp = random.randrange(Temp0,Temp1)

        """Eliminacion de enemy fuera de pantalla"""
        for e in Enemys:
            if e.rect.right < 0:
                Enemys.remove(e)

        Jugadores.update()
        Enemys.update()
        Generadores.update()
        #Dibujado
        ventana.fill(NEGRO)
        pygame.draw.line(ventana, AMARILLO, [0, 100], [ANCHO, 100])
        pygame.draw.line(ventana, AMARILLO, [0, 200], [ANCHO, 200])
        pygame.draw.line(ventana, AZUL, [0, 300], [ANCHO, 300])
        pygame.draw.line(ventana, AZUL, [0, 400], [ANCHO, 400])
        pygame.draw.line(ventana, AMARILLO, [0, 500], [ANCHO, 500])
        pygame.draw.line(ventana, AMARILLO, [0, 600], [ANCHO, 600])
        Jugadores.draw(ventana)
        Enemys.draw(ventana)
        Generadores.draw(ventana)
        pygame.display.flip()
        reloj.tick(FPS)
