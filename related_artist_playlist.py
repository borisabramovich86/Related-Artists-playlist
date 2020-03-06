import spotipy
import sys
import argparse
import pprint
import os
from spotipy.oauth2 import SpotifyOAuth

spotify_username = os.environ['SPOTIFY_USER_NAME']
TRACKS_PER_RELATED_ARTIST = 2

spotify_client = None
track_list = []
track_name_list = []

def authenticate():
	scope = "playlist-modify-public"
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username=spotify_username))
	return sp

def chunks(list, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list), n):
        yield list[i:i + n]

def get_artist_uri(artist_name):
	result = spotify_client.search(q='artist:' + artist_name, type='artist')
	artist = result['artists']['items'][0]
	name = artist['name']
	uri = artist['uri']
	return uri

def add_artist_top_track_to_tracklist(artist_uri):
	response = spotify_client.artist_top_tracks(artist_uri)
	for track in response['tracks'][0:TRACKS_PER_RELATED_ARTIST]:
		track_list.append(track['uri'])
		track_name_list.append(track['name'])

def get_related_artists(artist_uri):
	related = spotify_client.artist_related_artists(artist_uri)

	for related_artist in related['artists']:
		print('  ', related_artist['name'])
		related_artist_uri = related_artist['uri']
		add_artist_top_track_to_tracklist(related_artist_uri)

	#print(track_list)
	#print(track_name_list)

def create_playlist(artist_name):
	playlist_name = artist_name + " - Related Artsits Playlist"
	print("Creating playlist: " + playlist_name)

	new_playlist = spotify_client.user_playlist_create(spotify_username, playlist_name)
	playlist_id = new_playlist['id']
	split_track_list = chunks(track_list, 100)
	for track in split_track_list:
		results = spotify_client.user_playlist_add_tracks(spotify_username, playlist_id, track)
		
def main(args):
	global spotify_client
	
	print("Tracks per artist: " + str(TRACKS_PER_RELATED_ARTIST))
	print("Spotify username: " + spotify_username)

	artist_name = args.artist
	spotify_client = authenticate()
	artist_uri = get_artist_uri(artist_name)

	print("Getting related artists")

	get_related_artists(artist_uri)

	print("Getting track list for: {}".format(artist_name))

	create_playlist(artist_name)

def setArgs(args):
	global spotify_username
	global TRACKS_PER_RELATED_ARTIST

	if args.username:
		spotify_username = args.username
	if (args.tracks_per_artist):
		TRACKS_PER_RELATED_ARTIST = args.tracks_per_artist

parser = argparse.ArgumentParser(description="Create a plylist for top tracks of related artists")
parser.add_argument("artist", type=str, help='Artist name')
parser.add_argument("-u", "--username", type=str, help='Spotify username')
parser.add_argument("-t", "--tracks_per_artist", type=int, help='number of tracks to take from artist. Default is 2')
args = parser.parse_args()

setArgs(args)
main(args)

