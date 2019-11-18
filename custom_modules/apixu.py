import requests

async def main(q):
	url = 'http://api.apixu.com/v1/current.json'
	payload = {'key': '595d5646dcb847f8a9e132542170308', 'q': ''}
	payload['q'] = q
	r = requests.get(url, params=payload, timeout=10)
	response = r.json()
	try:
		if r.json()['error']:
			return response['error']['message']
	except KeyError:
		return response


if __name__ == '__main__':
	while True:
		q = input('q: ')
		res = main(q)
		print(res)
