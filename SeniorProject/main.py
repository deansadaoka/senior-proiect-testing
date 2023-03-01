import my_spotify
import database

import csv


def main():
    f = open('top_songs.csv')
    csv_reader = csv.reader(f)
    line_num = 0
    for row in csv_reader:
        if line_num != 0:
            artist_name = row[2]
            artist = my_spotify.search_artist(artist_name)
            if artist is not None:
                database.insert_artist(artist)
        line_num += 1



if __name__ == '__main__':
    main()

