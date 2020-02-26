import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import pprint

client = None

track_list = []
track_name_list = []
username = SPOTIFY_USER_NAME

def authenticate():
	scope = "playlist-modify-public"
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username=username))
	return sp

def get_artist_uri(artist_name):
	result = client.search(q='artist:' + artist_name, type='artist')
	artist = result['artists']['items'][0]
	name = artist['name']
	uri = artist['uri']
	return uri

def add_artist_top_track_to_tracklist(artist_uri):
	response = client.artist_top_tracks(artist_uri)
	for track in response['tracks'][0:2]:
		track_list.append(track['uri'])
		track_name_list.append(track['name'])

def get_related_artists(artist_uri):
	related = client.artist_related_artists(artist_uri)

	for related_artist in related['artists']:
		print('  ', related_artist['name'])
		related_artist_uri = related_artist['uri']
		add_artist_top_track_to_tracklist(related_artist_uri)

	#print(track_list)
	#print(track_name_list)

def create_playlist(artist_name):
	playlist_name = "Friends of " + artist_name
	print("Creating playlist: " + playlist_name)

	new_playlist = client.user_playlist_create(username, playlist_name)
	playlist_id = new_playlist['id']
	results = client.user_playlist_add_tracks(username, playlist_id, track_list)
	print(results)
		
def main():
	global client
	
	if len(sys.argv) > 1:
		artist_name = sys.argv[1]
	else:
		artist_name = 'metallica'

	print("Getting track list for: {}".format(artist_name))

	client = authenticate()

	artist_uri = get_artist_uri(artist_name)

	get_related_artists(artist_uri)

	create_playlist(artist_name)

main()

