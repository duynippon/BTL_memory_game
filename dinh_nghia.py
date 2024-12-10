import pygame


class Dinh_nghia:
    def __init__(self):
        self.WHITE = "#ffffff"
        self.RED = "#c1121f"
        self.BLACK = "#0a0908"
        self.WINDOW_WIDTH = 1280

        self.WINDOW_HEIGHT = 860
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.FPS = 120
