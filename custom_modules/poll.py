import functions

class Poll(object):

	def __init__(self):
		self.userid = None
		self.choices = None
		self.valid_choices = {}
		self.user_choices = {}
		self.is_active = False
		self.final_choice = None
		self.choices_str = None

	def create(self, userid, choices):
		self.is_active = True
		self.userid = userid
		self.choices = choices.split(', ')
		self.choices_str = ','.join(self.choices)
		self.valid_choices = dict.fromkeys(self.choices, 0)
		if len(self.choices) < 2:
			return 'You can\'t create a poll with less than 2 choices.'
		else:
			return f'Poll is now active with choices {self.choices_str}, you can vote with _vote [choice]'

	def close(self, userid):
		self.is_active = False
		if userid == self.userid:
			return self.get_result()
			

	def vote(self, userid, choice):
		#if userid == self.userid:
		#	return 'You can\'t vote on your own poll.'
		if userid in self.user_choices:
			return 'You\'ve already voted on this poll.'
		elif choice in self.valid_choices:
			self.user_choices[userid] = choice
			self.valid_choices[choice] += 1
			return f'You voted for {choice}.'

	def get_result(self):
		"""
		valid_choices_lst = list(self.valid_choices.values())
		valid_choices_lst = ['1', '6', '23']
		valid_choices_lst.sort()
		return valid_choices_lst
		return f'Poll finished with {self.valid_choices[self.final_choice]} vote(s) for {self.final_choice}.'
		"""
		return f'Poll finished with the following results:\n{functions.listify_sync(self.valid_choices)}'
