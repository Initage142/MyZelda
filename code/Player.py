import pygame
from Support import import_folder
from Setting import *
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../Graphics/player/down_idle/下1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        #碰撞箱用于碰撞检测
        self.hitbox  = self.rect.inflate(-6,HITBOX_OFFSET['player'])


        #角色图片建立
        self.import_player_assets()
        self.status = 'down'
        # self.frame_index = 0
        # self.animation_speed = 0.15


        #角色初始速度
        # self.speed = 5
        # self.direction = pygame.math.Vector2() #角色的坐标
        self.attacking = False
        self.attack_cooldown = 400 #攻击冷却时间
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        #武器
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack #攻击结束销毁攻击动作
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200 #武器切换时间


        #魔法
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #状态
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 123
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #升级
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}

        #音效
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

        #死亡
        self.is_dead = False
        #出生点
        self.spawn_pos = pos

    def check_death(self):
        if self.health <= 0:
            self.is_dead = True

    def import_player_assets(self):
        character_path = '../Graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    #角色的控制逻辑
    def input(self):

        if not self.attacking:
            keys =pygame.key.get_pressed()

            #移动逻辑
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            #攻击逻辑
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            #魔法攻击
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            #按q 切换武器
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]
            #按e 切换魔法
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        #空闲状态
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        #攻击状态,禁止移动
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            #攻击结束
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    # #角色的移动逻辑
    # def move(self,speed):
    #     #确保对角线移动速度过快
    #     if self.direction.magnitude() != 0:
    #         self.direction = self.direction.normalize()
    #
    #     #移动，当前坐标加速度向量
    #     self.hitbox.x += self.direction.x * speed
    #     #水平碰撞检测
    #     self.collision('horizontal')
    #     self.hitbox.y += self.direction.y * speed
    #     #垂直碰撞检测
    #     self.collision('vertical')
    #     self.rect.center  = self.hitbox.center
    #
    #
    # #障碍物检测
    # def collision(self,direction):
    #     if direction == 'horizontal':
    #         for sprite in self.obstacle_sprites: # 检测碰撞函数
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.x > 0: #向右移动
    #                     self.hitbox.right = sprite.hitbox.left
    #                     # 角色的右侧与障碍物的左侧对其
    #                 if self.direction.x < 0: #向左移动
    #                     self.hitbox.left = sprite.hitbox.right
    #                     #角色的左侧与障碍物的右侧对其
    #
    #     if direction == 'vertical':
    #         for sprite in self.obstacle_sprites: # 检测碰撞函数
    #             if sprite.rect.colliderect(self.hitbox):
    #                 if self.direction.y > 0: #向下移动
    #                     self.hitbox.bottom = sprite.hitbox.top
    #                 if self.direction.y < 0: #向上移动
    #                     self.hitbox.top = sprite.hitbox.bottom

    #攻击冷却和切换武器冷却
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown+ weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    #角色的动画帧加载
    def animate(self):
        animation = self.animations[self.status]

        #循环播放动画帧
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # 闪烁效果
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage
    #能量恢复
    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    #更新角色
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
        self.check_death()