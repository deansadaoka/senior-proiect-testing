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

CREATE TABLE users (
    userId INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    PRIMARY KEY (userId)
);

CREATE TABLE friends (
    friend_id INT NOT NULL AUTO_INCREMENT,
    user1Id INT NOT NULL,
    user2Id INT NOT NULL,
    PRIMARY KEY (friend_id),
    FOREIGN KEY (user1Id) REFERENCES Users(userId),
    FOREIGN KEY (user2Id) REFERENCES Users(userId)
);

CREATE TABLE playlists (
    playlistId INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    authorId INT NOT NULL,
    description VARCHAR(200),
    songs VARCHAR(500),
    PRIMARY KEY (playlistId),
    FOREIGN KEY (authorId) REFERENCES Users(userId)
);

# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'adminpass';
# flush privileges;


SELECT * FROM artists;
SELECT * FROM albums;
SELECT * FROM tracks;

SELECT DISTINCT genre FROM tracks;


INSERT INTO users (username, password)
VALUES ('Matt', '123'),
       ('Dean', '123'),
       ('Nick', '123'),
       ('Lubinov', '123');

SELECT * FROM users;


INSERT INTO Friends (user1Id, user2Id)
VALUES (1, 2), -- Dean and Matt
       (1, 3), -- Dean and Nick
       (3, 4), -- Nick and Lubinov
       (2, 3), -- Matt and Nick
       (2, 4), -- Matt and Lubinov
       (1, 4); -- Dean and Lubinov

SELECT * FROM friends;




