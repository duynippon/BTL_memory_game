import time

import pygame

from dinh_nghia import Dinh_nghia
from game import Game

goi_ham_DN = Dinh_nghia()

pygame.init()
game = None

# Set constants
WHITE = goi_ham_DN.WHITE
RED = goi_ham_DN.RED
BLACK = goi_ham_DN.BLACK
screen = goi_ham_DN.screen
pygame.display.set_caption("BTL_memory_game")

# set phong chu ne
big_font = pygame.font.Font("fonts/Little Alien.ttf", 50)
small_font = pygame.font.Font("fonts/Little Alien.ttf", 25)
# set dang o dau ne
STATE_START = 0
STATE_ON_GAME = 1
STATE_END = 2
STATE = STATE_START

# load hinh ne
start_background = pygame.image.load("image_from_shool/HCMUT-BachKhoa-Logo.png")
start_background = pygame.transform.scale(
    start_background, (goi_ham_DN.WINDOW_WIDTH, goi_ham_DN.WINDOW_HEIGHT)
)
end_background = pygame.image.load("image_from_shool/img_dep")
end_background = pygame.transform.scale(
    end_background, (goi_ham_DN.WINDOW_WIDTH, goi_ham_DN.WINDOW_HEIGHT)
)

# segt cai nut ne
button_width = 200
button_height = 60
button_x = (goi_ham_DN.WINDOW_WIDTH - button_width) // 2
button_y = goi_ham_DN.WINDOW_HEIGHT // 2

# set thoi gian ne
TIMER_DURATION = 300
start_time = None


# reset vui ve ne
def reset_game():

    global game
    game = Game()


# ve man hinh ne
def draw_start_screen():
    screen.blit(start_background, (0, 0))  # Draw the background image
    """Draws the start screen."""
    game_name_text = big_font.render("MEMORY GAME CUTE DE THUONG", True, WHITE)
    game_name_rect = game_name_text.get_rect(
        center=(goi_ham_DN.WINDOW_WIDTH // 2, goi_ham_DN.WINDOW_HEIGHT // 4)
    )
    screen.blit(game_name_text, game_name_rect)

    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
    button_text = small_font.render("START", True, goi_ham_DN.RED)
    button_rect = button_text.get_rect(
        center=(button_x + button_width // 2, button_y + button_height // 2)
    )
    screen.blit(button_text, button_rect)


# ve man hinh muon
def draw_end_screen():
    screen.blit(end_background, (0, 0))  # Draw the background image
    game_name_text = big_font.render(
        "MEMORY GAME CUTE DE THUONG", True, goi_ham_DN.WHITE
    )
    game_name_rect = game_name_text.get_rect(
        center=(goi_ham_DN.WINDOW_WIDTH // 2, goi_ham_DN.WINDOW_HEIGHT // 4)
    )
    screen.blit(game_name_text, game_name_rect)

    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
    button_text = small_font.render("PLAY AGAIN", True, goi_ham_DN.RED)
    button_rect = button_text.get_rect(
        center=(button_x + button_width // 2, button_y + button_height // 2)
    )
    screen.blit(button_text, button_rect)


running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (
                button_x <= mouse_x <= button_x + button_width
                and button_y <= mouse_y <= button_y + button_height
            ):
                if STATE == STATE_START or STATE == STATE_END:
                    STATE = STATE_ON_GAME
                    start_time = time.time()
                    reset_game()

    screen.fill(goi_ham_DN.BLACK)

    if STATE == STATE_START:
        draw_start_screen()

    elif STATE == STATE_ON_GAME:
        if start_time is not None:
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, TIMER_DURATION - elapsed_time)

            game.update(event_list)

            if remaining_time <= 0:
                STATE = STATE_END

    elif STATE == STATE_END:
        draw_end_screen()

    pygame.display.update()
