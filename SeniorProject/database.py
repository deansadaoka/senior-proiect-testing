import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ['SQL_PASSWORD'],
    database="mydatabase"
)

mycursor = mydb.cursor()


def insert_artist(artist):
    sql = "INSERT INTO artists (spotifyId, name, popularity, followers, link, image) " \
          "VALUES (%s, %s, %s, %s, %s, %s)"

    val = [
        artist['id'],
        artist['name'],
        artist['popularity'],
        artist['followers']['total'],
        artist['external_urls']['spotify'],
        artist['images'][0]['url']
    ]

    try:
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print("Artist \"" + artist['name'] + "\" is already in table")
