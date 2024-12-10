import os
import random

import cv2
import pygame

from dinh_nghia import Dinh_nghia
from game import Game

pygame.init()
goi_ham_dinh_nghia = Dinh_nghia()
pygame.display.set_caption("BTL_memory_game")
screen = goi_ham_dinh_nghia.screen
fps = goi_ham_dinh_nghia.FPS
clock = pygame.time.Clock()
running = True

game = Game()
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    game.update(event_list)
    pygame.display.update()
    clock.tick(fps)
