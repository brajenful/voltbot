import sys
import random
import asyncio

import g
import functions
import commands
"""
@g.client.event
async def on_command_error(error, ctx):
	if g.int_debug == 0:
		pass
	elif g.int_debug == 1:
		await g.client.send_message(ctx.message.channel, error)
	elif g.int_debug == 2:
		print(error)

@g.client.event
async def on_error(on_message, message):
	if g.int_debug == 0:
		pass
	elif g.int_debug == 1:
		await g.client.send_message(message.channel, sys.exc_info())
	elif g.int_debug == 2:
		print(sys.exc_info())
"""

async def on_ready():
	print('Logged in as')
	print(g.client.user.name)
	print(g.client.user.id)
	print('------')
	print('VOLTBOT')
	g.dict_custom = await g.json_read('json/g.dict_custom.json')
	g.dict_ignore = await g.json_read('json/g.dict_ignore.json')
	g.dict_standnames = await g.json_read('json/g.dict_standnames.json')
	g.dict_prefixes = await g.json_read('json/g.dict_prefixes.json')
	await functions.get_members()
	await functions.random_typing()
	#g.dict_streams = g._unpickle('g.dict_streams.pickle')
	#g.dict_groups = g._unpickle('g.dict_groups.pickle')
	#print(g.dict_streams)
	#for name, obj in g.dict_streams.items():
		#obj.channel.refresh_status()
"""
	if not g.client.opus.is_loaded():
		g.client.opus.load_opus('libopus-0.x86.dll')
		"""

async def on_message(message):

	if message.content == '_get globals().clear()':
		await g.client.send_message(message.channel, 'more like _get fucked lmao')
		for x in range(random.randint(0, 10)):
			await g.client.send_message(message.channel, message.author.mention)
		return

	with open('txt/messages.txt', 'a+', encoding='utf-8') as file:
		file.write(f'[{message.timestamp}][{message.server}({message.server.id})][#{message.channel}({message.channel.id})]\n{message.author}:{message.content}\n')
	
	if message.author.id in g.dict_ignore and message.author.id not in g.list_admins or message.author.id == '356382448935763968':
		return

	try:
		g.client.command_prefix = g.dict_prefixes[message.server.id]
	except KeyError:
		g.client.command_prefix = '_'

	try:
		await functions.onmessage_temperature(message)
		await functions.onmessage_cat(message)
		await functions.onmessage_goodbot(message)
		await functions.onmessage_badbot(message)
		await functions.onmessage_what(message)
		await functions.onmessage_thanks(message)
		await functions.onmessage_botmention(message)
		#await functions.onmessage_same(message)
	except KeyError as e:
		await g.client.send_message(message.channel, e)
	except PermissionError:
		await g.client.send_message(message.channel, 'PermissionError')
	g.dict_last_message[message.channel] = message
	#await functions.nice_serial(message)
	try:
		if await functions.process_loading_commands(message):
			return
		elif await functions.process_custom_commands(message):
			return
		else:
			await g.client.process_commands(message)
	except WikipediaException as e:
		await g.client.send_message(message.channel, e)

	await g.json_write('json/g.dict_custom.json', g.dict_custom)
	await g.json_write('json/g.dict_ignore.json', g.dict_ignore)
	await g.json_write('json/g.dict_standnames.json', g.dict_standnames)
	await g.json_write('json/g.dict_prefixes.json', g.dict_prefixes)
	#g._pickle('g.dict_streams.pickle', g.dict_streams)
	#g._pickle('g.dict_groups.pickle', g.dict_groups)

async def on_command(command, ctx):
	message = f'[{ctx.message.timestamp}][{ctx.message.author}][{ctx.message.server}][#{ctx.message.channel}][{ctx.message.content}]'
	print(message)
	with open('txt/command_log.txt', 'a+', encoding='utf-8') as file:
		file.write(f'{message}\n')

async def on_message_delete(message):
	with open('txt/deleted_messages.txt', 'a+', encoding='utf-8') as file:
		file.write(f'[{message.timestamp}][{message.server}({message.server.id})][#{message.channel}({message.channel.id})]\n{message.author}:{message.content}\n')