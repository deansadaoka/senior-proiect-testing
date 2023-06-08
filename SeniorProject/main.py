import csv
import random

import my_spotify
import database


def add_track_to_database(track_name):
    track = my_spotify.search_track(track_name)
    album = track['album']
    artist = track['artists'][0]

    albumId = album['id']
    albumName = album['name']
    albumTotalTracks = album['total_tracks']
    albumLink = album['external_urls']['spotify']

    artistId = artist['id']
    artistName = artist['name']

    duration = track['duration_ms']
    spotifyId = track['id']
    name = track['name']
    popularity = track['popularity']
    previewLink = track['preview_url']

    if len(album['images']) > 0:
        imageLink = album['images'][0]['url']
    else:
        imageLink = ""

    genre = "OTHER"



def main():
    add_track_to_database("Smells Like Teen Spirit")
    return

    f = open('top_songs.csv')
    csv_reader = csv.reader(f)
    # line_num = 0
    # for row in csv_reader:
    #     if line_num != 0:
    #         artist_name = row[2]
    #         artist = my_spotify.search_artist(artist_name)
    #         if artist is not None:
    #             database.insert_artist(artist)
    #     line_num += 1

    # artist = my_spotify.search_artist("Kanye West")
    # related = my_spotify.get_related_artists(artist['id'])
    # for r in related['artists']:
    #     print(r['name'])
    #     print(r['popularity'])
    #     print(r['genres'])
    #     print()
    # print(related)
    # exit(0)

    song_ids = []
    song_names = []
    first = True
    for row in csv_reader:
        if not first:
            uri = row[1]
            song_ids.append(uri.split("track:")[1])
            song_names.append(row[3])
        else:
            first = False

    tracks = []

    genres = ['Pop', 'Country', 'Rock', 'EDM']

    for i in range(0, len(song_ids), 50):
        print(i)
        results = my_spotify.get_several_tracks(song_ids[i:i+50])
        for t in results['tracks']:
            tracks.append(t)

    for t in tracks:
        if t is not None:
            print(t['name'])
            album = my_spotify.get_album(t['album']['id'])
            artist = my_spotify.get_artist(t['artists'][0]['id'])

            i = random.randint(0, len(genres)-1)
            genre = genres[i]

            database.insert_artist(artist)
            database.insert_album(album)
            database.insert_track(t, genre, album['images'][0]['url'])


if __name__ == '__main__':
    main()



# {
#     'album': {
#         'album_type': 'album',
#         'artists': [
#             {
#                 'external_urls': {
#                     'spotify': 'https://open.spotify.com/artist/6olE6TJLqED3rqDCT0FyPh'
#                 },
#                 'href': 'https://api.spotify.com/v1/artists/6olE6TJLqED3rqDCT0FyPh',
#                 'id': '6olE6TJLqED3rqDCT0FyPh',
#                 'name': 'Nirvana',
#                 'type': 'artist',
#                 'uri': 'spotify:artist:6olE6TJLqED3rqDCT0FyPh'
#             }
#         ],
#         'available_markets': [
#             'CA', 'MX', 'US'
#         ],
#         'external_urls': {
#             'spotify': 'https://open.spotify.com/album/2guirTSEqLizK7j9i1MTTZ'
#         },
#         'href': 'https://api.spotify.com/v1/albums/2guirTSEqLizK7j9i1MTTZ',
#         'id': '2guirTSEqLizK7j9i1MTTZ',
#         'images': [
#             {
#                 'height': 640,
#                 'url': 'https://i.scdn.co/image/ab67616d0000b273e175a19e530c898d167d39bf',
#                 'width': 640
#             },
#             {
#                 'height': 300,
#                 'url': 'https://i.scdn.co/image/ab67616d00001e02e175a19e530c898d167d39bf',
#                 'width': 300
#             },
#             {
#                 'height': 64,
#                 'url': 'https://i.scdn.co/image/ab67616d00004851e175a19e530c898d167d39bf',
#                 'width': 64
#             }
#         ],
#         'name': 'Nevermind (Remastered)',
#         'release_date': '1991-09-26',
#         'release_date_precision': 'day',
#         'total_tracks': 13,
#         'type': 'album',
#         'uri': 'spotify:album:2guirTSEqLizK7j9i1MTTZ'
#     },
#     'artists': [
#         {
#             'external_urls': {
#                 'spotify': 'https://open.spotify.com/artist/6olE6TJLqED3rqDCT0FyPh'
#             },
#             'href': 'https://api.spotify.com/v1/artists/6olE6TJLqED3rqDCT0FyPh',
#             'id': '6olE6TJLqED3rqDCT0FyPh',
#             'name': 'Nirvana',
#             'type': 'artist',
#             'uri': 'spotify:artist:6olE6TJLqED3rqDCT0FyPh'
#         }
#     ],
#     'available_markets': [
#         'CA', 'MX', 'US'
#     ],
#     'disc_number': 1,
#     'duration_ms': 301920,
#     'explicit': False,
#     'external_ids': {
#         'isrc': 'USGF19942501'
#     },
#     'external_urls': {
#         'spotify': 'https://open.spotify.com/track/5ghIJDpPoe3CfHMGu71E6T'
#     },
#     'href': 'https://api.spotify.com/v1/tracks/5ghIJDpPoe3CfHMGu71E6T',
#     'id': '5ghIJDpPoe3CfHMGu71E6T',
#     'is_local': False,
#     'name': 'Smells Like Teen Spirit',
#     'popularity': 80,
#     'preview_url': 'https://p.scdn.co/mp3-preview/91219ebc0d0505a1001c4b854f8b2451fcec95b8?cid=fa10ca25853a48d7b697e2bcfee74832',
#     'track_number': 1,
#     'type': 'track',
#     'uri': 'spotify:track:5ghIJDpPoe3CfHMGu71E6T'
# }