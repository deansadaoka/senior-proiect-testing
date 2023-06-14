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
    tags       VARCHAR(200) NOT NULL, #DEPRECATED
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
    friendId INT NOT NULL AUTO_INCREMENT,
    user1Id INT NOT NULL,
    user2Id INT NOT NULL,
    PRIMARY KEY (friendId),
    FOREIGN KEY (user1Id) REFERENCES users(userId),
    FOREIGN KEY (user2Id) REFERENCES users(userId)
);

CREATE TABLE friend_requests (
    requestId INT NOT NULL AUTO_INCREMENT,
    requesterId INT NOT NULL,
    recipientId INT NOT NULL,
    PRIMARY KEY (requestId),
    FOREIGN KEY (requesterId) REFERENCES users(userId),
    FOREIGN KEY (recipientId) REFERENCES users(userId),
    UNIQUE KEY (requesterId, recipientId)
);

CREATE TABLE playlists (
    playlistId INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    authorId INT NOT NULL,
    description VARCHAR(200),
    PRIMARY KEY (playlistId),
    FOREIGN KEY (authorId) REFERENCES users(userId)
);

CREATE TABLE playlist_tracks (
    playlistId INT NOT NULL,
    spotifyId VARCHAR(50) NOT NULL,
    rating INT NOT NULL,
    PRIMARY KEY (playlistId, spotifyId),
    FOREIGN KEY (playlistId) REFERENCES playlists(playlistId) ON DELETE CASCADE,
    FOREIGN KEY (spotifyId) REFERENCES tracks(spotifyId) ON DELETE CASCADE
);

CREATE TABLE tags (
    tagId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE track_tags (
    spotifyId VARCHAR(50),
    tagId INT,
    PRIMARY KEY (spotifyId, tagId),
    FOREIGN KEY (spotifyId) REFERENCES tracks(spotifyId) ON DELETE CASCADE,
    FOREIGN KEY (tagId) REFERENCES tags(tagId) ON DELETE CASCADE
);


INSERT INTO users (username, password)
VALUES ('Matt', '123'),
       ('Dean', '123'),
       ('Nick', '123'),
       ('Lubinov', '123');

SELECT * FROM users;


INSERT INTO friends (user1Id, user2Id)
VALUES (1, 2), -- Dean and Matt
       (1, 3), -- Dean and Nick
       (3, 4), -- Nick and Lubinov
       (2, 3), -- Matt and Nick
       (2, 4), -- Matt and Lubinov
       (1, 4); -- Dean and Lubinov

SELECT * FROM friends;


INSERT INTO users (username, password)
VALUES ('Kevin', '123'),
       ('Bob', '123');

INSERT INTO friend_requests (requesterId, recipientId)
SELECT u1.userId, u2.userId
FROM users u1, users u2
WHERE (u1.username = 'Bob' AND u2.username = 'Dean')
    OR (u1.username = 'Kevin' AND u2.username = 'Dean');

SELECT * FROM friend_requests;

SELECT * FROM playlists;

SELECT * FROM tags;
SELECT * FROM track_tags;
SELECT * FROM tracks;
SELECT * FROM artists;

SELECT * FROM tracks WHERE artist = 'Nirvana';
SELECT * FROM albums WHERE name = 'Nevermind (Remastered)';
SELECT * FROM artists WHERE name = 'Nirvana';
