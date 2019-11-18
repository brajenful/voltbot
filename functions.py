import logging
import discord
import asyncio
import serial, time
import random
import sys
import json
from discord.ext import commands as com
from discord.errors import DiscordException

import g

async def check_permission(ctx):
	userid = ctx.message.author.id
	if userid in g.list_admins:
		return True
	else:
		return False

async def check_enable(cmd):
	cmd = str(cmd)
	cmd = cmd.upper()
	if g.dict_enable[cmd]:
		return True
	else:
		return False

async def onmessage_temperature(message):
	msg = message.content
	if 'C' in msg:
		lst = msg.split(' ')
		for i in lst:
			if 'C' in i:
				if not i.startswith('C'):
					try:
						c = int(i.strip('C'))
						f = await convert(c, 'C')
						msg = '{0}C = {1}F'.format(c, f)
						await g.client.send_message(message.channel, msg)
					except ValueError:
						pass
					
	elif 'F' in msg:
		lst = msg.split(' ')
		for i in lst:
			if 'F' in i:
				if not i.startswith('F'):
					try:
						f = int(i.strip('F'))
						c = await convert(f, 'F')
						msg = '{0}F = {1}C'.format(f, c)
						await g.client.send_message(message.channel, msg)
					except ValueError:
						pass

async def convert(num:int, unit:str):
	if unit == 'C':
		res = num * 1.8 + 32
		return int(res)
	if unit == 'F':
		res = (num - 32) // 1.8
		return int(res)

async def onmessage_what(message):
	res = await check_enable('WHAT')
	if res:
		if message.content.lower() == 'what':
			num_what = random.randint(0, g.int_what_max)
			if num_what == 0:
				table = str.maketrans(g.str_tiny, g.str_reg)
				output = g.dict_last_message[message.channel].content.translate(table)
				output = output.upper()
				await g.client.send_message(message.channel, output)

async def onmessage_cat(message):
	res = await check_enable('CAT')
	if res:
		if 'cat' in message.content.lower():
			num_cat = random.randint(0, g.int_cat_max)
			if num_cat == 0:
				await g.client.add_reaction(message, 'smugcat:350704879133786125')
			
async def onmessage_goodbot(message):
	if message.content.lower() == 'good bot':
		await g.client.send_message(message.channel, 'thank')

async def onmessage_badbot(message):
	if message.content.lower() == 'bad bot':
		await g.client.send_message(message.channel, 'heck u')

async def onmessage_same(message):
	if message.author != g.dict_last_message[message.channel].author:
		if message.content == g.dict_last_message[message.channel].content:
			g.dict_samecount[message.channel.name] += 1
		else:
			g.dict_samecount[message.channel.name] = 0
	if g.dict_samecount[message.channel.name] == 3:
		g.dict_samecount[message.channel.name] = 0
		await g.client.send_message(message.channel, g.dict_last_message[message.channel].content)
		
async def listify(dct, lst=False):
	if not lst:
		lst = []
		for key, value in dct.items():
			lst.append('{}: {}'.format(key, value))
		lst.insert(0, '```')
		lst.append('```')
		return '\n'.join(lst)
	if lst:
		lst = dct
		lst.insert(0, '```')
		lst.append('```')
		return '\n'.join(lst)
	
def listify_sync(dct, lst=False):
	if not lst:
		lst = []
		for key, value in dct.items():
			lst.append('{}: {}'.format(key, value))
		lst.insert(0, '```')
		lst.append('```')
		return '\n'.join(lst)
	if lst:
		lst = dct
		lst.insert(0, '```')
		lst.append('```')
		return '\n'.join(lst)

async def nice_serial(message):
	if message.content.lower() == 'nice'.lower():
		g.serial.write(b'1')

async def process_custom_commands(message):
	if message.content.startswith('_'):
		command = message.content.strip('_')
		command = command.split(' ')[0]
		if command in g.dict_custom:
			await g.client.send_message(message.channel, g.dict_custom[command])
			return True

async def get_members():
	for server in g.client.servers:
		g.dict_members[server.id] = {}
		for member in server.members:
			g.dict_members[server.id][member.id] = member

async def code_formatter(code, name=None):
	code_feed = []
	if '```' in code:
		code = code.strip('```')
		return code
	else:
		return code
		"""
	if name:
		return code.split(' ')[1]
	list_code = code.split(' ')
	list_code = list_code[0].strip('\n')
	for element in code_generator(list_code):
		print(element)
"""
def code_generator(code_list):
	code_feed = []
	for element in code_list:
		code_feed.append(element)
		if '\n' in element:
			yield code_feed

def def_sync_function(code):
	return compile(code, '<string>', 'exec')

async def oncommand_addemoji(message):
	await g.client.add_reaction(message, 'a:loading:432572804601217035')

async def oncommand_removeemoji(message):
	await g.client.remove_reaction(message, 'a:loading:432572804601217035', g.client.user)

async def process_loading_commands(message):
	if message.content.startswith('_'):
		command = message.content.strip('_')
		command = command.split(' ')[0]
		if command in g.list_loading:
			await oncommand_addemoji(message)
			await g.client.process_commands(message)
			await oncommand_removeemoji(message)
			return True

async def onmessage_senpai(message):
	if 'senpai' in message.content.lower():
		if message.author.id == '209389248921600000':
			await g.client.delete_message(message)

async def onmessage_thanks(message):
	if random.randint(0, 10) == 10:
		if message.content.lower() == 'thanks':
			await g.client.send_message(message.channel, 'You\'re welcome.')

async def serverinfo_embed(ctx):
	text_channel_count = 0
	voice_channel_count = 0
	role_count = 0
	server = ctx.message.server
	for channel in list(server.channels):
		if str(channel.type) == 'text':
			text_channel_count += 1
		elif str(channel.type) == 'voice':
			voice_channel_count += 1
	for role in server.roles:
		role_count += 1
	embed = discord.Embed(color=ctx.message.author.color)
	embed.set_thumbnail(url=server.icon_url)
	embed.add_field(name=server.name, value=server.created_at.date(), inline=False)
	embed.add_field(name='Region', value=server.region, inline=False)
	embed.add_field(name='Users', value=server.member_count, inline=False)
	embed.add_field(name='Text Channels', value=text_channel_count, inline=False)
	embed.add_field(name='Voice Channels', value=voice_channel_count, inline=False)
	embed.add_field(name='Roles', value=role_count, inline=False)
	embed.add_field(name='Owner', value=server.owner, inline=False)
	embed.set_footer(text=f'Server ID: {server.id}')
	return embed

async def userinfo_embed(ctx, userid, is_member=False):
	if userid:
		if userid in g.dict_members[ctx.message.server.id]:
			user = g.dict_members[ctx.message.server.id][userid]
			is_member = True
		else:
			for serverid in g.dict_members:
				if userid in g.dict_members[serverid]:
					user = g.dict_members[serverid][userid]
					is_member = True
					break
		if is_member == False:
			user = await g.client.get_user_info(userid)
	else:
		user = ctx.message.author
	if is_member == True:
		roles = []
		for role in user.roles:
			if not role.is_everyone:
				roles.append(role.name)
		roles = ', '.join(roles)
		embed = discord.Embed(color=user.color)
		embed.set_thumbnail(url=user.avatar_url)
		embed.add_field(name=f'{user.name}#{user.discriminator} - {user.nick}', value=user.status, inline=False)
		embed.add_field(name='Joined Discord on', value=user.created_at.date(), inline=False)
		embed.add_field(name='Joined this server on', value=user.joined_at.date(), inline=False)
		embed.add_field(name='Roles', value=roles, inline=False)
		embed.set_footer(text=f'User ID: {user.id}')
	if is_member == False:
		embed = discord.Embed()
		embed.set_thumbnail(url=user.avatar_url)
		embed.add_field(name=f'{user.name}#{user.discriminator}', value=user.display_name, inline=False)
		embed.add_field(name='Joined Discord on', value=user.created_at.date(), inline=False)
		embed.set_footer(text=f'User ID: {user.id}')
	return embed

async def onmessage_botmention(message):
	if g.client.user.mentioned_in(message):
		await g.client.send_message(message.channel, 'hi')

async def change_server_prefix(serverid, prefix):
	g.dict_prefixes[serverid] = prefix
	#await g.json_write('json/g.dict_prefixes.json', g.dict_prefixes)
async def random_typing():
	for i in range(sys.maxsize):
		await asyncio.sleep(random.randint(300, 3600))
		server = random.choice(list(g.client.servers))
		channel = random.choice(list(server.channels))
		await g.client.send_typing(channel)
		print(f'Typing sent to {channel} ({server})')
