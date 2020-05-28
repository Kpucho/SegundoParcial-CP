import pygame
import random
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
        return (self.rect.y + TamVias/4)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.velx = 0
        self.vely = 0

    def update(self):
        self.rect.x += self.velx

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, posy, Mamada):
        pygame.sprite.Sprite.__init__(self)
        self.isMamado = Mamada
        self.image = pygame.Surface([50,50])
        if (self.isMamado == True):
            self.image.fill(ROJO)
        else:
            self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
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
        self.temp = 0
        self.impacto = False
        # self.bloques = None

    def update_vel(self):
        if not self.impacto:
            if j.vely > 0:
                j.vely = j.rapidez
            elif j.vely < 0:
                j.vely = - j.rapidez

            if j.velx > 0:
                j.velx = j.rapidez
            elif j.velx < 0:
                j.velx = - j.rapidez
        else:
            if self.temp == 0:
                self.impacto = False
            else:
                self.temp -= 1

    def update(self):
        self.rect.x += self.velx

        self.rect.y+=self.vely

        #Franjas negras
        if self.rect.bottom >= Vias[5]:
            self.vely=0
            self.rect.bottom = Vias[5]
        if self.rect.top <= Vias[0]:
            self.vely=0
            self.rect.top = Vias[0]

        #Penalizacion por fango o arena
        if self.rect.top <= Vias[1] and self.rect.bottom >= Vias[0]:
            self.rapidez = 2
        elif self.rect.top <= Vias[5] and self.rect.bottom >= Vias[4]:
            self.rapidez = 2

        elif self.rect.top > Vias[0] and self.rect.bottom < Vias[5]:
            self.rapidez = 7

        self.update_vel()

    def reducevel(self):
        self.Temp = 10
        self.impacto = True
        self.rapidez = 1


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
                if g.Type == "Enemys":
                    e = Enemy(g.getPosGenetation())
                    e.velx = -5
                    Enemys.add(e)
                    g.temp = random.randrange(Temp0,Temp1)
                if g.Type == "Obstaculos":
                    if (random.randrange(101) <= 50):
                        Mamada = True
                    else:
                        Mamada = False
                    o = Obstaculo(g.getPosGenetation(),Mamada)

                    o.velx = -2 #Velocidad de desplazamiento del mundo // para remplazar
                    Obstaculos.add(o)
                    g.temp = random.randrange(2*Temp0,3*Temp1)

        """Eliminacion de enemy fuera de pantalla y Colisionessss"""
        for e in Enemys:
            Ls_Enemys = pygame.sprite.spritecollide(e,Jugadores,False)
            impacto = False

            if e.rect.right < 0:
                Enemys.remove(e)

            for j in Ls_Enemys:
                if not impacto:
                    e.image.fill(LIGHT_PINK)
                    j.reducevel()
                    print j.vida
                    j.vida-=1
                    """INFO de jugador"""
                    impacto = True

        for o in Obstaculos:
            Ls_Obs = pygame.sprite.spritecollide(o,Jugadores,False)
            impacto = False

            if o.rect.right < 0:
                Obstaculos.remove(o)

            for j in Ls_Obs:
                if o.isMamado == True:
                    if not impacto:
                        o.image.fill(LIGHT_PINK)
                        j.reducevel()
                        print j.vida
                        j.vida-=1
                        print "golpe"
                        """INFO de jugador"""
                        impacto = True

                if o.isMamado == False:
                    if not impacto:
                        o.image.fill(VERDE)
                        j.reducevel()
                        impacto = True

        for j in Jugadores:
            if j.vida < 0:
                """Sonido perro de muerte"""
                print "Fin del juego"
                #fin_juego = True

        Jugadores.update()
        Enemys.update()
        Obstaculos.update()
        Generadores.update()
        #Dibujado
        ventana.fill(NEGRO)

        """Dibujado del mundo recorrible"""
        for v in Vias:
            pygame.draw.line(ventana, BLANCO, [0, v], [ANCHO, v])

        Jugadores.draw(ventana)
        Enemys.draw(ventana)
        Obstaculos.draw(ventana)
        Generadores.draw(ventana)
        pygame.display.flip()
        reloj.tick(FPS)
