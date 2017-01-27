-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Table that keeps track of players in tournament using unique id
CREATE TABLE tournament ( id SERIAL primary key,
                          playername TEXT);

-- Table to keep track of players matches and wins using their unique id
CREATE TABLE matches ( id SERIAL references tournament,
                          matches INTEGER,
                          wins INTEGER);
