import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

name = "Drake"

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'])
    print("Photo     : " + artist['images'][0]['url'])
    print("Followers : " + str(artist['followers']['total']))
    print("Popularity: " + str(artist['popularity']))
    print("Genres    : ", end="")
    for g in artist['genres']:
        print(g, end=", ")
    print()