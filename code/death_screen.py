import pygame
from Setting import *

class DeathScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, 74)
        self.small_font = pygame.font.Font(UI_FONT, 30)

        # 创建一次性使用的覆盖层表面
        self.overlay = pygame.Surface(
            (self.display_surface.get_width(),
             self.display_surface.get_height())
        )
        self.overlay.fill((50, 50, 50))  # 灰色
        self.overlay.set_alpha(150)  # 半透明

        # 预渲染文本表面避免每帧重新创建
        self.death_text = self.font.render("YOU DIED", True, (255, 0, 0))
        self.restart_text = self.small_font.render("Press R to Restart", True, (255, 255, 255))

        # 计算文本位置
        self.death_text_rect = self.death_text.get_rect(
            center=(self.display_surface.get_width()//2,
                    self.display_surface.get_height()//2 - 50)
        )
        self.restart_text_rect = self.restart_text.get_rect(
            center=(self.display_surface.get_width()//2,
                    self.display_surface.get_height()//2 + 50)
        )

    def display(self):
        """显示死亡画面"""
        # 绘制灰色覆盖层
        self.display_surface.blit(self.overlay, (0, 0))

        # 绘制死亡文本
        self.display_surface.blit(self.death_text, self.death_text_rect)
        self.display_surface.blit(self.restart_text, self.restart_text_rect)
