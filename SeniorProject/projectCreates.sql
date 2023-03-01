# DROP TABLE artists;
#
# CREATE TABLE artists (
#     spotifyId VARCHAR(50) NOT NULL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     popularity INT NOT NULL,
#     followers INT NOT NULL,
#     link VARCHAR(200) NOT NULL,
#     image VARCHAR(200) NOT NULL
# );
#
#
# CREATE TABLE albums (
#     spotifyId VARCHAR(50) NOT NULL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     totalTracks INT NOT NULL,
#
# );

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'adminpass';
flush privileges;


SELECT * FROM artists;