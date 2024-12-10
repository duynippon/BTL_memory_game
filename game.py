import pygame

from dinh_nghia import Dinh_nghia

goi_ham_dinh_nghia = Dinh_nghia()
screen = goi_ham_dinh_nghia.screen


class Game:
    def __init__(self):
        self.level = 1
        self.qua_man = False

    def update(self, event_list):
        self.draw()

    def draw(self):
        screen.fill(goi_ham_dinh_nghia.BLACK)
        # thì phải set up cái font trước rồi mới ghi chữ chứ đk ?
        title_font = pygame.font.Font("fonts/Little Alien.ttf", size=45)
        content_font = pygame.font.Font("fonts/Little Alien.ttf", size=25)
        # viết chữ nè render ra r sau đó là mik phải đưa vào 1 cái rectangle để nó hiển thị trên đó
        lbl_text = title_font.render("BTL_CKT_NMLT", True, goi_ham_dinh_nghia.WHITE)
        lbl_rect = lbl_text.get_rect(midtop=(goi_ham_dinh_nghia.SCREEN_WIDTH // 2, 10))

        label_hien_level_text = content_font.render(
            f"level : {self.level} ", True, goi_ham_dinh_nghia.WHITE
        )
        label_level_rect = label_hien_level_text.get_rect(
            midtop=(goi_ham_dinh_nghia.SCREEN_WIDTH // 2, 80)
        )
        bangr_info_text = content_font.render(
            "hay tim 2 hinh giong nhau cho toi khi het man",
            True,
            goi_ham_dinh_nghia.WHITE,
        )
        bangr_info_rect = bangr_info_text.get_rect(
            midtop=(goi_ham_dinh_nghia.SCREEN_WIDTH // 2, 120)
        )
        if self.level != 5:
            choi_tiep_text = content_font.render(
                "nhan nut SPACE de choi tiep man sau", True, goi_ham_dinh_nghia.WHITE
            )
        else:
            choi_tiep_text = content_font.render(
                "nhan nut SPACE de choi lai tu dau nhe hihi ",
                True,
                goi_ham_dinh_nghia.WHITE,
            )
        choi_tiep_rect = choi_tiep_text.get_rect(
            midbottom=(
                goi_ham_dinh_nghia.SCREEN_WIDTH // 2,
                goi_ham_dinh_nghia.SCREEN_HEIGHT - 40,
            )
        )
        # render ra màn hình nè cute hong hihi
        screen.blit(lbl_text, lbl_rect)
        screen.blit(label_hien_level_text, label_level_rect)
        screen.blit(bangr_info_text, bangr_info_rect)
        if self.qua_man:
            screen.blit(choi_tiep_text, choi_tiep_rect)
