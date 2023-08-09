
class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion"""
	#параметры экрана
	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		#настройки корабля
		self.ship_speed = 1.5
		self.ship_limit = 3

		#настройки пулей
		self.bullet_speed = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3

		#настройки пришельцев
		self.alien_speed = 0.5 #x
		self.fleet_drop_speed = 10 #y
		#флаг для изменения движения 1R -1L
		self.fleet_direction = 1