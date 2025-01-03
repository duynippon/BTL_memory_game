import os
import random
import time

import cv2
import pygame

from dinh_nghia import Dinh_nghia
from tile import Tile

goi_ham_dinh_nghia = Dinh_nghia()

WHITE = goi_ham_dinh_nghia.WHITE
RED = goi_ham_dinh_nghia.RED
BLACK = goi_ham_dinh_nghia.BLACK

WINDOW_WIDTH = goi_ham_dinh_nghia.WINDOW_WIDTH
WINDOW_HEIGHT = goi_ham_dinh_nghia.WINDOW_HEIGHT
screen = goi_ham_dinh_nghia.screen
FPS = goi_ham_dinh_nghia.FPS


class Game:

    def __init__(self):
        self.level = 1
        self.level_complete = False

        # aliens cute pho mai que
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

        # thoi gian lat bai va quay cai la bai
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # tao ra level dau tien
        self.generate_level(self.level)

        # tai video len ne
        self.is_video_playing = True
        self.play = pygame.image.load("images/play.png").convert_alpha()
        self.stop = pygame.image.load("images/stop.png").convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(
            topright=(WINDOW_WIDTH - 50, 10)
        )
        self.get_video()

        # lam nhac nheo do nghe cho no da
        self.is_music_playing = True
        self.sound_on = pygame.image.load("images/speaker.png").convert_alpha()
        self.sound_off = pygame.image.load("images/mute.png").convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(
            topright=(WINDOW_WIDTH - 10, 10)
        )

        # Time
        self.TIMER_DURATION = 300
        self.start_time = time.time()
        # ve thoi gian ne
        self.draw_timer()
        # chieu nhac len cho nghe ne
        pygame.mixer.music.load("sounds/nhac_10p_sieu_cute_HIHI.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    def update(self, event_list):
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []

    def generate_level(self, level):
        self.aliens = self.select_random_aliens(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)

    def generate_tileset(self, aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = self.img_width * self.cols + self.padding * 3
        LEFT_MARING = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        # tiles = []
        self.tiles_group.empty()

        for i in range(len(aliens)):
            x = LEFT_MARING + ((self.img_width + self.padding) * (i % self.cols))
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
        for event in event_list:
            # event.button ==1 co nghia la chi lay chuot trai th chuot phai ko dung
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # su dung ham côliidepoint de lay dung toa do cua cai rect dang can
                # nguyen  cai if nay ne  cai nay la khi bam am thanh thi no tat ne va thay doi hinh anh
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()
                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_video_playing:
                        self.is_video_playing = False
                        self.video_toggle = self.stop
                    else:
                        self.is_video_playing = True
                        self.video_toggle = self.play

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level(self.level)

    def draw_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, self.TIMER_DURATION - elapsed_time)
        font_time = pygame.font.Font(os.path.join("fonts", "Little Alien.ttf"), 30)
        minutes, seconds = divmod(remaining_time, 60)
        timer_text = font_time.render(
            f"{minutes:02}:{seconds:02}", True, goi_ham_dinh_nghia.RED
        )
        screen.blit(timer_text, (10, 10))

    def draw(self):

        screen.fill(goi_ham_dinh_nghia.BLACK)
        self.draw_timer()

        # fonts
        title_font = pygame.font.Font("fonts/Little Alien.ttf", 44)
        content_font = pygame.font.Font("fonts/Little Alien.ttf", 24)

        # text
        title_text = title_font.render(
            "BTL_CKT_laptrinh", True, goi_ham_dinh_nghia.WHITE
        )
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render(
            "Level " + str(self.level), True, goi_ham_dinh_nghia.WHITE
        )
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        info_text = content_font.render(
            "chon 2 cai giong nhau cho den khi het hinh", True, goi_ham_dinh_nghia.WHITE
        )
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        if self.is_video_playing:
            if self.success:
                screen.blit(
                    pygame.image.frombuffer(self.img.tobytes(), self.shape, "BGR"),
                    (0, 120),
                )
            else:
                self.get_video()
        else:
            screen.blit(
                pygame.image.frombuffer(self.img.tobytes(), self.shape, "BGR"), (0, 120)
            )

        if self.level != 5:
            next_text = content_font.render(
                "len level . hay bam SPACE de qua man", True, goi_ham_dinh_nghia.WHITE
            )
        else:
            next_text = content_font.render(
                "thang roi !!! hay nhan space de choi lai level 1 ",
                True,
                goi_ham_dinh_nghia.WHITE,
            )
        next_rect = next_text.get_rect(
            midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)
        )

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        pygame.draw.rect(
            screen, goi_ham_dinh_nghia.WHITE, (WINDOW_WIDTH - 90, 0, 100, 50)
        )
        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            screen.blit(next_text, next_rect)

    # module video cua pygame no ko con nua
    # nen la dung cv2 nen la muon sai thi phai tai no ve va dung theo quy cach dac biet cua no
    def get_video(self):
        self.cap = cv2.VideoCapture("video/earth.mp4")
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]
