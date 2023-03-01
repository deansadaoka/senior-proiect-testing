import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

name = "Geowulf"

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
    artist_id = artist['id']
    print()
    print()

    artist_uri = 'spotify:artist:' + artist_id

    results = spotify.artist_top_tracks(artist_uri)

    for track in results['tracks'][:10]:
        print('track     : ' + track['name'])
        print('audio     : ' + track['preview_url'])
        print('cover art : ' + track['album']['images'][0]['url'])
        print('popularity: ' + str(track['popularity']))
        print()


    print("\n\nRelated Artists: \n")
    related = spotify.artist_related_artists(artist_uri)
    for artist in related['artists'][:10]:
        print('name      : ' + artist['name'])
        print('popularity: ' + str(artist['popularity']))
        print('followers : ' + str(artist['followers']['total']))
        print('genres    : ' + str(artist['genres']))

        print()