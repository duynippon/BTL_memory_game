import os
import random
import time

import cv2
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split(".")[0]

        self.original_image = pygame.image.load("images/aliens/" + filename)

        self.back_image = pygame.image.load("images/aliens/" + filename)
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False


class Game:
    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.game_started = False
        self.remaining_time = 300  # 5 minutes in seconds
        self.start_time = None

        # aliens
        self.all_aliens = [
            f for f in os.listdir("images/aliens") if os.path.join("images/aliens", f)
        ]

        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level(self.level)

        # Initialize fonts
        self.title_font = pygame.font.Font("fonts/Little Alien.ttf", 44)
        self.content_font = pygame.font.Font("fonts/Little Alien.ttf", 24)

    def update(self, event_list):
        if not self.game_started:
            self.handle_start_screen(event_list)
        else:
            self.update_game(event_list)

    def handle_start_screen(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button_rect.collidepoint(mouse_pos):
                    self.game_started = True
                    self.start_time = time.time()

        self.draw_start_screen()

    def update_game(self, event_list):
        self.remaining_time = max(0, 300 - int(time.time() - self.start_time))
        if self.remaining_time == 0:
            self.draw_game_over_screen(event_list)
        else:
            self.user_input(event_list)
            self.draw()
            self.check_level_complete(event_list)

    def draw_start_screen(self):
        screen.fill(BLACK)
        start_text = self.title_font.render("Memory Game", True, WHITE)
        start_text_rect = start_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )

        button_text = self.content_font.render("Start", True, BLACK)
        self.start_button_rect = pygame.Rect(
            (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 20, 150, 50)
        )
        pygame.draw.rect(screen, WHITE, self.start_button_rect)
        screen.blit(
            button_text, button_text.get_rect(center=self.start_button_rect.center)
        )

        screen.blit(start_text, start_text_rect)

    def draw_game_over_screen(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button_rect.collidepoint(mouse_pos):
                    self.reset_game()

        screen.fill(BLACK)
        over_text = self.title_font.render("Time's Up!", True, RED)
        over_text_rect = over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )

        button_text = self.content_font.render("Play Again", True, BLACK)
        self.start_button_rect = pygame.Rect(
            (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50)
        )
        pygame.draw.rect(screen, WHITE, self.start_button_rect)
        screen.blit(
            button_text, button_text.get_rect(center=self.start_button_rect.center)
        )

        screen.blit(over_text, over_text_rect)

    def reset_game(self):
        self.game_started = False
        self.level = 1
        self.remaining_time = 300
        self.generate_level(self.level)

    def draw(self):
        screen.fill(BLACK)
        time_text = self.content_font.render(
            f"Time: {self.remaining_time // 60}:{self.remaining_time % 60:02}",
            True,
            WHITE,
        )
        screen.blit(time_text, (10, 10))

        self.tiles_group.draw(screen)
        self.tiles_group.update()

    def generate_level(self, level):
        self.aliens = self.select_random_aliens(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)

    def generate_tileset(self, aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = self.img_width * self.cols + self.padding * 3
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        self.tiles_group.empty()

        for i in range(len(aliens)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(aliens[i], x, y)
            self.tiles_group.add(tile)

    def select_random_aliens(self, level):
        aliens = random.sample(self.all_aliens, (self.level + self.level + 2))
        aliens_copy = aliens.copy()
        aliens.extend(aliens_copy)
        random.shuffle(aliens)
        return aliens

    def user_input(self, event_list):
        pass

    def check_level_complete(self, event_list):
        pass


pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Memory Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    game.update(event_list)

    pygame.display.update()

pygame.quit()
