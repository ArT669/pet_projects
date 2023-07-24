import random
from matplotlib import pyplot, colors
import numpy as np
import matplotlib.patches as mpatches

class agent():
	def __init__(self, x, y, group, pregroup, step,
        chance_of_infect, radius_of_infect,
        transition, t_time, time=0, counter_step=False):

		"""
		0 -- здоровый;
		1 -- инфицированный;
		2 -- легко больной;
		3 -- тяжело больной;
		4 -- имунный;
		5 -- мертвый.
		"""

		self.x = x
		self.y = y 
		self.group = group #принадлежность к некой группе
		self.pregroup = pregroup #запоминание предыдущей группы
		self.step = step[group] #шаг, не более которого может совершить человек
		self.chance_of_infect = chance_of_infect[group] #шанс того, что экземпляр может заразить других
		self.radius_of_infect = radius_of_infect[group] #радиус заражения
		self.transition = transition[group] #вероятность перехода в новое состояние
		self.t_time = t_time[group] #время периода стабильного течения болезни
		self.time = time #время смены состояния [1-5]
		self.counter_step = counter_step #флаг для отслеживания, был ли шаг

	def info(self):
		"""Для документации можно использовать"""
		print(
			f"(x, y) = ({self.x}, {self.y}), group = {self.group}, pregroup = {self.pregroup}")
		print(f"step = {self.step}, p_infect = {self.chance_of_infect}")
		print(f"r = {self.radius_of_infect}, p_trans = {self.transition}")
		print(f"t_time = {self.t_time}, time is {self.time}")

	def options(self):
			"""Изменение всех характеристик, связанных с группой"""
			self.radius_of_infect = radius_of_infect[self.group]
			self.chance_of_infect = chance_of_infect[self.group]
			self.step = step[self.group]
			self.t_time = t_time[self.group]
			self.transition = transition[self.group]


	def change_group_infect(self, opposite, opposite_chance, counter):
		"""Инфицирование"""
		pregroup = self.pregroup
		group = self.group

		if pregroup == 0 and opposite != 0 and group != 1:
			change = self.group
			self.pregroup = change
			chance = opposite_chance
			new_flip = random.choices([1, 0], 
				weights = [chance, 1 - chance]) #использование вероятности для определения перехода
			self.group = new_flip[-1]
			self.options() #изменение всех характеристик на новые

			if self.group != 0:
				self.time = counter


	def change_group_condition(self):
		"""Смена состояния внутри болезни"""
		n_need = [0, 4, 5]
		if self.pregroup not in n_need:

			change = self.group
			self.pregroup = change
			slices = list(range(change + 1, 6))
			new_flip = random.choices(slices, 
				weights=transition[change]) #использование вероятности для определения перехода
			self.group = new_flip[-1]
			self.options() #изменение всех характеристик на новые

def agentCreator(size, group, pregroup, groupList, field, n, m, step, chance_of_infect, radius_of_infect, transition, t_time):
	"""Создание агентов"""
	for j in range(size):

		while True:
			x = random.choice(range(n)) 
			y = random.choice(range(m)) 

			if field[x][y] == None: #проверка на незанятость ячейки
				field[x][y] = agent(x=x,
						y=y,
						group=group,
						pregroup=pregroup,
						step=step,
				        chance_of_infect=chance_of_infect,
				        radius_of_infect=radius_of_infect,
				        transition=transition,
				        t_time=t_time,
				        time=0,
				        counter_step=False)
				groupList.append(field[x][y]) #также для документации
				break

def animation(size, world, flag):
	"""Создание массива для отображения конкретного шага (в зависимости от флага можно вывести и общие данные)"""
	population = [[[211, 211, 211] for j in range(0, size)] for i in range(0, size)] #RGB код (light grey)
	data = [0, 0, 0, 0, 0, 0]

	for i in range(size):
		for j in range(size):
			if world[i][j] == None: #light grey
				pass

			elif world[i][j].group == 0:
				population[i][j] = [0,128,0] #green
				data[0] += 1

			elif world[i][j].group == 1:
				population[i][j] = [255,0,0] #red
				data[1] += 1

			elif world[i][j].group == 2:
				population[i][j] = [255,20,147] #deep pink
				data[2] += 1

			elif world[i][j].group == 3:
				population[i][j] = [0,0,0] #black
				data[3] += 1

			elif world[i][j].group == 4:
				population[i][j] = [0,0,255] #blue
				data[4] += 1

	if flag == 'population':
		return population

	elif flag == 'data':
		return data

def legend_for_me(figure, infected, location):
	"""
	Вспомогательная функция для визуализации
	"""
	green_patch = mpatches.Patch(color = 'green', label=f"health = {infected[0]}")
	red_patch = mpatches.Patch(color = 'red', label=f"infected = {infected[1]}")
	pink_patch = mpatches.Patch(color = 'deeppink', label=f"easy ill = {infected[2]}")
	black_patch = mpatches.Patch(color = 'black', label=f"hard ill = {infected[3]}")
	blue_patch = mpatches.Patch(color = 'blue', label=f"immune = {infected[4]}")

	return figure.legend(loc=location, handles=[green_patch, red_patch,
						pink_patch, black_patch, blue_patch, ], title=f"sum = {sum(infected)}\ndead = {infected[5]}")

def cut_off(size_of_world, i, j, around, marker):
	"""
	Создаю два массива, состоящих из окрестностей по строкам и столбцам,
	не учитывая то, что выходящих за пределы сетки координат у нас нет.
	"""
	neigh1 = list(range(i - around, i + around + 1))
	neigh2 = list(range(j - around, j + around + 1))
	N1 = len(neigh1)
	N2 = len(neigh2)
	k = 0
	l = 0
	"""
	Избавляюсь от неугодных значений, выходящих за пределы сетки.
	"""
	while k < N1:
		if neigh1[k] < 0 or neigh1[k] > size_of_world - 1:
			del neigh1[k]
			N1 -= 1
		else:
			k += 1

	while l < N2:
		if neigh2[l] < 0 or neigh2[l] > size_of_world - 1:
			del neigh2[l]
			N2 -= 1
		else:
			l += 1

	if marker == 'i':
		return neigh1

	if marker == 'j':
		return neigh2

def make_data(file, flag):

	data = []
	file = open(file, 'r')
	lines = file.readlines()

	if flag == 'step':

		data = lines[1].split()

		for i in range(len(data)):
			data[i] = int(data[i])

		step = {
    	0: data[0],
    	1: data[0],
    	2: round(data[0] / 2),
   		3: data[1],
   		4: data[0],
    	5: 0
			}

		print(f"step \n {step}")

		return step

	if flag == 'chance':

		data = lines[3].split()

		for i in range(len(data)):
			data[i] = float(data[i])


		chance_of_infect = {
    	0: 0,
    	1: data[0],
    	2: data[1],
    	3: data[2],
    	4: 0,
    	5: 0
			}

		print(f"chance_of_infect \n{chance_of_infect}")

		return chance_of_infect

	elif flag == 'radius':

		data = lines[5].split()

		for i in range(len(data)):
			data[i] = int(data[i])

		radius_of_infect = {
    	0: 0,
    	1: data[0],
    	2: data[1],
    	3: data[2],
    	4: 0,
    	5: 0
			}

		print(f"radius_of_infect \n {radius_of_infect}")

		return radius_of_infect


	elif flag == 'transition':

		for k in range(9, 12):
			data.append(lines[k].split())

		for i in range(len(data)):
			for j in range(len(data[i])):
				data[i][j] = float(data[i][j])

		transition = {
    	0: 0,
    	1: data[0],
    	2: data[1],
    	3: data[2],
    	4: 0,
    	5: 0
			}

		print(f"transition \n {transition}")

		return transition


	elif flag == 't_time':

		data = lines[7].split()

		for i in range(len(data)):
			data[i] = int(data[i])

		t_time = {0: 0,
        	1: data[0],
        	2: data[1],
    		3: data[2],
    		4: 0,
    		5: 0
          	}

		print(f"t_time \n {t_time}")

		return t_time

	else:
		print('ERROR')


"""
Создание начальных условий.
"""  
size_of_world = 20
world = [[None for i in range(0, size_of_world)] for i in range(0, size_of_world)] #создание пустого поля

agents_0 = []
agents_1 = []
agents_2 = []

"""
Расстояния для движения. 
d1 -- здоровый, инфицированный, имунный; 
round(d1/2) -- легко больной;
d2 -- тяжело больной
"""

"""
Вероятность заразить кого-то. 
p1 -- инфицированный заражает здоровых;
p2 -- легко больной заражает здоровых;
p3 -- тяжело больной заражает здоровых.
"""

"""
Радиус заражения.
r1 -- для инфицированного;
r2 -- для легко больного;
r3 -- для тяжело больного.
"""

"""
Время, по истечению которого будет смена состояния.
td1 -- инкубационный период (переход от инфицированного к болеющему/переболевшему/мертвому [1-5]);
td2 -- время стабильного течения болезни в легкой стадии (переход от легко больного к тяжело больному/переболевшему/мертвому [2-5]);
td3 -- время стабильного течения болезни в тяжелой стадии (переход от тяжело больного к переболевшему/мертвому [3-5]).
"""

"""
Вероятности перехода из одного состояния в другое.
Например, pc13 -- вероятность перехода из состояния инфицированный [1] в состояние тяжело больной [3])
"""

"""
Словари характеристик в зависимости от группы для передачи классу агентов.
"""
step = make_data('data.txt', 'step')
chance_of_infect = make_data('data.txt', 'chance')
radius_of_infect = make_data('data.txt', 'radius')
transition = make_data('data.txt', 'transition')
t_time = make_data('data.txt', 't_time')

"""
Создание начального количества здоровых [group = 0] и инфицированных [group = 1], а также легко больных [group = 2].
"""       
agentCreator(size=35,
		group=0,
        pregroup=0,
		groupList=agents_0,
		field=world,
		n=size_of_world,
		m=size_of_world,
        step=step,
        chance_of_infect=chance_of_infect,
        radius_of_infect=radius_of_infect,
        transition=transition,
        t_time=t_time)

agentCreator(size=15,
		group=1,
        pregroup=1,
		groupList=agents_1,
		field=world,
		n=size_of_world,
		m=size_of_world,
        step=step,
        chance_of_infect=chance_of_infect,
        radius_of_infect=radius_of_infect,
        transition=transition,
        t_time=t_time)

agentCreator(size=7,
		group=2,
        pregroup=0,
		groupList=agents_2,
		field=world,
		n=size_of_world,
		m=size_of_world,
        step=step,
        chance_of_infect=chance_of_infect,
        radius_of_infect=radius_of_infect,
        transition=transition,
        t_time=t_time)


dead = 0 #счетчик смертей

"""
Создание изображения начальных данных.
"""
locations = world.copy()
population_before_run = animation(size_of_world, locations, 'population')
infected1 = animation(size_of_world, locations, 'data')

"""
Задание количества шагов.
"""
iteration = 2

"""
Основное тело программы.
"""
for counter in range(1, iteration + 1):  

	"""
	Следующие два вложенных цикла отвечают за заражение.
	Находят способного заразить, проверяют его окрестность Мура: если находят незараженного,
	то в дело вступает внутренняя функция класса агентов, меняющая здоровых на зараженных.
	"""
	for i in range(0, len(world)):
		for j in range(0, len(world)):

			if world[i][j] != None: # Проверка на то, что ячейка не пуста.
				
				"""
				Объявляем, что шаг не был сделан. Добавили это в начало оценки окрестностей, чтобы не делать очередной вложенный цикл после шага.
				"""
				world[i][j].counter_step = False

				if world[i][j].pregroup != 0 and world[i][j].group != 4:  # ищу способного заразить [1-3]
					"""
					Беру характеристики за новые переменные, чтобы не возиться с обращением к атрибутам.
					"""
					pregroup = world[i][j].pregroup
					radius = world[i][j].radius_of_infect
					chance_of_infecting = world[i][j].chance_of_infect

					neigh1 = cut_off(size_of_world, i, j, radius, 'i')
					neigh2 = cut_off(size_of_world, i, j, radius, 'j')
					
					"""
					Проверяю соседей. Если сосед существует и незаражен, то заражаю его.
					"""
					for k in neigh1:
						for l in neigh2:
							
							if world[k][l]:
								if world[k][l].group == 0:
									world[k][l].change_group_infect(pregroup, chance_of_infecting, counter)

					"""
					Счетчик для смены состояний и подсчета смертей.
					"""
					if counter - world[i][j].time == world[i][j].t_time:
						"""print(
							f"time of ({i}, {j}), need is {world[i][j].t_time}, now is {counter}, last change is {world[i][j].time} and it is for {world[i][j].pregroup} ")
						"""
						world[i][j].change_group_condition()
						world[i][j].time = counter

						"""
						Здесь я удаляю с поля мертвых.
						"""
						if world[i][j].group == 5:
							world[i][j] = None
							dead += 1


	"""
	Следующий вложенный цикл отвечает за остальные части:
	-- смена предыдущей группы на текущую после обхода всех заражённых 
	(дабы избежать ситуации, где человек заражается дважды и в итоге не заражается вовсе, если последний раз вышел неудачным)
	-- увеличение счетчика времени для каждого агента
	-- шаг
	"""

	for i in range(0, len(world)):
		for j in range(0, len(world)):

				if world[i][j] != None:
						
					"""
					Проверка на то, был ли сделан шаг. 
					Для того, чтобы при переборе не получилось, что кто-то сходил n раз.
					"""
					if world[i][j].counter_step == False:
						
						if world[i][j].group != world[i][j].pregroup:
							group = world[i][j].group
							world[i][j].pregroup = group

						steps = world[i][j].step
						step_i = cut_off(size_of_world, i, j, steps, 'i')
						step_j = cut_off(size_of_world, i, j, steps, 'j')
						correct_steps = []

						for row in step_i:
							for column in step_j:
								if world[row][column] == None:
									correct_steps.append((row, column))

						if correct_steps:

							found = random.choice(correct_steps)
							found_i = found[0]
							found_j = found[1]

							world[found_i][found_j] = world[i][j]
							world[i][j] = None
							world[found_i][found_j].counter_step = True
							#print(f"движение ({i},{j}) на клетку ({found_i}, {found_j})")

						else:
							world[i][j].counter_step = True
							#print(f"движение ({i},{j}) на месте")

"""
Анимация
"""
population_after_run = animation(size_of_world, world, 'population')
infected = animation(size_of_world, world, 'data')
infected[5] = dead

figure = pyplot.figure(figsize = (13,8))

pyplot.subplot(1, 2, 1, label='before simulation')
pyplot.imshow(population_before_run)
pyplot.title("before simulation run", 
			fontsize = 12)


pyplot.subplot(1, 2, 2, label='after simulation')
pyplot.imshow(population_after_run)
pyplot.title(f"after {iteration} simulation run",
            fontsize = 12)

loc1 = 2
legend_for_me(figure, infected1, loc1)

loc2 = 1
legend_for_me(figure, infected, loc2)

pyplot.show()