class Player(object):

	def __init__(self, ctx, client):
		self.ctx = ctx
		self.client = client

		self.server = None
		self.channel = None
		self.player = None
		self.creator_id = ctx.message.author.id
		self.queue = []

	def create_player(self, link):
		if self.player:
			return 'Player client already exists.'
		self.player = await self.client.create_ytdl_player(link)
		self.loop()

	def add_song(self, link):
		if (len(self.queue) != 0):
			self.queue.append(link)
		if (len(self.queue) == 0):
			self.create_player(link)

	def loop(self):
		self.client.start()
		for milliseconds in (self.client.duration*10):
			if self.player.is_playing():
				pass
			if self.player.is_done():
				self.player = None
				self.create_player(queue[0])
