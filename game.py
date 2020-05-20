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

"""                          WORLD                      """
def World():
    pass


if __name__ == '__main__':
    pygame.init()
    ventana = pygame.display.set_mode([ANCHO,ALTO])

    Jugadores = pygame.sprite.Group()

    J = Player()
    Jugadores.add(J)

    reloj = pygame.time.Clock()
    fin = False
    while not fin:
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
