from datetime import datetime, time
from prettytable import PrettyTable
import json

def get_result(data, number):

	result = data[number]
	result = datetime.strptime(result, '%H:%M:%S.%f')
	result = datetime.strftime(result, '%M:%S,%f')
	result = result[:-4]

	return result

results_run = open('results_RUN.txt', 'r', encoding="utf-8-sig")
lines = results_run.readlines()
number_of_line = 0
data_finish = ''
data_of_results = {}
number = []
diff_time = []

for line in lines:

	time_finish = '00:00:00,0'
	time_finish = datetime.strptime(time_finish, '%H:%M:%S,%f')

	if number_of_line % 2 == 0:

		data_start = line.split()
		time_start = data_start[-1]
		time_start = datetime.strptime(time_start, '%H:%M:%S,%f')

	elif number_of_line % 2 == 1:

		data_finish = line.split()
		time_finish = data_finish[-1]
		time_finish = datetime.strptime(time_finish, '%H:%M:%S,%f')
	
	result = 0

	if number_of_line % 2 == 1:

		result = time_finish - time_start
		result = str(result)
		number.append(data_start[0])
		diff_time.append(result)

	number_of_line += 1

results_run.close()

for i in range(len(number)):

	data_of_results[number[i]] = diff_time[i]

with open('competitors2.json', 'r', encoding="utf-8") as people_file:

	people_data = json.load(people_file)

data_of_results = sorted(data_of_results.items(), key=lambda x:x[1])
data_of_results = dict(data_of_results)
""""""

place = 0
table = [['Занятое место', 'Нагрудный номер', 'Имя', 'Фамилия', 'Результат']]
sport_table = PrettyTable(table[0])

for number_ in data_of_results.keys():
	for number, people_info in people_data.items():

		if number_ == number:

			place += 1
			name = people_info['Surname']
			surname = people_info['Name']
			result = get_result(data_of_results, number_)
			mid_table = [place, number_, name, surname, result]
			table.append(mid_table)
			sport_table.add_row(mid_table)

print(sport_table)
 
#print(table)
