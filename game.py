import pygame
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,40])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO/2

    def Right(self):
        self.rect.x = 200

    def Left(self):
        self.rect.x = 100

    def update(self):
        pass

"""                                                 WORLD                                                       """
def World():
    pass

def draw_text(msj, font, color, surface, cord):
    object = font.render(msj, True, color)
    surface.blit(object, cord)


if __name__ == '__main__':

    ventana = pygame.display.set_mode([ANCHO,ALTO])

    """                                             MENU                                                        """
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


    """                                              JUEGO                                                       """
    musica.stop()

    Jugadores = pygame.sprite.Group()

    J = Player()
    Jugadores.add(J)

    reloj = pygame.time.Clock()
    fin_juego = False
    while not fin and (not fin_juego):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    J.Right()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    J.Left()



        #CONTROL
        Jugadores.update()
        ventana.fill(NEGRO)
        Jugadores.draw(ventana)
        pygame.display.flip()
        reloj.tick(FPS)
