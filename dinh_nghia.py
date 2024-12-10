import pygame


class Dinh_nghia:
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 860
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # mau me
        self.WHITE = "#edede9"
        self.RED = "#c1121f"
        self.BLACK = "#0a0908"
        self.FPS = 120
