
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
from button import Button
from scoreboard import Scoreboard

class AlienInvasion():
	
	def __init__(self):
		"""Инициализация настроек из pygame:запуск pygame"""

		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		# Создание экземпляра для хранение игровой статистики
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		# Создание экземпляра корабля, спрайтов пулей и пришельцев как пустых
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		# Создание флота 
		self._create_fleet()

		# Назначение цвета фона
		self.bg_color = self.settings.bg_color

		# Создание кнопки Play
		self.play_button = Button(self, 'Play', 'green')

	def run_game(self):
		"""Запуск основного цикла игры"""
		
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

	def _check_events(self):
		# Отслеживание внешних событий: клавиатура и мышка
		for event in pygame.event.get():

				"""event.get() даёт список событий с последнего вызова этой функции"""

				# Запись рекорда в файл
				if event.type == pygame.QUIT:
					with open('records.txt', 'w+', encoding = 'utf-8') as f:
						print(self.stats.high_score, file=f)
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)

				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()				
					self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Запускает новую игру при нажатии кнопки Play"""
		if self.play_button.rect.collidepoint(mouse_pos):
			button_clicked = self.play_button.rect.collidepoint(mouse_pos)
			if button_clicked and not self.stats.game_active:
				# Сброс игровой статистики
				self.settings.initialize_dynamic_settings()
				self.stats.reset_stats()
				self.stats.game_active = True
				self.sb.prep_score()
				self.sb.prep_level()
				self.sb.prep_ships()

				# Очистка пришельцев и пуль
				self.aliens.empty()
				self.bullets.empty()

				# Создание нового флота
				self._create_fleet()
				self.ship.center_ship()

				# Скрываем указатель
				pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""Реакция на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			# Переместить корабль вправо
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

		# Выход из игры с помощью клавиши Q и запись рекорда
		elif event.key == pygame.K_q:
			with open('records.txt', 'w+', encoding = 'utf-8') as f:
				print(self.stats.high_score, file=f)
			sys.exit()

	def _check_keyup_events(self, event):
		"""Реакция на отпускание клавиш"""
		if event.key == pygame.K_RIGHT:
			# Остановка перемещения вправо
			self.ship.moving_right = False

		elif event.key == pygame.K_LEFT:
			# Остановка перемещения влево
			self.ship.moving_left = False

		elif event.key == pygame.K_UP:
			# Остановка перемещения вверх
			self.ship.moving_up = False

		elif event.key == pygame.K_DOWN:
			# Остановка перемещения вниз
			self.ship.moving_down = False

	def _fire_bullet(self):
		"""Создание новой пули"""
		new_bullet = Bullet(self)

		# Добавление новой пули, если можно выстрелить ещё одну
		if len(self.bullets) < self.settings.bullets_allowed:
			self.bullets.add(new_bullet)

	def _create_fleet(self):
		"""Создание флота вторжения"""

		# Создание пришельца и вычисление их кол-ва в ряду
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		# Определение кол-во рядов, помещающихся на экране
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(3 * alien_height) - ship_height)
		number_rows = available_space_y // (4 * alien_height)

		# Создание флота пришельцев в соответствии с вычисленными настройками
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
		"""Перемещение всего флота вниз и смена направления движения"""

		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		"""Обновление экрана: прорисовка"""

		# Задание цвета экрана и обновление корабля
		self.screen.fill(self.bg_color)
		self.ship.blitme()


		# Отрисовка всех пуль в спрайте
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		# Отрисовка всех пришельцев в одну строку, т.к. они через картинку рисуются, а не вручную
		self.aliens.draw(self.screen)

		# Отображение всей игровой информации: количество жизней, уровень, текущий счет и рекорд
		self.sb.show_score()

		# Кнопка Play отображается в том случае, если игра неактивна
		if not self.stats.game_active:
				self.play_button.draw_button()

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
		# Проверка столкновения пуль и пришельцев, при поражении удаление и снаряда, и пришельца
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		"""ключ значение тру1 это удаление снаряда, 
		тру2 это удаление пришельцев"""

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#Уничтожение существующих снарядов и создание нового флота
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			# Увеличение уровня
			self.stats.level += 1
			self.sb.prep_level()

	def _ship_hit(self):
		"""Обрабатывает столкновение корабля с пришельцем"""

		# Уменьшение количества жизней
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			# Очистка спрайтов пришельцев и снарядов
			self.aliens.empty()
			self.bullets.empty()

			# Создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()

			# Пауза
			sleep(0.5)

		# При утрате последней жизни игра останавливается и появляется курсор
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

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

	# Создание экземпляра игры и запуск
	ai = AlienInvasion()
	ai.run_game()