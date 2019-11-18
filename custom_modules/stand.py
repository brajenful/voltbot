import random

import g

standname1 = []
standname2 = []
standstats_choices = ['None', 'E', 'D', 'C', 'B', 'A', 'Infinite']
standstats_stats = ['dp', 'spd', 'rg', 'dur', 'pre', 'devp']

with open('txt/standname1.txt', 'r') as name1:
	standname1 = name1.read().splitlines()

with open('txt/standname2.txt', 'r') as name2:
	standname2 = name2.read().splitlines()

async def generate_name(ctx):
	name = f'{random.choice(standname1)} {random.choice(standname2)}'
	g.dict_standnames[ctx.message.author.id] = name
	await g.json_write('json/g.dict_standnames.json', g.dict_standnames)
	return f'**{ctx.message.author.nick}\'s Stand Name:**\n```fix\n『{name}』\n```'

async def get_name(ctx):
	return g.dict_standnames[ctx.message.author.id]

async def generate_stats(ctx):
	stats = {}
	for i in range(0, 6):
		stats[standstats_stats[i]] = random.choice(standstats_choices)
	output = (f'>>> Destructive Power (破壊力) - {stats["dp"]}\n'
	f'>>> Speed (スピード) - {stats["spd"]}\n'
	f'>>> Range (射程距離) - {stats["rg"]}\n'
	f'>>> Durability/Staying (持続力) - {stats["dur"]}\n'
	f'>>> Precision (精密動作性) - {stats["pre"]}\n'
	f'>>> Development Potential/Learning (成長性) - {stats["devp"]}')
	return f'**『{g.dict_standnames[ctx.message.author.id]}』\'s statistics:**\n```py\n{output}\n```'

async def save_stand_name(ctx):
	with open('txt/standnames_saved.txt', 'a+') as saved_names:
		saved_names.write(f'{g.dict_standnames[ctx.message.author.id]}\n')

async def get_saved_stand_names():
	with open('txt/standnames_saved.txt', 'r') as saved_names:
		return saved_names.read().splitlines()