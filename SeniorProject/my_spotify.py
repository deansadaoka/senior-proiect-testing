import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def search_artist(name: str):
    """Searches Spotify for artist and returns artist info if found.
    Otherwise, returns None"""
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    return items[0] if len(items) > 0 else None


def search_track_artist(track_name, artist_name):
    """Searches Spotify for a track with the name and artist"""
    results = spotify.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    tracks = results['tracks']['items']

    if tracks:
        return tracks[0]  # return the first track in the list

    return None


def get_artist(artist_id: str):
    results = spotify.artist(artist_id=artist_id)
    return results


def get_album(album_id: str):
    results = spotify.album(album_id)
    return results


def get_top_songs(artist_id: str):
    results = spotify.artist_top_tracks(artist_id=artist_id)
    return results


def get_related_artists(artist_id: str):
    results = spotify.artist_related_artists(artist_id=artist_id)
    return results


def search_track(track_name: str):
    results = spotify.search(q='track:' + track_name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def get_track(track_id: str):
    results = spotify.track(track_id=track_id)
    return results


def get_several_tracks(track_ids):
    results = spotify.tracks(tracks=track_ids)
    return results

# def get_artist(artist_id: str):
#     name = "Geowulf"
#
#     results = spotify.search(q='artist:' + name, type='artist')
#     items = results['artists']['items']
#     if len(items) > 0:
#         artist = items[0]
#         print(artist['name'])
#         print("Photo     : " + artist['images'][0]['url'])
#         print("Followers : " + str(artist['followers']['total']))
#         print("Popularity: " + str(artist['popularity']))
#         print("Genres    : ", end="")
#         for g in artist['genres']:
#             print(g, end=", ")
#         artist_id = artist['id']
#         print()
#         print()
#
#         artist_uri = 'spotify:artist:' + artist_id
#
#         results = spotify.artist_top_tracks(artist_uri)
#
#         for track in results['tracks'][:10]:
#             print('track     : ' + track['name'])
#             print('audio     : ' + track['preview_url'])
#             print('cover art : ' + track['album']['images'][0]['url'])
#             print('popularity: ' + str(track['popularity']))
#             print()
#
#         print("\n\nRelated Artists: \n")
#         related = spotify.artist_related_artists(artist_uri)
#         for artist in related['artists'][:10]:
#             print('name      : ' + artist['name'])
#             print('popularity: ' + str(artist['popularity']))
#             print('followers : ' + str(artist['followers']['total']))
#             print('genres    : ' + str(artist['genres']))
#
#             print()
