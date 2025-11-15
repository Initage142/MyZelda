import pygame
from settings import *


class Button:
    def __init__(self, text, width, height):
        # 获取显示表面
        self.display_surface = pygame.display.get_surface()

        # 初始化按钮的宽度、高度和文本内容
        self.width = width
        self.height = height
        self.text = text

        # 初始化字体和字体大小
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # 创建按钮的矩形区域，并将其居中放置在屏幕中央
        window_size = self.display_surface.get_size()
        window_center = (window_size[0] // 2, window_size[1] // 2)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = window_center


    def display(self):
        # 设置按钮的背景色和边框颜色
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,self.rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,self.rect,4)
        # 设置按钮的文本内容和颜色
        surface = self.font.render(self.text, False, TEXT_COLOR)
        surface_rect = surface.get_rect(center=self.rect.center)
        # 将按钮的文本内容绘制到屏幕上
        self.display_surface.blit(surface, surface_rect)