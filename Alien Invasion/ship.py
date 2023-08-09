import pygame

class Ship():
	"""Класс для управления кораблем"""

	def __init__(self, ai_game):
		"""Задает начальную позицию"""

		self.screen = ai_game.screen
		self.settings = ai_game.settings
		#rectangle surface
		self.screen_rect = ai_game.screen.get_rect()

		#загружает изображение корабля и получает прямоугольник
		self.image = pygame.image.load('images/ship.bmp')
		#положение корабля
		self.rect = self.image.get_rect()
		#каждый новый корабль появляется у нижнего края экрана midtop etc positions
		self.rect.midbottom = self.screen_rect.midbottom

		#прямоугольники принимают только целые значения, а скорость взяли дробную, поэтому
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		#флаги для перемещения
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False


	def update(self):

		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed

		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		if self.moving_up and self.rect.top > self.screen_rect.top:
			self.y -= self.settings.ship_speed

		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings.ship_speed

		self.rect.x = self.x
		self.rect.y = self.y


	def update1(self):
		"""Обновляет позицию корабля с учетом нажатия клавиш"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed

		#можно поставить и > 0, т.к. (0,0) в левом углу, но мы это опустим
		if self.moving_left and self.rect.left > self.screen_rect.left: 
			self.x -= self.settings.ship_speed

		#будет сохранена только целая часть, но для отображения ок
		self.rect.x = self.x


	def blitme(self):
		"""Рисует корабль в текущей позиции"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Размещает корабль в центр экрана"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)



