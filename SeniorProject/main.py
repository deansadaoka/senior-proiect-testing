import csv
import random
import re

import requests

import my_spotify
import database

top_tags = ['rock', 'electronic', 'seen live', 'alternative', 'indie', 'pop', 'female vocalists', 'metal', 'alternative rock', 'jazz', 'classic rock', 'ambient', 'experimental', 'folk', 'indie rock', 'punk', 'Hip-Hop', 'hard rock', 'black metal', 'instrumental', 'singer-songwriter', 'dance', '80s', 'Progressive rock', 'death metal', 'heavy metal', 'hardcore', 'british', 'soul', 'chillout', 'electronica', 'rap', 'industrial', 'Classical', 'Soundtrack', 'punk rock', 'blues', 'thrash metal', '90s', 'metalcore', 'acoustic', 'psychedelic', 'japanese', 'hip hop', 'post-rock', 'Progressive metal', 'german', 'House', 'funk', 'new wave', 'trance', 'techno', 'piano', 'american', 'post-punk', 'reggae', '70s', 'indie pop', 'electro', 'trip-hop', 'rnb', '60s', 'country', 'Power metal', 'Melodic Death Metal', 'downtempo', 'emo', 'male vocalists', 'post-hardcore', 'doom metal', 'Psychedelic Rock', 'oldies', 'Love', 'synthpop', 'beautiful', '00s', 'french', 'russian', 'Gothic Metal', 'Grunge', 'idm', 'Gothic', 'noise', 'dark ambient', 'guitar', 'cover', 'britpop', 'favorites', 'screamo', 'swedish', 'Mellow', 'lounge', 'pop rock', 'albums I own', 'grindcore', 'under 2000 listeners', 'j-pop', 'Nu Metal', 'female vocalist', 'symphonic metal', 'polish', 'blues rock', 'chill', 'Drum and bass', 'Avant-Garde', 'new age', 'ska', 'shoegaze', 'fip', 'Progressive', 'minimal', 'Awesome', 'darkwave', 'pop punk', 'dubstep', 'ebm', 'Canadian', 'world', 'folk metal', 'deathcore', 'easy listening', 'J-rock', 'alternative metal', 'finnish', 'Brutal Death Metal', 'industrial metal', 'hardcore punk', 'Gothic Rock', 'Lo-Fi', 'Disco', 'latin', 'USA', 'dub', 'atmospheric', 'folk rock', 'drone', 'Stoner Rock', 'All', 'sexy', 'christian', 'deutsch', 'female', 'electropop', 'celtic', 'jazz fusion', 'christmas', 'Sludge', 'Garage Rock', 'contemporary classical', 'dream pop', 'anime', 'italian', 'Smooth Jazz', 'psytrance', 'melancholic', 'epic', 'brazilian', 'cool', 'spanish', 'romantic', 'melancholy', 'comedy', 'sad', 'male vocalist', 'Ballad', 'ethereal', 'Favorite', 'Fusion', 'UK', 'JPop', 'Technical Death Metal', 'soft rock', 'k-pop', 'Korean', 'art rock', 'classic', 'video game music', 'australian', 'underground hip-hop', 'Female fronted metal', 'swing', 'acid jazz', 'neofolk', 'irish', 'party', 'dark', 'speed metal', 'baroque', 'visual kei', 'live', 'norwegian', 'neoclassical', 'viking metal', 'rock n roll', 'Alt-country', 'remix', 'rockabilly', 'Favourites', 'amazing', 'glam rock']

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


def get_track_tags(artist_name, track_name):
    base_url = "http://ws.audioscrobbler.com/2.0/"
    api_key = "a7bfdeea33862f1ae4696306d97a369a"

    params = {
        "method": "track.gettoptags",
        "artist": artist_name,
        "track": track_name,
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    tags = []
    if 'toptags' in data and 'tag' in data['toptags']:
        for tag in data['toptags']['tag']:
            # Check if tag matches the undesired pattern
            if not re.match(r'^-\d+$', tag['name']):
                tags.append(tag['name'])

    return tags


def add_track_to_database(track_name, artist_name, tag, genre):
    # Get track, artist, and album from spotify
    track = my_spotify.search_track_artist(track_name, artist_name)

    album = track['album']

    albumId = album['id']


    artistId = track['artists'][0]['id']

    duration = track['duration_ms']
    spotifyId = track['id']
    name = track['name']
    popularity = track['popularity']
    previewLink = track['preview_url']

    if len(album['images']) > 0:
        imageLink = album['images'][0]['url']
    else:
        imageLink = ""

    # Insert Artist, Album, and Track
    artist = my_spotify.get_artist(artistId)
    database.insert_artist(artist)

    if not database.album_exists(albumId):
        database.insert_album(album)

    database.insert_track(track, genre, imageLink)

    # Get tags, filter out bad ones, insert
    all_tags = get_track_tags(track['artists'][0]['name'], track['name'])
    tags_to_insert = []
    for t in all_tags:
        if t in top_tags:
            tags_to_insert.append(t)

    tags_to_insert.append(tag)
    for ti in tags_to_insert:
        database.insert_tag_and_relation(track['id'], ti)




def main():
    # add_track_to_database("Smells Like Teen Spirit")
    # return

    f = open('top_tags_and_tracks.csv')
    csv_reader = csv.reader(f)

    csv_data = read_csv_file("top_tags_and_tracks.csv")
    i = 0
    for row in csv_data:
        track_name = row['Song Name']
        artist_name = row['Artist Name']
        genre = row['Genre']
        tag = row['Tag Name']

        # print(track_name)
        # print(artist_name)
        # print(tag)
        # print(genre)

        # if i > 1303 and not database.track_exists(track_name, artist_name):
        #     add_track_to_database(track_name, artist_name, genre, tag)
        #     print(track_name + " inserted!, " + str(i))


        try:
            if i > 4793 and not database.track_exists(track_name, artist_name):
                add_track_to_database(track_name, artist_name, genre, tag)
                print(track_name + " inserted!, " + str(i))
            #add_track_to_database(track_name, artist_name, genre, tag)
        except Exception as e:
            print(e)
            print(track_name)
            print(i)

        i += 1

    return

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