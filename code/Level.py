import pygame
from Setting import *
from Tile import  Tile
from Player import Player


class Level:
    def __init__(self):
        #渲染
        self.display_surface = pygame.display.get_surface()

        #可视化精灵组和障碍物精灵组
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # 创建地图，角色生成
        self.create_map()


    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)