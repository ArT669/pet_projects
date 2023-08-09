# страница 275
import sys
from time import sleep

"""
sys предназначена для операций над системой и порядком исполнения программы
time для остановки игры на момент столкновения
"""

import pygame

"""
функционал для создания игры
каждый игровой цикл называется кадром
1. обработка ввода (события)
2. обновление игры
3. рендеринг (прорисовка)
"""

from settings import Settings 
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion():
	
	def __init__(self):
		"""Инициализация настроек из pygame:запуск pygame"""

		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		#Создание экземпляра для хранение игровой статистики
		self.stats = GameStats(self)

		#корабль
		self.ship = Ship(self)
		#пули
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()
		#назначение цвета фона
		self.bg_color = self.settings.bg_color
		

	def run_game(self):
		"""Запуск основного цикла игры"""
		
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

	"""разделяем run_game на вспомогательные методы [рефакторинг]"""

	def _check_events(self):
		# Отслеживание внешних событий: клавиатура и мышка
		for event in pygame.event.get():
				"""event.get() даёт список событий с последнего вызова этой функции"""
				if event.type == pygame.QUIT:
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)

				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""Реакция на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			#переместить корабль вправо
			self.ship.moving_right = True

		elif event.key == pygame.K_LEFT:
			# Переместить корабль влево
			self.ship.moving_left = True

		elif event.key == pygame.K_UP:
			# Переместить корабль вверх
			self.ship.moving_up = True

		elif event.key == pygame.K_DOWN:
			# Переместить корабль вниз
			self.ship.moving_down = True

		elif event.key == pygame.K_SPACE:
			# Выстрелить снарядом
			self._fire_bullet()

		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""Реакция на отпускание клавиш"""
		if event.key == pygame.K_RIGHT:
			# не Переместить корабль вправо
			self.ship.moving_right = False

		elif event.key == pygame.K_LEFT:
			# не Переместить корабль влево
			self.ship.moving_left = False

		elif event.key == pygame.K_UP:
			# не Переместить корабль вверх
			self.ship.moving_up = False

		elif event.key == pygame.K_DOWN:
			# не Переместить корабль вниз
			self.ship.moving_down = False

	def _fire_bullet(self):
		"""Создание группы пуль"""
		new_bullet = Bullet(self)

		if len(self.bullets) < self.settings.bullets_allowed:
			self.bullets.add(new_bullet)

	def _create_fleet(self):
		"""Создание флота вторжения"""
		# Создание пришельца и вычисление их кол-ва в ряду

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		"""Определяет кол-во рядов, помещающихся на экране"""
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(3 * alien_height) - ship_height)
		number_rows = available_space_y // (4 * alien_height) #для уменьшения количества рядов 4

		# Создание флота пришельцев
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Создание пришельца и размещение его в ряду"""

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Реакция на толчок в край экрана"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self.change_fleet_direction()
				break

	def change_fleet_direction(self):
		"""Опускает весь флот и меняет направление"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		# При каждом проходе перерисовывается экран
		self.screen.fill(self.bg_color) # Цвет
		self.ship.blitme() # Корабль

		for bullet in self.bullets.sprites():
			bullet.draw_bullet() # Прохожу по всем пулям и рисую

		self.aliens.draw(self.screen)

		# Отображение последнего отрисованного экрана
		pygame.display.flip()

	def _update_bullets(self):

		self.bullets.update()
		# Удаление старых снарядов
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		
		self._check_bullet_alien_collisions()
		
	def _check_bullet_alien_collisions(self):
		"""Обработка коллизий снарядов с пришельцами"""
		# проверка попаданий в пришельцев
		# при поражении удалить снаряд и пришельца
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		"""ключ значение тру1 это удаление снаряда, 
		тру2 это удаление пришельцев"""
		if not self.aliens:
			#Уничтожение существующих снарядов и создание нового флота
			self.bullets.empty() #существующие снаряды убираются

			"""ЛУТБОКСЫ ЗДЕСЬ"""

			self._create_fleet()

	def _ship_hit(self):
		"""Обрабатывает столкновение корабля с пришельцем"""
		# Уменьшение _ship_left
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1

			# Очистка списков пришельцев и снарядов
			self.aliens.empty()
			self.bullets.empty()

			# Создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()

			# Пауза
			sleep(0.5)

		else:
			self.stats.game_active = False

	def _check_aliens_bottom(self):
		"""Проверяет, добрались ли пришельцы до нижнего края экрана"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Происходит то же, что при столкновении с кораблем
				self._ship_hit()
			

	def _update_aliens(self):
		"""Обновляет позиции всех пришельцев во флоте 
		с учетом достижения края экрана"""
		self._check_fleet_edges()
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Проверка добрались ли пришельцы до нижнего края экрана
		self._check_aliens_bottom()


if __name__ == '__main__':
	# Создание экземпляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()




