import wikipedia
import random

def get_random_article():
	title = wikipedia.random(pages=1)
	title = title.split(' ')
	title = '_'.join(title)
	url = add_url('en', title)
	return url

def add_url(lang, title):
	return 'https://wikipedia.org/{0}/{1}'.format(lang, title)

def search(query):
	try:
		wikipedia.set_lang('en')
		try:
			article = wikipedia.page(wikipedia.search(query, results=1))
			return article.url
		except wikipedia.exceptions.DisambiguationError as e:
			while True:
				try:
					article = wikipedia.page(wikipedia.search(random.choice(e.args[1]), results=1))
					return f'The term {e.args[0]} yielded multiple results, so I selected one at random.\n{article.url}'
				except wikipedia.exceptions.DisambiguationError:
					continue
	except wikipedia.exceptions.WikipediaException as e:
		return e

	"""
	title = str(title)
	title = title.strip("['']")
	title = title.split(' ')
	title = '_'.join(title)
	if title:
		url = add_url(lang, title)
		return url
		"""

#print(search('en', 'voltage'))