import time
import asyncio
import g

from twitch import TwitchClient

CLIENT_ID = 'w6h5tufp5eg7gu7szpivgfvc48qcej'
OAUTH_ID = 'bdzlkuug1khpy6mtfi1j16lyhh7a0w'
USERNAME = 'Volt669'

client = TwitchClient(CLIENT_ID, OAUTH_ID)

class UserGroup(object):

	def __init__(self, ctx, name, is_twitch:bool):
		self.name = name
		self.ctx = ctx
		self.is_twitch = is_twitch

		self.owner = self.ctx.message.author
		self.destination = self.ctx.message.channel

		self.users = []

		if self.is_twitch:
			self.channel = self.Channel(self.ctx, self.name, self.users)

		self.__add_owner()

	def __add_owner(self):
		self.users.append(self.owner)

	def _is_twitch(self):
		return self.is_twitch

	def get_owner(self):
		return self.owner.name

	def get_name(self):
		return self.name

	def get_users(self):
		usernames = []
		for user in self.users:
			usernames.append(user.name)
		return usernames

	def add_user(self, user):
		if user in self.users:
			return f'User {user.name} already exists in group {self.name}.'
		else:
			self.users.append(user)
			return f'User {user.name} added to group {self.name}.'

	def remove_user(self, user):
		if user in self.users:
			self.users.remove(user)
			return f'User {user.name} removed from group {self.name}.'
		else:
			return f'User {user.name} does not exist in group {self.name}.'

	class Channel(object):

		def __init__(self, ctx, name, users):
			self.ctx = ctx
			self.name = name
			self.users = users

			self.status = None
			self.last_status = None
			self.destination = self.ctx.message.channel

			try:
				self.id = client.users.translate_usernames_to_ids(self.name)[0]['id']
			except Exception as e:
				print(e)

			self.refresh_status()

		def get_channel_id(self):
			return self.id

		async def get_stream_status(self):
			if client.streams.get_stream_by_user(self.id):
				self.status = True
			else:
				self.status = False

			if self.status != self.last_status:
				if self.status:
					message = [user.mention for user in self.users]
					message = ' '.join(message)
					await g.client.send_message(self.destination, message)
					await g.client.send_message(self.destination, f'{self.name} is online.')
					self.last_status = True
				else:
					await g.client.send_message(self.destination, f'{self.name} is offline.')
					self.last_status = False

		async def __looper(self):
			while True:
				await self.get_stream_status()
				#print(self.status)
				await asyncio.sleep(30)

		def refresh_status(self):
			looper = asyncio.ensure_future(self.__looper())

if __name__ == 'main':	
	group = UserGroup('northernlion', False)
	print(group)