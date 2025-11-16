import pygame, sys
from Setting import *
from Level import Level
from death_screen import DeathScreen

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.level = Level()
		#音效
		main_sound = pygame.mixer.Sound('../audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops=-1)

		self.death_screen = DeathScreen()  # 创建死亡界面实例
		self.game_over = False

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

					# 添加复活按键处理
					if self.game_over and event.key == pygame.K_r:
						self.restart_game()
			if not self.game_over:
				self.screen.fill(WATER_COLOR)
				self.level.run()

				# 检查玩家是否死亡
				if self.level.player.is_dead:
					self.game_over = True
			else:
				# 显示死亡界面
				self.death_screen.display()

			self.screen.fill('skyblue')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)



	def restart_game(self):
		self.level.player.health = self.level.player.stats['health']
		self.level.player.is_dead = False
		# 将玩家位置重置到出生点
		self.level.player.rect.topleft = self.level.player.spawn_pos
		self.level.player.hitbox.center = self.level.player.rect.center

if __name__ == '__main__':
	game = Game()
	game.run()