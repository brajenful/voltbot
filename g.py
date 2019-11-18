import logging
import discord
import asyncio
import serial, time
import random
import sys
import json
from discord.ext import commands as com
import inspect
import json
import importlib
import pickle

import functions
from custom_modules import poll
from custom_modules import reddit

def init():

	sys.path.append('custom_modules')

	global client
	global serial

	client = com.Bot(command_prefix='_', description=None, max_messages=999999)
	#serial = serial.Serial('COM7', 9600, timeout=.1)

	global TOKEN

	global int_limit_say
	global int_debug
	global int_cat_max
	global int_what_max

	global dict_enable
	global dict_last_message
	global dict_last_author
	global dict_samecount
	global dict_whatcount
	global dict_custom
	global dict_ignore
	global dict_members
	global dict_standnames
	global dict_standstats
	global dict_poll_valid_choices
	global dict_poll_user_choices
	global dict_prefixes
	global dict_commands
	global dict_groups
	global dict_streams

	global list_admins
	global list_ban
	global list_loading
	global list_vx_comments

	global str_reg
	global str_tiny

	global bool_poll_is_active

	global obj_poll
	global obj_player_client

	TOKEN = ''
	
	int_limit_say = 2
	int_debug = 1
	int_cat_max = 10
	int_what_max = 20

	dict_enable = {'WHAT': True, 'CAT': True, 'SAY': True, 'SEND': True, 'JOIN': True}
	dict_last_message = {}
	dict_last_author = {}
	dict_samecount = {}
	dict_whatcount = {}
	dict_custom = {}
	dict_ignore = {}
	dict_members = {}
	dict_standnames = {}
	dict_standstats = {}
	dict_poll_valid_choices = {}
	dict_poll_user_choices = {}
	dict_prefixes = {366386144947994625: '_'}
	dict_commands = client.__dict__['commands']
	dict_groups = {}
	dict_streams = {}
	#TODO put the commands init function in events.on_ready

	list_admins = ['160870028089098240','151558788325965826']
	list_ban = ['273200524206145537', '178375458843262976']
	list_loading = ['song', 'wiki', 'weather', 'wholesome', 'meme', 'tip', 'gif']
	list_commands = []
	#list_vx_comments = reddit.get_user_comments('VXJunkies_SS', 500)

	str_tiny = 'ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏᶫᵐᶰᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹⁰'
	str_reg = 'abcdefghijklmnopqrstuvwxyz1234567890'

	bool_poll_is_active = False

	obj_poll = None
	obj_player_client = None

async def json_read(file):
	with open(file, 'r+') as f:
		return json.load(f)

async def json_write(file, var):
	with open(file, 'w+') as f:
		json.dump(var, f)

async def getvars(ctx):
	res = await functions.check_permission(ctx)
	if res:
		lst = []
		for key, value in globals().items():
			if '__' not in key:
				if 'int' in key or 'dict' in key or 'list' in key:
					lst.append(key)
		lst = await functions.listify(lst, True)
		await client.say(lst)

async def setvar(ctx, var, val):
	res = await functions.check_permission(ctx)
	if res:
		globals()[var] = eval(val)
		await client.say('{} = {}'.format(var, val))

async def getvar(ctx, var):
	var = eval(var)
	await client.say(type(var))
	if type(var).__name__ == 'dict':
		var = await functions.listify(var)
	await client.say(var)

async def execute(code):
	exec(code)
	await client.say('Code successfully executed.')

async def inspect_module(module):
	module = importlib.import_module(module)
	return dir(module)

async def printvar(ctx, var):
	var = eval(var)
	print(type(var))
	if type(var).__name__ == 'dict':
		var = await functions.listify(var)
	print(var)

def get_commands():
	for command in dict_commands:
		command = command.__repr__()

def _pickle(path, file):
	with open(path, 'wb') as outfile:
		pickle.dump(file, outfile)

def _unpickle(file):
	with open(file, 'rb') as infile:
		return pickle.load(infile)
