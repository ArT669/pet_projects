
class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion"""

	def __init__(self):
		"""Инициализация статистических настроек игры"""
		# Настройки экрана
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# Настройки корабля
		self.ship_speed = 1.5
		self.ship_limit = 3

		# Настройки пулей
		self.bullet_speed = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3 # Сколько пуль может быть одновременно на экране

		# Настройки пришельцев
		self.alien_speed = 0.5 #x
		self.fleet_drop_speed = 10 #y
		
		# Темп ускорения игры с увеличением уровня
		self.speedup_scale = 1.1
		# Темп роста стоимости пришельцев с увеличением уровня
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Инициализация динамических настроек"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3.0
		self.alien_speed_factor = 1.0
		self.fleet_direction = 1

		# Начальная стоимость пришельца
		self.alien_points = 50

	def increase_speed(self):
		"""Увеличивает настройки игры"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)