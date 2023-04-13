# DROP TABLE artists;
DROP TABLE tracks;
DROP TABLE albums;
#
CREATE TABLE artists (
    spotifyId VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    popularity INT NOT NULL,
    followers INT NOT NULL,
    link VARCHAR(200) NOT NULL,
    image VARCHAR(200) NOT NULL
);
#
#
CREATE TABLE albums (
    spotifyId VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    totalTracks INT NOT NULL,
    imageLink VARCHAR(100) NOT NULL
);

CREATE TABLE tracks
(
    spotifyId  VARCHAR(50)  NOT NULL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    albumId    VARCHAR(50)  NOT NULL,
    artistId   VARCHAR(50)  NOT NULL,
    artist     VARCHAR(100) NOT NULL,
    popularity INT          NOT NULL,
    previewLink       VARCHAR(200),
    duration   INT          NOT NULL,
    genre      VARCHAR(50)  NOT NULL,
    tags       VARCHAR(200) NOT NULL,
    imageLink VARCHAR(100) NOT NULL,
    FOREIGN KEY (albumId) REFERENCES albums (spotifyId) ON DELETE CASCADE,
    FOREIGN KEY (artistId) REFERENCES artists (spotifyId) ON DELETE CASCADE
);

# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'adminpass';
# flush privileges;


SELECT * FROM artists;
SELECT * FROM albums;
SELECT * FROM tracks;

SELECT DISTINCT genre FROM tracks;


create database test;
