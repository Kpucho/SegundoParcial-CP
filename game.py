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
        self.islife = True
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        if self.islife == True :
            self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO

        self.rect.y = posy
        self.rapidez = 3
        self.velx = 0
        self.vely = 0
        self.estado = 0 # animacion 0 izq  1: abajo 2: arriba
        self.via = posy
        self.tipo = tipo
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

    def Dead(self):
        self.islife = False
        self.image.fill(LIGHT_PINK)

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, posy, Mamada):
        pygame.sprite.Sprite.__init__(self)
        self.islife = True
        self.isMamado = Mamada
        self.image = pygame.Surface([50,50])
        if (self.isMamado == True):
            if self.islife == True:
                self.image.fill(ROJO)
        else:
            if self.islife  == True:
                self.image.fill(BLANCO)

        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.velx = 0
        self.vely = 0

    def update(self, fondo_velx):
        self.velx = fondo_velx
        self.rect.x += self.velx

    def Dead(self):
        self.islife = False
        if (self.isMamado == True):
            if self.islife == False:
                self.image.fill(LIGHT_PINK)
        else:
            if self.islife == False:
                self.image.fill(VERDE)

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('images/sprites/cars3.png')
        self.image = self.original_image.subsurface(0, 0, 110, 75)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO/2
        self.velx = 0
        self.vely = 0
        self.rapidez = 7
        self.vida = 3
        self.dir = 1
        self.temp = 0
        self.impacto = False

        # self.bloques = None

        #Modificadores

        # De vida
        #incremento de vida
        #inmunidadad
        self.inmunidad = False
        self.temp_inmunidad = 2 * FPS

        #modificadores de movimiento
        self.lentitud = False
        self.vivacidad = False #Aumento de velocidad con respecto a la base

        # multiplicador de puntaje
        self.por_dos = False

        self.puntaje = 0



    def update_puntaje (self):
        if self.inmunidad:
            pun_inmunidad = 2
        else:
            pun_inmunidad = 0

        if self.por_dos:
            multiplicador = 2
        else:
            multiplicador = 1

        if self.velx >= 0:
            self.puntaje += multiplicador*((self.rapidez/4) + pun_inmunidad)
        print 'puntaje', self.puntaje



    def update_rapidez(self):

        #el aumento de vida y la inmunidad se realiza en colision
        # El modificador de multiplicador de puntaje en la funcion puntaje del juegador


        # En la colision si se coloca uno verdadero, el otro tiene que ser falso
        # modificadores de velocidad
        if self.lentitud:
            valor_lentitud = - 2
        else:
            valor_lentitud = 0

        if self.vivacidad:
            valor_vivacidad = 2
        else:
            valor_vivacidad = 0

        #Penalizacion por fango o arena
        if self.rect.top <= Vias[1] and self.rect.bottom >= Vias[0]:
            valor_camino = 3
        elif self.rect.top <= Vias[5] and self.rect.bottom >= Vias[4]:
            valor_camino = 3
        elif self.rect.top > Vias[0] and self.rect.bottom < Vias[5]:
            valor_camino = 5

        j.rapidez = valor_camino + valor_lentitud + valor_vivacidad


    def update_vel(self):

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

        """Direcciones: 1 horizontal, 2 hacia abajo, 3 hacia arriba """
        if self.dir == 1:
            j.image = j.original_image.subsurface(0, 0, 110, 75)
        elif self.dir == 2:
            j.image = j.original_image.subsurface(224, 0, 120, 75)
        elif self.dir == 3:
            j.image = j.original_image.subsurface(115, 0, 110, 75)

        #Limites de la pantalla
        if self.rect.left <= 0:
            self.velx = 0
            self.rect.left = 0

        if self.rect.right >= ANCHO:
            self.velx = 0
            self.rect.right = ANCHO

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
        self.update_puntaje()
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
    Jugadores = pygame.sprite.Group()


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
    Generadores = pygame.sprite.Group()
    Enemys = pygame.sprite.Group()
    for v in Vias:
        G = Generador(v)
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
                    j.dir = 2

                if event.key == pygame.K_UP:
                    j.velx = 0
                    j.vely = - j.rapidez
                    j.dir = 3

                if event.key == pygame.K_RIGHT:
                    j.velx = j.rapidez
                    j.vely = 0
                    j.dir = 1

                if event.key == pygame.K_LEFT:
                    j.velx = - j.rapidez
                    j.vely = 0
                    j.dir = 1



        #CONTROL
        """Activacion generadores"""
        for g in Generadores:
            if g.temp < 0:
                if g.Type == "Enemys":
                    #prob2 retorna 1 o 0 dependiendo de la probabilidad dada
                    # probabilidad = 30  "enemigo color rojo"
                    e = Enemy(g.getPosGenetation(), prob2(30))
                    e.velx = - e.rapidez
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
                if e.islife == True:
                    if not impacto:
                        e.Dead()
                        j.reducevel()
                        print j.vida
                        j.vida-=1
                        """Sonido de golpe perro"""
                        """Actualizar INFO de jugador"""
                        impacto = True

        for o in Obstaculos:
            Ls_Obs = pygame.sprite.spritecollide(o,Jugadores,False)
            impacto = False

            if o.rect.right < 0:
                Obstaculos.remove(o)

            for j in Ls_Obs:
                if o.islife == True:
                    if o.isMamado == True:
                        if not impacto:
                            o.Dead()
                            j.reducevel()
                            print j.vida
                            j.vida-=1
                            """Sonido de golpe perro"""
                            """Actualizar INFO de jugador"""
                            impacto = True

                    if o.isMamado == False:
                        if not impacto:
                            o.Dead()
                            j.reducevel()
                            impacto = True

        for j in Jugadores:
            if j.vida < 0:
                """Sonido perro de muerte"""
                fin_juego = True

        fondo_velx = - j.rapidez
        fondo_posx += fondo_velx

        """informacion del jugador"""
        for j in Jugadores:
            text = "Vidas: " + str(j.vida)
            draw_text(text, fuente, BLANCO, ventana, [650,0])

        Jugadores.draw(ventana)
        Enemys.draw(ventana)
        Obstaculos.draw(ventana)
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
