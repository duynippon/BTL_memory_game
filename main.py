import pygame

from dinh_nghia import Dinh_nghia
from game import Game

pygame.init()
goi_ham_dinh_nghia = Dinh_nghia()
WINDOW_WIDTH = goi_ham_dinh_nghia.WINDOW_WIDTH
WINDOW_HEIGHT = goi_ham_dinh_nghia.WINDOW_HEIGHT
screen = goi_ham_dinh_nghia.screen
pygame.display.set_caption("Memory Game")

WHITE = goi_ham_dinh_nghia.WHITE
RED = goi_ham_dinh_nghia.RED
BLACK = goi_ham_dinh_nghia.BLACK

FPS = goi_ham_dinh_nghia.FPS
clock = pygame.time.Clock()

game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update(event_list)

    pygame.display.update()
    clock.tick(FPS)
