import pygame

class GameStats():
	"""Отслеживание статистики для игры Alien Invasion"""

	def __init__(self, ai_game):
		"""Инициализирует статистику"""
		self.settings = ai_game.settings
		self.reset_stats()
		self.game_active = False

		with open('records.txt', 'r', encoding = 'utf-8') as f:
			record = f.read()
			self.high_score = int(record)
		#чтобы рекорд не сбрасывался, он будет здесь
		#self.high_score = 0

	def reset_stats(self):
		"""Инициализирует статистику, изменяющуюся в ходе игры"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
