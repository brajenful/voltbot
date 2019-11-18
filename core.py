import logging
import discord
import asyncio
import time
import random
import sys
import json
from discord.ext import commands as com
from discord.errors import DiscordException

import g
g.init()

import functions
import commands
import events

logging.basicConfig(level=logging.INFO)

@g.client.event
async def on_ready():
	await events.on_ready()

@g.client.event
async def on_message(message):
	await events.on_message(message)

@g.client.event
async def on_command(command, ctx):
	await events.on_command(command, ctx)

@g.client.event
async def on_message_delete(message):
	await events.on_message_delete(message)

if __name__ == '__main__':
	g.client.run(g.TOKEN)