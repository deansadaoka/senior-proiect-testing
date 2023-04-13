import mysql.connector
import os
import time
import requests

API_KEY = "d108b6367729b00677185f71707e6b6c"
USER_AGENT = "niikallen"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ['SQL_PASSWORD'],
    database="test"
)

mycursor = mydb.cursor()


def insert_artist(artist):
    sql = "INSERT INTO artists (spotifyId, name, popularity, followers, link, image) " \
          "VALUES (%s, %s, %s, %s, %s, %s)" \
          "ON DUPLICATE KEY UPDATE popularity=%s, followers=%s"

    val = [
        artist['id'],
        artist['name'],
        artist['popularity'],
        artist['followers']['total'],
        artist['external_urls']['spotify'],
        artist['images'][0]['url'],
        artist['popularity'],
        artist['followers']['total']
    ]

    try:
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print("Artist \"" + artist['name'] + "\" is already in table")


def query_artist(artist_id):
    sql = "SELECT * FROM artists WHERE spotifyId = %s"
    params = (artist_id,)
    mycursor.execute(sql, params)
    results = mycursor.fetchall()
    return results[0]


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


def lookup_tags(track, album, artist):
    response = lastfm_get({
        'method': 'track.getTopTags',
        'artist': artist,
        'track': track
    })

    # if there's an error, just return nothing
    if response.status_code != 200:
        return None

    # extract the top three tags and turn them into a string
    tags = [t['name'] for t in response.json()['toptags']['tag'][:4]]
    if not tags:
        response = lastfm_get({
            'method': 'album.getTopTags',
            'artist': artist,
            'album': album
        })

        if response.status_code != 200:
            return None

        tags = [t['name'] for t in response.json()['toptags']['tag'][:4]]
        if not tags:
            response = lastfm_get({
                'method': 'artist.getTopTags',
                'artist': artist,
            })

            if response.status_code != 200:
                return None

            tags = [t['name'] for t in response.json()['toptags']['tag'][:4]]

    tags_str = ', '.join(tags)

    # rate limiting
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)
    return tags_str


def insert_track(track, genre, image_link):
    sql = "INSERT INTO tracks (spotifyId, name, albumId, artistId, artist, popularity, " \
          "previewLink, duration, genre, tags, imageLink) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" \
          "ON DUPLICATE KEY UPDATE popularity=%s, previewLink=%s, imageLink=%s"

    values = [
        track['id'],
        track['name'],
        track['album']['id'],
        track['artists'][0]['id'],
        track['artists'][0]['name'],
        track['popularity'],
        track['preview_url'],
        track['duration_ms'],
        genre,
        lookup_tags(track['name'], track['album']['name'], track['artists'][0]['name']),
        image_link,
        track['popularity'],
        track['preview_url'],
        image_link
    ]

    mycursor.execute(sql, values)
    mydb.commit()
    print("track inserted")


def insert_album(album):
    sql = "INSERT INTO albums (spotifyId, name, totalTracks, imageLink) " \
          "VALUES (%s, %s, %s, %s)" \
          "ON DUPLICATE KEY UPDATE name=%s, totalTracks=%s, imageLink=%s"

    val = [
        album['id'],
        album['name'],
        album['total_tracks'],
        album['images'][0]['url'],
        album['name'],
        album['total_tracks'],
        album['images'][0]['url'],
    ]

    mycursor.execute(sql, val)
    mydb.commit()


track_ex = {
    'album': {
        'album_group': 'single', 'album_type': 'single', 'artists': [
            {
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/5YGY8feqx7naU7z4HrwZM6'
                },
                'href': 'https://api.spotify.com/v1/artists/5YGY8feqx7naU7z4HrwZM6',
                'id': '5YGY8feqx7naU7z4HrwZM6',
                'name': 'Miley Cyrus',
                'type': 'artist',
                'uri': 'spotify:artist:5YGY8feqx7naU7z4HrwZM6'
            }
        ],
        'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF',
                              'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG',
                              'CH', 'CI', 'CL', 'CM', 'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO',
                              'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH',
                              'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL',
                              'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW',
                              'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD',
                              'ME', 'MG', 'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ',
                              'NA', 'NE', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK',
                              'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI',
                              'SK', 'SL', 'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO',
                              'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS',
                              'XK', 'ZA', 'ZM', 'ZW'],
        'external_urls': {'spotify': 'https://open.spotify.com/album/7I0tjwFtxUwBC1vgyeMAax'},
        'href': 'https://api.spotify.com/v1/albums/7I0tjwFtxUwBC1vgyeMAax',
        'id': '7I0tjwFtxUwBC1vgyeMAax',
        'images': [
            {'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273f429549123dbe8552764ba1d', 'width': 640},
            {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e02f429549123dbe8552764ba1d', 'width': 300},
            {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851f429549123dbe8552764ba1d', 'width': 64}],
        'is_playable': True,
        'name': 'Flowers',
        'release_date': '2023-01-13',
        'release_date_precision': 'day',
        'total_tracks': 1,
        'type': 'album',
        'uri': 'spotify:album:7I0tjwFtxUwBC1vgyeMAax'
    },
    'artists': [
        {
            'external_urls': {
                'spotify': 'https://open.spotify.com/artist/5YGY8feqx7naU7z4HrwZM6'
            },
            'href': 'https://api.spotify.com/v1/artists/5YGY8feqx7naU7z4HrwZM6',
            'id': '5YGY8feqx7naU7z4HrwZM6',
            'name': 'Miley Cyrus',
            'type': 'artist',
            'uri': 'spotify:artist:5YGY8feqx7naU7z4HrwZM6'
        }
    ],
    'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO',
                          'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV',
                          'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT',
                          'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP',
                          'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN',
                          'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI',
                          'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT',
                          'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS',
                          'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'WS', 'SM', 'ST', 'SN',
                          'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI',
                          'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW',
                          'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY',
                          'TJ', 'VE', 'ET', 'XK'],
    'disc_number': 1,
    'duration_ms': 200454,
    'explicit': False,
    'external_ids': {'isrc': 'USSM12209777'},
    'external_urls': {'spotify': 'https://open.spotify.com/track/0yLdNVWF3Srea0uzk55zFn'},
    'href': 'https://api.spotify.com/v1/tracks/0yLdNVWF3Srea0uzk55zFn',
    'id': '0yLdNVWF3Srea0uzk55zFn',
    'is_local': False,
    'name': 'Flowers',
    'popularity': 100,
    'preview_url': 'https://p.scdn.co/mp3-preview/9fbe346e805ed219204f53324f94557ab557b6d3?cid=fa10ca25853a48d7b697e2bcfee74832',
    'track_number': 1,
    'type': 'track',
    'uri': 'spotify:track:0yLdNVWF3Srea0uzk55zFn'
}

album_ex = {
    'album_group': 'single',
    'album_type': 'single',
    'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5YGY8feqx7naU7z4HrwZM6'},
                 'href': 'https://api.spotify.com/v1/artists/5YGY8feqx7naU7z4HrwZM6', 'id': '5YGY8feqx7naU7z4HrwZM6',
                 'name': 'Miley Cyrus', 'type': 'artist', 'uri': 'spotify:artist:5YGY8feqx7naU7z4HrwZM6'}],
    'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF',
                          'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG',
                          'CH', 'CI', 'CL', 'CM', 'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO',
                          'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH',
                          'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL',
                          'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW',
                          'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD',
                          'ME', 'MG', 'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ',
                          'NA', 'NE', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK',
                          'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI',
                          'SK', 'SL', 'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO',
                          'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS',
                          'XK', 'ZA', 'ZM', 'ZW'],
    'copyrights': [{
                       'text': '(P) 2023 Smiley Miley, Inc. under exclusive license to Columbia Records, a Division of Sony Music Entertainment',
                       'type': 'P'}],
    'external_ids': {'upc': '196589803047'},
    'external_urls': {'spotify': 'https://open.spotify.com/album/7I0tjwFtxUwBC1vgyeMAax'},
    'genres': [],
    'href': 'https://api.spotify.com/v1/albums/7I0tjwFtxUwBC1vgyeMAax',
    'id': '7I0tjwFtxUwBC1vgyeMAax',
    'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273f429549123dbe8552764ba1d', 'width': 640},
               {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e02f429549123dbe8552764ba1d', 'width': 300},
               {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851f429549123dbe8552764ba1d', 'width': 64}],
    'is_playable': True,
    'label': 'Columbia',
    'name': 'Flowers',
    'popularity': 94,
    'release_date': '2023-01-13',
    'release_date_precision': 'day',
    'total_tracks': 1,
    'tracks': {
        'href': 'https://api.spotify.com/v1/albums/7I0tjwFtxUwBC1vgyeMAax/tracks?offset=0&limit=50',
        'items': [{'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5YGY8feqx7naU7z4HrwZM6'},
                                'href': 'https://api.spotify.com/v1/artists/5YGY8feqx7naU7z4HrwZM6',
                                'id': '5YGY8feqx7naU7z4HrwZM6', 'name': 'Miley Cyrus', 'type': 'artist',
                                'uri': 'spotify:artist:5YGY8feqx7naU7z4HrwZM6'}],
                   'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ',
                                         'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU',
                                         'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO',
                                         'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR',
                                         'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA',
                                         'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS',
                                         'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR',
                                         'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ',
                                         'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT',
                                         'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW',
                                         'PG', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL',
                                         'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ',
                                         'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ',
                                         'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE',
                                         'ET', 'XK'], 'disc_number': 1, 'duration_ms': 200454, 'explicit': False,
                   'external_urls': {'spotify': 'https://open.spotify.com/track/0yLdNVWF3Srea0uzk55zFn'},
                   'href': 'https://api.spotify.com/v1/tracks/0yLdNVWF3Srea0uzk55zFn', 'id': '0yLdNVWF3Srea0uzk55zFn',
                   'is_local': False, 'name': 'Flowers',
                   'preview_url': 'https://p.scdn.co/mp3-preview/9fbe346e805ed219204f53324f94557ab557b6d3?cid=fa10ca25853a48d7b697e2bcfee74832',
                   'track_number': 1, 'type': 'track', 'uri': 'spotify:track:0yLdNVWF3Srea0uzk55zFn'}], 'limit': 50,
        'next': None, 'offset': 0, 'previous': None, 'total': 1}, 'type': 'album',
    'uri': 'spotify:album:7I0tjwFtxUwBC1vgyeMAax'}
