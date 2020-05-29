import pygame
from config import *
import random


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
        if self.Type == "Enemys":
            self.temp = random.randrange(Temp0,Temp1)
        elif self.Type == "Obstaculos":
            self.temp = random.randrange(2*Temp0,3*Temp1)
        elif self.Type == "Modificadores":
            self.temp = random.randrange(5*Temp0,10*Temp1)

    def update(self):
        self.temp-=1

    def getPosGenetation(self):
        return self.rect.y

    def getposModifi(self):
        return (Vias[random.randrange(1,3)] + (Vinicial))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posy, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.islife = True
        sprite = random.randrange(0, 4)
        self.image = ENEMIGOS[sprite]
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.rapidez = 1
        self.velx = 0
        self.vely = 0
        self.estado = 0 # animacion 0 izq  1: abajo 2: arriba
        self.life = True
        self.via = posy
        self.tipo = tipo
        self.temp_giro = random.randrange(Temp0,Temp1) #asegurar que sea cada segundo


    def corregir_via(self):
        #No salirse de su carril
        if self.rect.top <= self.via:
            self.estado = 0
            self.vely = 0
            self.rect.top = self.via
        elif self.rect.bottom >= self.via + 128:
            self.estado = 0
            self.vely = 0
            self.rect.bottom = self.via + 128


    def update_giro(self):

        if self.tipo == 1 and self.life:
            if self.temp_giro < 0:
                #Verifica a donde ir
                if self.rect.top <= self.via:
                    self.estado = 1
                    self.vely = self.rapidez + 1
                elif self.rect.bottom >= self.via + 128:
                    self.estado = 2
                    self.vely = - self.rapidez - 1
                self.temp_giro = random.randrange(Temp0,Temp1)
            elif self.vely != 0 and self.estado != 0:
                self.corregir_via()
            else:
                self.temp_giro -= 1
        elif self.tipo == 1 and not self.life:
            self.corregir_via()

    def Dead(self):
        self.life = False



    def update(self, fondo_velx):

        self.velx = - self.rapidez + fondo_velx
        self.rect.x += self.velx
        self.rect.y += self.vely

        self.update_giro()



class Obstaculo(pygame.sprite.Sprite):

    def __init__(self, posy, tipo):
        pygame.sprite.Sprite.__init__(self)

        self.life = True
        #tipo 0 es arbol
        #tipo 1 es arbusto
        self.tipo = tipo
        self.color = [BLANCO, VERDE]
        sprite = random.randrange(0, 2)
        self.image = OBSTACULOS[sprite]


        # self.image = pygame.image.load('images/sprites/obstaculos.png')
        # self.image = self.image.subsurface(0, 530, 80, 115)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = posy
        self.velx = 0
        self.vely = 0


    def Dead(self):
        self.life = False

    def update(self, fondo_velx):
        self.velx = fondo_velx
        self.rect.x += self.velx

class Modificador(pygame.sprite.Sprite):

    def __init__(self, posy, type):
        pygame.sprite.Sprite.__init__(self)
        #tipo 0 es vida
        #tipo 1 es x2
        #tipo 2 es inmunidadad
        #tipo 3 es vivacidad
        #tipo 4 es lentitud
        self.tipo = type
        #self.color = [VERDE, DORADO, BLANCO, ROJO, AZUL]
        self.image = MODIFI[self.tipo]
        #self.image = pygame.Surface([32,32])
        #self.image.fill(self.color[self.tipo])

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
        self.animacion = 0
        self.image = DIR[self.animacion]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO/2
        self.velx = 0
        self.vely = 0
        self.rapidez = 5
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
        self.temp_inmunidad = 0

        #modificadores de movimiento
        self.lentitud = False
        self.temp_lentitud = 0

        self.vivacidad = False #Aumento de velocidad con respecto a la base
        self.temp_vivacidad = 0

        self.impacto = False
        self.temp_impacto = 0

        # multiplicador de puntaje
        self.por_dos = False
        self.temp_por_dos = 0
        self.conta_animacion = 3
        self.muerto = False

        self.puntaje = 0

    def update_puntaje (self):
        if self.inmunidad:
            pun_inmunidad = 0
        else:
            pun_inmunidad = 2

        if self.por_dos:
            multiplicador = 2
        else:
            multiplicador = 1

        if self.velx >= 0:
            self.puntaje += multiplicador*((self.rapidez/4) + pun_inmunidad)


    def update_rapidez(self):

        #el aumento de vida y la inmunidad se realiza en colision
        # El modificador de multiplicador de puntaje en la funcion puntaje del juegador
        if not self.impacto:
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

            self.rapidez = valor_camino + valor_lentitud + valor_vivacidad
        else:
            self.rapidez = 2

    def update_vel(self):

        self.temp = 0
        self.impacto = False

        # self.bloques = None

    def update_vel(self):
        if not self.impacto:
            if self.vely > 0:
                self.vely = self.rapidez
            elif self.vely < 0:
                self.vely = - self.rapidez

            if self.velx > 0:
                self.velx = self.rapidez
            elif self.velx < 0:
                self.velx = - self.rapidez
        else:
            if self.temp == 0:
                self.impacto = False
            else:
                self.temp -= 1

    def update(self):
        self.rect.x += self.velx
        self.rect.y+=self.vely

        if not self.inmunidad:
            """Direcciones: 1 horizontal, 2 hacia abajo, 3 hacia arriba """
            if self.dir == 1:
                self.image = DIR[self.animacion]
            elif self.dir == 2:
                self.image = DIR2[self.animacion]
            elif self.dir == 3:
                self.image = DIR3[self.animacion]

        else:
            """Direcciones: 1 horizontal, 2 hacia abajo, 3 hacia arriba """
            if self.dir == 1:
                self.image = INMU[self.animacion]
            elif self.dir == 2:
                self.image = INMU2[self.animacion]
            elif self.dir == 3:
                self.image = INMU1[self.animacion]


        if self.animacion < self.conta_animacion:
            self.animacion += 1
        else:
            self.animacion = 0
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

        #Manejo de temporizadores
        if self.inmunidad and self.temp_inmunidad > 0:
            self.temp_inmunidad -= 1
        elif self.inmunidad and self.temp_inmunidad <= 0:
            self.inmunidad = False

        if self.lentitud and self.temp_lentitud > 0:
            self.temp_lentitud -= 1
        elif self.lentitud and self.temp_lentitud <= 0:
            self.lentitud = False

        if self.vivacidad and self.temp_vivacidad > 0:
            self.temp_vivacidad -= 1
        elif self.vivacidad and self.temp_vivacidad <= 0:
            self.vivacidad = False

        if self.impacto and self.temp_impacto > 0:
            self.temp_impacto -= 1
        elif self.impacto and self.temp_impacto <= 0:
            self.impacto = False

        if self.por_dos and self.temp_por_dos > 0:
            self.temp_por_dos -= 1
        elif self.por_dos and self.temp_por_dos <= 0:
            self.por_dos = False


        #Animacion


        self.update_rapidez()
        self.update_puntaje()
        self.update_vel()

    def impacto_jugador(self):
        self.impacto = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sonidos/efectos/choque.wav'))
        self.temp_impacto = 25

    def quitar_vida(self):
        if not self.inmunidad:
            self.vida -= 1
            self.inmunidad = True
            self.temp_inmunidad = 4 * FPS

    def info_jugador(self):
        for v in range(self.vida + 1):
            if self.inmunidad == False:
                ventana.blit(MODIFI[0],[10+64*v,10])
            elif self.inmunidad == True:
                ventana.blit(MODIFI[2],[10+64*v,10])
        if self.por_dos:
            ventana.blit(MODIFI[1],[10,630])

        if self.vivacidad:
            ventana.blit(MODIFI[3],[74,630])

        if self.lentitud:
            ventana.blit(MODIFI[4],[138,630])



"""                          WORLD                                        """

def draw_text(msj, font, color, surface, cord):
    object = font.render(msj, True, color)
    surface.blit(object, cord)

def Juego(ventana):
    pygame.mixer.init(44100, -16, 2, 2048)
    Jugadores = pygame.sprite.Group()
    Generadores = pygame.sprite.Group()
    Enemys = pygame.sprite.Group()
    Obstaculos = pygame.sprite.Group()
    Modificadores = pygame.sprite.Group()

    j = Player()
    Jugadores.add(j)



    """Construcion de generadores"""
    for i in range(6):
        Aux = Vinicial+i*TamVias
        Vias.append(Aux)
        if i < 5:
            if i in carretera:
                G = Generador(Aux, "Enemys")
            else:
                G = Generador(Aux, "Obstaculos")
            Generadores.add(G)

    G = Generador(0,"Modificadores")
    Generadores.add(G)

    #Carga del mapa
    fondojuego = pygame.image.load('carmap.png')
    fondo_info = fondojuego.get_rect()
    fondo_posx = 0
    limFondo = ANCHO - fondo_info[2]
    musica = pygame.mixer.Sound('sonidos/juego.wav')

    reloj = pygame.time.Clock()
    fin_juego = False
    fin = False
    musica.play(-1)
    """Eventos"""
    while not fin and (not fin_juego):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    j.velx = 0
                    j.vely = j.rapidez
                    j.dir = 2

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    j.velx = 0
                    j.vely = - j.rapidez
                    j.dir = 3

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    j.velx = j.rapidez
                    j.vely = 0
                    j.dir = 1

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
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
                    #Probabilidad 60 que salgan arbustos
                    # tipo 1 arbusto tipo 0 arbol
                    o = Obstaculo(g.getPosGenetation(), prob2(60))
                    o.velx = fondo_velx
                    Obstaculos.add(o)
                    g.temp = random.randrange(2*Temp0,3*Temp1)
                if g.Type == "Modificadores":
                    i = prob5(80)
                    m = Modificador(g.getposModifi(), i)
                    m.velx = -fondo_velx
                    Modificadores.add(m)
                    g.temp = random.randrange(1*Temp0,4*Temp1)

        """Eliminacion de enemy fuera de pantalla y Colisionessss"""
        for e in Enemys:
            Ls_Enemys = pygame.sprite.spritecollide(e,Jugadores,False)
            #Verificar importancia de variable impacto
            impacto = False

            if e.rect.right < 0:
                Enemys.remove(e)

            for j in Ls_Enemys:
                if e.life == True and not impacto:
                    e.Dead()
                    j.impacto_jugador()
                    j.quitar_vida()


                    """Actualizar INFO de jugador"""
                    impacto = True

        for o in Obstaculos:
            Ls_Obs = pygame.sprite.spritecollide(o,Jugadores,False)
            impacto = False

            if o.rect.right < 0:
                Obstaculos.remove(o)

            for j in Ls_Obs:
                if o.life == True and not impacto:
                    #Arbol
                    if o.tipo == 0:
                        o.Dead()
                        j.impacto_jugador()
                        j.quitar_vida()
                        # print j.vida

                        """Sonido de golpe perro"""
                        """Actualizar INFO de jugador"""
                    else: # Arbusto
                        o.Dead()
                        j.impacto_jugador()
                    impacto = True

        for m in Modificadores:
            Ls_Modi = pygame.sprite.spritecollide(m,Jugadores,False)

            if m.rect.right < 0:
                Modificadores.remove(m)

            for j in Ls_Modi:
                if m.tipo == 0: #tipo 0 es vida
                    j.vida += 1
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sonidos/efectos/vida.wav'))
                    print j.vida
                if m.tipo == 1: #tipo 1 es x2
                    j.por_dos = True
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('sonidos/efectos/pordos.wav'))
                    j.temp_por_dos = Tx2
                if m.tipo == 2: #tipo 2 es inmunidadad
                    j.inmunidad = True
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('sonidos/efectos/invencible.wav'))
                    j.temp_inmunidad = Tinmu
                if m.tipo == 3: #tipo 3 es vivacidad
                    j.vivacidad = True
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('sonidos/efectos/acelera.wav'))
                    j.temp_vivacidad = Tviva
                if m.tipo == 4: #tipo 4 es lentitud
                    j.lentitud = True
                    pygame.mixer.Channel(5).play(pygame.mixer.Sound('sonidos/efectos/lentitud.wav'))
                    j.temp_lentitud = Tlenti


                Modificadores.remove(m)


        for j in Jugadores:
            if j.vida < 0:
                """Sonido perro de muerte"""
                j.muerto = True
                j.velx = 0
                j.rapidez = 0
                fin_juego = True

        fondo_velx = - j.rapidez
        fondo_posx += fondo_velx

        Jugadores.update()
        Enemys.update(fondo_velx)
        Obstaculos.update(fondo_velx)
        Modificadores.update(fondo_velx)
        Generadores.update()

        #Dibujado
        ventana.fill(NEGRO)
        ventana.blit(fondojuego, [fondo_posx,0])
        Jugadores.draw(ventana)
        Enemys.draw(ventana)
        Obstaculos.draw(ventana)
        Modificadores.draw(ventana)
        Generadores.draw(ventana)
        j.info_jugador()
        pygame.display.flip()
        reloj.tick(FPS)

    musica.stop()
    FinJuego(ventana, j.puntaje)

def FinJuego(ventana, Puntaje):
    pygame.font.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    musica = pygame.mixer.Sound('sonidos/final.wav')
    fuente = pygame.font.Font(None, 40)
    fondo  = pygame.image.load('images/fin_juego.jpg')
    click = False
    musica.play(-1)
    fin = False
    volver = False
    while (not fin) and (not volver):
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        ventana.blit(fondo, [0,0])
        mx, my = pygame.mouse.get_pos()
        draw_text('Puntaje final: ' + str(Puntaje), fuente, BLANCO, ventana, [300, 50])
        draw_text('Satanic Cars Alv', fuente, ROJO, ventana, [300, 650])
        boton1 = pygame.Rect(100, 400, 250, 50)

        boton2 = pygame.Rect(450, 400, 250, 50)
        if boton1.collidepoint((mx, my)):
            if click:
                print "volver a jugar"
                volver = True
        if boton2.collidepoint((mx, my)):
            if click:
                fin = True
        pygame.draw.rect(ventana, LIGHT_ROJO, boton1)
        draw_text('Volver a jugar', fuente, BLANCO, ventana, [120, 410])
        pygame.draw.rect(ventana, LIGHT_ROJO, boton2)
        draw_text('Salir', fuente, BLANCO, ventana, [540, 410])

        click = False

    if not fin:
        musica.stop()
        Juego(ventana)

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
        draw_text('Satanic Cars Alv', fuente, BLANCO, ventana, [300, 50])
        boton1 = pygame.Rect(300, 150, 220, 50)

        boton2 = pygame.Rect(300, 250, 220, 50)
        if boton1.collidepoint((mx, my)):
            if click:
                previo = True
        if boton2.collidepoint((mx, my)):
            if click:
                fin = True
        pygame.draw.rect(ventana, LIGHT_PINK, boton1)
        draw_text('Iniciar', fuente, BLANCO, ventana, [370, 160])
        pygame.draw.rect(ventana, LIGHT_PINK, boton2)
        draw_text('Salir', fuente, BLANCO, ventana, [370, 260])

        click = False

    musica.stop()
    Juego(ventana)
