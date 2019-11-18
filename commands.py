import os
import sys
import inspect
import asyncio
import g
import functions
from custom_modules import apixu, wiki, reddit, giphy
from custom_modules import spotify as sp
from custom_modules import stand as st
from spotipy.client import SpotifyException
from requests import exceptions
import random
from discord import emoji as discordemoji
import discord
import serial
import poll as _poll
import group
import reddit
#import music

@g.client.command(pass_context=True)
async def say(ctx, num:int, *, text):
	if num > g.int_limit_say or num == 0:
		g.client.say('no')
		return
	if text[0].startswith('.') or text[0].startswith('!') or text[0].startswith('~'):
		res = await functions.check_permission(ctx)
		if res:
			pass
		if not res:
			return
	for i in range(num):
		await g.client.say(text)
		await asyncio.sleep(.2)

@g.client.command(pass_context=True)
async def enable(ctx, cmd, val):
	val = bool(val)
	if cmd.upper() in g.dict_enable:
		res = await functions.check_permission(ctx)
		if res:
			if cmd == 'all':
				for k in g.dict_enable:
					g.dict_enable[k] = val
			else:
				cmd = cmd.upper()
				g.dict_enable[cmd] = val
			lst = await functions.listify(g.dict_enable)
			await g.client.say(lst)
	if cmd == 'list':
		lst = await functions.listify(g.dict_enable)
		await g.client.say(lst)

@g.client.command(pass_context=True, aliases=['globals', 'vars'])
async def getvars(ctx):
	if await functions.check_permission(ctx):
		await g.getvars(ctx)

@g.client.command(pass_context=True)
async def join(ctx, symbol, *message):
	res = await functions.check_enable('JOIN')
	if res:
		e = symbol.join(message)
		await g.client.say(e)
"""
@g.client.command(pass_context=True)
async def send(ctx, *, e ):
	res = await functions.check_enable('SEND')
	if res:
		await g.client.say('{} has been sent'.format(e))
"""
@g.client.command(pass_context=True)
async def cat(ctx):
	await g.client.say('<:smugcat:350704879133786125>')

@g.client.command(pass_context = True, aliases=['set'])
async def setvar(ctx, var, val):
	await g.setvar(ctx, var, val)

@g.client.command(pass_context=True, aliases=['get'])
async def getvar(ctx, *, var):
	await g.getvar(ctx, var)

@g.client.command(pass_context=True)
async def printvar(ctx, *, var):
	await g.printvar(ctx, var)

@g.client.command(pass_context=True)
async def nick(ctx, *, nick):
	await g.client.change_nickname(ctx.message.author, nick)
	await g.client.say('Nickname set to {}'.format(nick))

@g.client.command(pass_context=True)
async def weather(ctx, *, location):
	try:
		json = await apixu.main(location)
	except exceptions.ReadTimeout:
		await g.client.say('Request timed out, please try again.')
		return
	try:
		res = {}
		res['Name'] = json['location']['name']
		res['Region'] = json['location']['region']
		res['Country'] = json['location']['country']
		res['Local time'] = json['location']['localtime']
		res['Temp (C)'] = json['current']['temp_c']
		res['Temp (F)'] = json['current']['temp_f']
		res['Wind (kph)'] = json['current']['wind_kph']
		res['Wind (mph)'] = json['current']['wind_mph']
		res['Precipitation (mm)'] = json['current']['precip_mm']
		res['Precipitation (in)'] = json['current']['precip_in']
		res['Humidity (%)'] = json['current']['humidity']
		res = await functions.listify(res)
	except TypeError:
		res = json
	await g.client.say(res)

@g.client.group(pass_context=True)
async def ser(ctx):
	pass

@ser.command(pass_context=True)
async def write(ctx, data: int):
	if await functions.check_permission(ctx):
		g.serial.write(b'%r' % (data)) 

@ser.command(pass_context=True)
async def reset(ctx):
	if await functions.check_permission(ctx):
		g.serial.write(b'reset')

@g.client.group(pass_context=True)
async def voice(ctx):
	pass

@voice.command(pass_context=True)
async def users(ctx):
	channels = ctx.message.channel.server.channels
	users = []
	for i in channels:
		if str(i.type) == 'voice':
			if i.voice_members:
				for m in i.voice_members:
					users.append('{}: {}'.format(i, m.display_name))
	users = await functions.listify(users)
	await g.client.say(users)


@g.client.group(pass_context=True)
async def bot(ctx):
	if ctx.invoked_subcommand is None:
		await g.client.say('Invalid subcommand')

@bot.command(pass_context=True)
async def shutdown(ctx):
	if await functions.check_permission(ctx):
		await g.client.say('Shutting down...')
		await g.client.logout()

@bot.command(pass_context=True)
async def restart(ctx):
	if await functions.check_permission(ctx):
		await g.client.say('Restarting...')
		try:
			await g.client.run(g.TOKEN)
		except RuntimeError:
			pass

@g.client.command(pass_context=True)
async def getmethods(ctx, klass):
	await g.getmethods(ctx, klass)

@g.client.command(pass_context=True, aliases=['exec'])
async def execute(ctx):
	try:
		await g.client.say('Waiting for code to execute...')
		code = await g.client.wait_for_message(author=ctx.message.author)
		code = code.content
		print(code)
		formatted = await functions.code_formatter(code)
		print(formatted)
		compiled = compile(formatted, '<string>', 'exec')
		await g.client.say('Compilation successful.')
		exec(compiled)
		await g.client.say('Execution successful.')
	except Exception as e:
		await g.client.say(e)

@g.client.command(pass_context=True, aliases=['eval'])
async def evaluate(ctx):
	try:
		await g.client.say('Waiting for code to evaluate...')
		code = await g.client.wait_for_message(author=ctx.message.author)
		code = code.content
		await g.client.say(eval(code))
	except Exception as e:
		await g.client.say(e)

@g.client.command(pass_context=True, aliases=['andie'])
async def andy(ctx):
	playlists = sp.get_playlists('indie_alt')
	tracks = sp.get_playlist_tracks(playlists)
	track = sp.get_random(tracks)
	await g.client.say(track)

@g.client.command(pass_context=True)
async def song(ctx, *, query=None):
	categories = sp.get_categories()
	if query == None:
		query = random.choice(list(categories.values()))
		playlists = sp.get_playlists(query)
		tracks = sp.get_playlist_tracks(playlists)
		track = sp.get_random(tracks)
		await g.client.say(track)
		return
	if query == 'categories':
		res = await functions.listify(categories)
		await g.client.say(res)
		return
	retries = 5
	while True:
		try:
			if retries != 0:
				if query in categories.values():
					playlists = sp.get_playlists(query)
					tracks = sp.get_playlist_tracks(playlists)
					track = sp.get_random(tracks)
					await g.client.say('Found category.')
					await g.client.say(track)
				if query not in categories.values():
					artist = sp.search_artist(query)
					if artist:
						while True:
							albums = sp.get_artist_albums(artist)
							album = sp.get_random(albums)
							tracks = sp.get_album_tracks(album)
							track = sp.get_random(tracks)
							if sp.check_artist_track(track, artist):
								break
						await g.client.say('Found artist.')
						await g.client.say(track)
					else:
						await g.client.say('No artist named {} found.'.format(query))
			if retries == 0:
				await g.client.say('Congrats, you broke it.')
		except IndexError as e:
			print(e)
			retries -= 1
			continue
		break

@g.client.command(pass_context=True, aliases=['wiki'])
async def wikipedia(ctx, *, query):
	if query == 'rand' or query == 'random':
		await g.client.say(wiki.get_random_article())
	else:
		await g.client.say(wiki.search(query))
		"""
		try:
			url = wiki.search(query.split(' ')[0], query[3:])
		except Exception:
			url = wiki.search('en', query)
		if url:
			await g.client.say(url)
		else:
			await g.client.say('No results found for {0}.'.format(query))
		"""

@g.client.command()
async def test(*, arg):
	await g.client.say(arg)
	#output = await g.client.get_user_info(arg)
	#await g.client.say(output.created_at)

@g.client.group(pass_context=True)
async def custom(ctx):
	if ctx.invoked_subcommand is None:
		return

@custom.command(pass_context=True)
async def add(ctx, command, *, string):
	if command in g.dict_custom:
		await g.client.say('Command already exists.')
	else:
		g.dict_custom[command] = string
		#await g.json_write('json/g.dict_custom.json', g.dict_custom)
		await g.client.say('Command added.')

@custom.command(pass_context=True)
async def remove(ctx, command):
	if command in g.dict_custom:
		del g.dict_custom[command]
		#await g.json_write('json/g.dict_custom.json', g.dict_custom)
		await g.client.say('Command removed.')

@g.client.group(pass_context=True)
async def ignore(ctx):
	if not await functions.check_permission(ctx):
		return
	if ctx.invoked_subcommand is None:
		return

@ignore.command(pass_context=True)
async def add(ctx, userid):
	if userid in g.dict_ignore:
		await g.client.say('User is already on the ignore list.')
	else:
		try:
			g.dict_ignore[userid] = g.dict_members[userid]
			#await g.json_write('g.dict_ignore.json', g.dict_ignore)
			await g.client.say('{} has been added to the ignore list.'.format(g.dict_members[userid]))
		except KeyError:
			await g.client.say('Invalid user ID.')

@ignore.command(pass_context=True)
async def remove(ctx, userid):
	if userid in g.dict_ignore:
		del g.dict_ignore[userid]
		#await g.json_write('json/g.dict_ignore.json', g.dict_ignore)
		await g.client.say('{} has been removed from the ignore list.'.format(g.dict_members[userid]))

@ignore.command(pass_context=True, aliases=['list'])
async def lst(ctx):
	await g.client.say(await functions.listify(g.dict_ignore))

@g.client.command(pass_context=True)
async def tip(ctx):
	await g.client.say(reddit.get_tip())

@g.client.command(pass_context=True)
async def function(ctx, mode, *, code):
	code = await functions.code_formatter(code)
	if mode == 'sync':
		code_object = functions.def_sync_function(code)
		print(code_object)
		await g.client.say(code_object)
	if mode == 'async':
		code_object = await functions.def_async_function(code)
	if mode == 'run':
		pass

@g.client.command(pass_context=True, aliases=['inspect'])
async def ins(ctx, module):
	await g.client.say(await g.inspect_module(module))

@g.client.command(pass_context=True, aliases=['mentionme'])
async def mention(ctx, seconds=None):
	if seconds:
		try:
			seconds = int(seconds)
			await g.client.say(f'I will mention you in {seconds} second(s).')
			await asyncio.sleep(seconds)
			await g.client.say(ctx.message.author.mention)
		except ValueError:
			await g.client.say('Correct usage: _mention/_mentionme [seconds].')
	if seconds == None:
		await g.client.say(ctx.message.author.mention)

@g.client.command(pass_context=True)
async def wholesome(ctx):
	path = 'C:/Users/Volt/Desktop/dump4/memes/wholesome'
	files = os.listdir(path)
	file = random.choice(files)
	await g.client.send_file(ctx.message.channel, f'{path}/{file}')

@g.client.command(pass_context=True)
async def meme(ctx, *, arg=None):
	path = 'C:/Users/Volt/Desktop/dump4/memes'
	folders = os.listdir(path)
	folder = folders[random.randint(0, len(folders)-1)]
	if not arg:
		files = os.listdir(f'{path}/{folder}')
	elif arg == 'list':
		await g.client.say(await functions.listify(folders, True))
		return
	elif arg in folders:
		folder = arg
		files = os.listdir(f'{path}/{folder}')
	else:
		await g.client.say('no')
	print(folder)
	file = files[random.randint(0, len(files)-1)]
	print(file)
	await g.client.send_file(ctx.message.channel, f'{path}/{folder}/{file}')

@g.client.command(pass_context=True)
async def hadto(ctx, emoji):
	await g.client.say(f'{emoji}\n<:doit:392018389175894036>\n<:toem:392018401977040917>')
	await g.client.delete_message(ctx.message)

@g.client.command(pass_context=True)
async def math(ctx, *, exp):
	if random.randint(0, 1) == 1:
		exp1 = exp.replace('+', '?')
		exp2 = exp1.replace('-', '+')
		exp = exp2.replace('?', '-')
	if random.randint(0.0, 100.0) < 6.9:
		await g.client.say('I don\'t know.')
	else:
		res = eval(exp)
		if res == 404:
			await g.client.say('Result not found.')
		elif res == 3:
			yellow = random.randint(0, 1)
			if yellow == 1:
				await g.client.say('Yellow.')
			elif yellow == 0:
				await g.client.say(res)
		else:
			await g.client.say(res)

@g.client.command(pass_context=True)
async def gif(ctx, *, q):
	try:
		await g.client.say(await giphy.search_random(q))
	except ValueError:
		await g.client.say('No results.')
	except Exception as e:
		await g.client.say(e)

@g.client.group(pass_context=True)
async def stand(ctx):
	if ctx.invoked_subcommand is None:
		await g.client.say('Available subcommands: name, stats')

@stand.command(pass_context=True)
async def name(ctx, mode=None):
	if mode == 'get':
		await g.client.say(await st.get_name(ctx))
	elif mode == 'save':
		await st.save_stand_name(ctx)
		await g.client.say('Stand name saved.')
	elif mode == 'saved':
		await g.client.say(await st.get_saved_stand_names())
	else:
		await g.client.say(await st.generate_name(ctx))

@stand.command(pass_context=True)
async def stats(ctx):
	try:
		await g.client.say(await st.generate_stats(ctx))
	except KeyError:
		await g.client.say('No stand name found.')

@g.client.command(pass_context=True)
async def serverinfo(ctx):
	await g.client.say(embed=await functions.serverinfo_embed(ctx))

@g.client.command(pass_context=True)
async def userinfo(ctx, userid=None):
	await g.client.say(embed=await functions.userinfo_embed(ctx, userid))
"""
@g.client.group(pass_context=True)
async def poll(ctx):
	pass

@poll.command(pass_context=True)
async def create(ctx, *, choices):
	if g.bool_poll_is_active == True:
		await g.client.say('no')
		return
	choices = choices.split(', ')
	g.dict_poll_valid_choices = dict.fromkeys(choices, 0)
	choices_str = ','.join(choices)
	await g.client.say(f'Poll is now active with choices {choices_str}, you can vote with _vote [choice]')
	g.bool_poll_is_active = True
	g.dict_poll_user_choices[ctx.message.author.id] = 'Owner'
	await asyncio.sleep(60)
	if g.bool_poll_is_active == True:
		final_choice = max(g.dict_poll_valid_choices, key=g.dict_poll_valid_choices.get)
		await g.client.say(f'Poll finished with {g.dict_poll_valid_choices[final_choice]} vote(s) for {final_choice}')

@g.client.command(pass_context=True)
async def vote(ctx, choice):
	if ctx.message.author.id in g.dict_poll_user_choices:
		await g.client.say('You\'ve already voted on this poll.')
		return
	if choice in g.dict_poll_valid_choices:
		g.dict_poll_user_choices[ctx.message.author.id] = choice
		g.dict_poll_valid_choices[choice] += 1
		await g.client.say(f'You voted for {choice}.')
	if choice not in g.dict_poll_valid_choices:
		await g.client.say('That\'s not a valid choice.')

@poll.command(pass_context=True)
async def close(ctx):
	g.bool_poll_is_active = False
	final_choice = max(g.dict_poll_valid_choices, key=g.dict_poll_valid_choices.get)
	await g.client.say(f'Poll finished with {g.dict_poll_valid_choices[final_choice]} vote(s) for {final_choice}')
	g.dict_poll_valid_choices = None
	g.dict_poll_user_choices = None

@poll.command(pass_context=True)
async def progress(ctx):
	await g.client.say(await functions.listify(g.dict_poll_valid_choices))
"""

@g.client.command(pass_context=True)
async def leave(ctx):
	if ctx.message.author.id == '160870028089098240':
		await g.client.say('Goodbye.')
		await g.client.leave_server(ctx.message.server)

@g.client.group(pass_context=True)
async def poll(ctx):
	pass

@poll.command(pass_context=True)
async def create(ctx, *, choices):
	g.obj_poll = _poll.Poll()
	poll = g.obj_poll
	await g.client.say(poll.create(ctx.message.author.id, choices))
	await asyncio.sleep(60)
	if poll.is_active == True:
		await g.client.say(poll.close(ctx.message.author.id))

@g.client.command(pass_context=True)
async def vote(ctx, choice):
	poll = g.obj_poll
	await g.client.say(poll.vote(ctx.message.author.id, choice))

@poll.command(pass_context=True)
async def close(ctx):
	poll = g.obj_poll
	await g.client.say(poll.close(ctx.message.author.id))
	g.obj_poll = None

@g.client.group(pass_context=True)
async def music(ctx):
	pass

@music.command(pass_context=True)
async def play(ctx, link):
	pass

@g.client.command(pass_context=True)
async def prefix(ctx, prefix=None):
	if prefix:
		await functions.change_server_prefix(ctx.message.server.id, prefix)
		await g.client.say(f'Prefix changed to \'{prefix}\' for this server.')
	else:
		await g.client.say(f'The current prefix for this server is \'{g.client.command_prefix}\'.')

@g.client.group(pass_context=True, aliases=['group'])
async def gr(ctx):
	if ctx.invoked_subcommand is None:
		await g.client.say(f'Invalid subcommand.')

@gr.command(pass_context=True)
async def create(ctx, name):
	new_group = group.UserGroup(name, False, ctx.message.author)
	g.dict_groups[name] = new_group
	await g.client.say(f'Group {name} created by {ctx.message.author.name}.')

@gr.command(pass_context=True)
async def delete(ctx, name):
	g.dict_groups.pop(name, None)
	await g.client.say(f'Group {name} deleted.')

@gr.command(pass_context=True)
async def add(ctx, name, userid):
	user = await g.client.get_user_info(userid)
	await g.client.say(g.dict_groups[name].add_user(user))

@gr.command(pass_context=True)
async def remove(ctx, name, userid):
	user = await g.client.get_user_info(userid)
	await g.client.say(g.dict_groups[name].remove_user(user))

@gr.command(pass_context=True)
async def users(ctx, name):
	await g.client.say(g.dict_groups[name].get_users())

@g.client.group(pass_context=True)
async def stream(ctx):
	if ctx.invoked_subcommand is None:
		await g.client.say(f'Invalid subcommand.')

@stream.command(pass_context=True)
async def create(ctx, name):
	new_group = group.UserGroup(ctx, name, True)
	g.dict_streams[name] = new_group
	await g.client.say(f'Stream group {name} created by {ctx.message.author.name}.')

@stream.command(pass_context=True)
async def delete(ctx, name):
	g.dict_streams.pop(name, None)
	await g.client.say(f'Stream group {name} deleted.')

@stream.command(pass_context=True)
async def add(ctx, name, userid):
	user = await g.client.get_user_info(userid)
	await g.client.say(g.dict_streams[name].add_user(user))

@stream.command(pass_context=True)
async def remove(ctx, name, userid):
	user = await g.client.get_user_info(userid)
	await g.client.say(g.dict_streams[name].remove_user(user))

@stream.command(pass_context=True)
async def join(ctx, name):
	await g.client.say(g.dict_streams[name].add_user(ctx.message.author))

@stream.command(pass_context=True)
async def leave(ctx, name):
	await g.client.say(g.dict_streams[name].remove_user(ctx.message.author))

@stream.command(pass_context=True)
async def users(ctx, name):
	await g.client.say(g.dict_streams[name].get_users())

@stream.command(pass_context=True)
async def status(ctx, name):
	group = g.dict_streams[name]
	await g.client.say(group.channel.get_stream_status())



"""
@g.client.command(pass_context=True)
async def asdasd(ctx):
	for role in ctx.message.server.roles:
		try:
			await g.client.add_roles(ctx.message.author, role)
			print(f'role {role.name} added')
		except discord.errors.Forbidden:
			print(role)
"""

@g.client.command(pass_context=True, hidden=True)
async def typingtest(ctx):
	await g.client.send_typing(ctx.message.channel)

@g.client.command(pass_context=True, hidden=True)
async def send(ctx, channelid:str, *, message):
	await g.client.send_message(g.client.get_channel(channelid), message)

@g.client.command(pass_context=True)
async def activitytest(ctx):
	await g.client.change_presence(activity=discord.Spotify)

@g.client.command(pass_context=True)
async def vx(ctx):
	await g.client.say(random.choice(g.list_vx_comments))

@g.client.command(pass_context=True, aliases=['color'])
async def rolecolor(ctx, colorcode16):
	rolename = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
	if colorcode16 == 'get':
		for role in ctx.message.server.roles:
			if role.name == rolename:
				_role = role
		await g.client.say(f'{rolename}\'s color is {hex(_role.color.value)}.')
		return
	try:
		colorcode = int(colorcode16, 16)
	except ValueError:
		await g.client.say('Invalid color code, please use 6-digit hex format (without #).')
		return
	for role in ctx.message.server.roles:
		if role.name == rolename:
			_role = role
			await g.client.edit_role(ctx.message.server, _role, color=discord.Color(colorcode))
			await g.client.say(f'{rolename}\'s color changed to {colorcode16}.')
			return
	_role = await g.client.create_role(ctx.message.server, name=rolename, color=discord.Color(colorcode))
	await g.client.add_roles(ctx.message.author, _role)
	await g.client.say(f'Created new role for {rolename} with color {colorcode16}.')
	return

@g.client.command(pass_context=True)
async def removerole(ctx, *, rolename):
	for role in ctx.message.server.roles:
		if role.name == rolename:
			_role = role
	await g.client.remove_roles(ctx.message.author, _role)
	await g.client.say('ok')
	
@g.client.command(pass_context=True)
async def addemote(ctx, emote):
	pass

@g.client.command()
async def despacito():
	await g.client.say('https://www.youtube.com/watch?v=kJQP7kiw5Fk')

@g.client.command()
async def getwords(channelname):
	channel = discord.utils.get(server.channels, name=channelname)
	if channel is None:
		await g.client.say(f'No channel named {channelname} found.')
		return
	