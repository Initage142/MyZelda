import pygame
from Setting import *
from Tile import Tile
from Player import Player
from Support import *
from random import choice,randint
from Weapon import Weapon
from debug import debug
from ui import UI
from Enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from death_screen import DeathScreen
class Level:
    def __init__(self):
        # 渲染
        self.display_surface = pygame.display.get_surface()

        # 可视化精灵组和障碍物精灵组
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # 攻击精灵组
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # 创建地图，角色生成
        self.create_map()
        # UI
        self.ui = UI()
        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        #暂停
        self.game_paused = False
        self.upgrade = Upgrade(self.player)

        #死亡
        self.death_screen = DeathScreen()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../Map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../Map/map_Grass.csv'),
            'object': import_csv_layout('../Map/map_Objects.csv'),
            'entities': import_csv_layout('../Map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../Graphics/Grass'),
            'objects': import_folder('../Graphics/Objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites,self.attackable_sprites], 'grass', random_grass_image)

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites,self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_exp)



    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])
    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    #玩家攻击判定逻辑
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):

        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.player.is_dead:
            self.death_screen.display()
        elif self.game_paused:
            self.upgrade.display()
        else:
            # 正常游戏更新逻辑
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

    # def display_death_overlay(self):
    #     # 创建一次性的灰色覆盖层表面
    #     if not hasattr(self, '_death_overlay'):
    #         self._death_overlay = pygame.Surface(
    #             (self.display_surface.get_width(),
    #              self.display_surface.get_height())
    #         )
    #         self._death_overlay.fill((50, 50, 50))  # 灰色
    #         self._death_overlay.set_alpha(150)  # 设置透明度
    #
    #     # 绘制覆盖层
    #     self.display_surface.blit(self._death_overlay, (0, 0))
    #
    #     # 显示死亡文本
    #     font = pygame.font.Font(None, 74)
    #     text = font.render("YOU DIED", True, (255, 0, 0))
    #     text_rect = text.get_rect(
    #         center=(self.display_surface.get_width() // 2,
    #                 self.display_surface.get_height() // 2)
    #     )
    #     self.display_surface.blit(text, text_rect)


    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def add_exp(self, amount):
        self.player.exp += amount

    # 相机系统的实现
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        # 相机偏移量
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] / 2
        self.half_height = self.display_surface.get_size()[1] / 2

        # 创建地板
        self.floor_surf = pygame.image.load('../Map/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # 得到偏移量
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # 排序精灵族，优先渲染y值小的
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
