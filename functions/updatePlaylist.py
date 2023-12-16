from concurrent.futures import ThreadPoolExecutor
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET", "")
REDIRECT_URL = os.environ.get("REDIRECT_URL", "")
SPOTIFY_TOKEN = os.environ.get("SPOTIFY_TOKEN", "")

file = open('token.txt', 'w')
file.write('SPOTIFY_TOKEN')
file.close()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=["playlist-modify-public", "playlist-modify-private"],
        redirect_uri=REDIRECT_URL,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)


def addTracks(playlist_id, tracks):
    tracksURI = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(searchTrack, tracks))
        for r in results:
            if r != None:
                tracksURI.append(r)
    sp.playlist_add_items(playlist_id=playlist_id, items=tracksURI)
    return tracksURI


def deteleAllPlaylistTracks(playlist_id):
    tracksURI = []
    for track in sp.playlist_items(playlist_id=playlist_id)['items']:
        tracksURI.append(track["track"]["uri"])
    sp.playlist_remove_all_occurrences_of_items(
        playlist_id=playlist_id, items=tracksURI)


def getGenres():
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, './genres.json')

    with open(json_file_path, 'r') as file:
        genres = json.load(file)
        return genres


def searchTrack(track):
    t = sp.search(f"isrc:{track['isrc']}")['tracks']
    if t['total'] > 0:
        return t["items"][0]["uri"]
    return None


def updatePlaylistHandler(event, context):
    genres = getGenres()
    playlist_id = genres[event['name']]['playlistUri']
    deteleAllPlaylistTracks(playlist_id)
    tracksURI = addTracks(playlist_id, event['data'])
    return tracksURI
