import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../Graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        #碰撞箱用于碰撞检测
        self.hitbox  = self.rect.inflate(0,-26)

        #角色初始速度
        self.speed = 5
        #角色的坐标
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites


    #角色的控制逻辑
    def input(self):
        keys =pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0



    #角色的移动逻辑
    def move(self,speed):
        #确保对角线移动速度过快
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #移动，当前坐标加速度向量
        self.hitbox.x += self.direction.x * speed
        #水平碰撞检测
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        #垂直碰撞检测
        self.collision('vertical')
        self.rect.center  = self.hitbox.center


    #障碍物检测
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites: # 检测碰撞函数
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #向右移动
                        self.hitbox.right = sprite.hitbox.left
                        # 角色的右侧与障碍物的左侧对其
                    if self.direction.x < 0: #向左移动
                        self.hitbox.left = sprite.hitbox.right
                        #角色的左侧与障碍物的右侧对其

        if direction == 'vertical':
            for sprite in self.obstacle_sprites: # 检测碰撞函数
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0: #向下移动
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #向上移动
                        self.hitbox.top = sprite.hitbox.bottom


    #更新角色
    def update(self):
        self.input()
        self.move(self.speed)

    #角色的攻击