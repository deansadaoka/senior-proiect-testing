import mysql.connector
import random

# Establish connection
cnx = mysql.connector.connect(
    user='nickdeanmatt',
    password='adminpass',
    host='ambari-node5.csc.calpoly.edu',
    database='nickdeanmatt'
)

# Create a cursor object
cursor = cnx.cursor()

# Create 20 common music tags
tags = ['Rap', 'Rock', '70s', 'Pop', 'EDM', 'Jazz', 'Blues', 'Country',
        'Classical', 'Reggae', 'Dance', 'R&B', 'Soul', 'Gospel', 'Punk',
        'Metal', 'Folk', 'Latin', 'New Age', 'World Music']

# Insert tags into tags table
for tag in tags:
    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))

# Fetch all tracks
cursor.execute("SELECT spotifyId FROM tracks")
tracks = cursor.fetchall()

# Fetch all tags
cursor.execute("SELECT tagId FROM tags")
tag_ids = cursor.fetchall()

# Assign each track a random tag
for track in tracks:
    random_tag_id = random.choice(tag_ids)[0]
    cursor.execute("INSERT INTO track_tags (spotifyId, tagId) VALUES (%s, %s)", (track[0], random_tag_id))

# Commit changes and close connection
cnx.commit()
cursor.close()
cnx.close()