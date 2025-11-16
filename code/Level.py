import pygame
from Setting import *
from Tile import  Tile
from Player import Player
from Support import *

class Level:
    def __init__(self):
        #渲染
        self.display_surface = pygame.display.get_surface()


        #可视化精灵组和障碍物精灵组
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # 创建地图，角色生成
        self.create_map()


    def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../Map/map_FloorBlocks.csv')
		}
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


    #相机系统的实现
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #相机偏移量
        self.offset = pygame.math.Vector2()
        self.half_width =self.display_surface.get_size()[0] / 2
        self.half_height = self.display_surface.get_size()[1] / 2
    def custom_draw(self,player):
        #得到偏移量
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #排序精灵族，优先渲染y值小的
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos  = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)