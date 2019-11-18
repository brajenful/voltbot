import requests

async def main(q):
	url = 'http://api.apixu.com/v1/current.json'
	payload = {'key': '', 'q': ''}
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
