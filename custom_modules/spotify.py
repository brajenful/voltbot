import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

client_id = '7afc9b24d7a14ba1bba12cb9a1b2c549'
client_secret = '5314e7d16ba24e709fbeb6ed30f5482e'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlists(category_id):
	playlists = []
	json = spotify.category_playlists(category_id=category_id)
	for i in json['playlists']['items']:
		playlists.append(i['id'])
	return playlists

def get_playlist_tracks(playlists):
	num = random.randint(0, len(playlists)-1)
	tracks = []
	json = spotify.user_playlist('spotify',playlist_id=playlists[num], fields='tracks(items(track(external_urls(spotify))))')
	for i in json['tracks']['items']:
		tracks.append([i['track']['external_urls']['spotify']])
	return tracks

def get_random(lst):
	num = random.randint(0, len(lst)-1)
	lst = lst[num]
	return str(lst).strip("['']")

def get_categories():
	categories = {}
	json = spotify.categories()
	for i in json['categories']['items']:
		categories[i['name']] = i['id']
	return categories

def search_artist(artist):
	json = spotify.search(artist, type='artist')
	for i in json['artists']['items']:
		if artist.lower() in i['name'].lower():
			return i['id']
	return json['artists']['items'][0]['id']

def get_artist_albums(artist_id):
	albums = []
	json = spotify.artist_albums(artist_id)
	for i in json['items']:
		albums.append(i['id'])
	return albums

def get_album_tracks(album_id):
	tracks = []
	json = spotify.album_tracks(album_id)
	for i in json['items']:
		tracks.append(i['external_urls']['spotify'])
	return tracks

def check_artist_track(track_id, artist_id):
	track_json = spotify.track(track_id)
	for i in track_json['artists']:
		if i['id'] == artist_id:
			return True
	return False

def search(query, mode):
	return spotipy.search(query, type=mode)