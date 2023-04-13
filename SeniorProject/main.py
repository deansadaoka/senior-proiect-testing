import csv
import random

import my_spotify
import database


def main():
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

