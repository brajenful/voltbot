import requests
import random

url = 'http://api.giphy.com/v1/gifs/search'
payload = {'key': 'hjqpAJJzAuGOZbazBCSQp7VDvvjhuhdw', 'q': '', 'limit': ''}

async def search_random(q, limit=25):
	if 'limit=' in q:
		qlist = q.split(' ')
		for i in qlist:
			if 'limit=' in i:
				limit = int(i.strip('limit='))
				del qlist[qlist.index(i)]
		payload['limit'] = limit
		payload['q'] = ' '.join(qlist)
	else:
		payload['limit'] = limit
		payload['q'] = q
	r = requests.get(url, params=payload, timeout=3)
	gifs = []
	for gif in r.json()['data']:
		gifs.append(gif['embed_url'])
	return gifs[random.randint(0, len(gifs)-1)]