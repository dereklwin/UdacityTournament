-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop all other existing connections
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();

-- drop any duplicate database prior to the database creation
DROP DATABASE IF EXISTS tournament;
-- create database
CREATE DATABASE tournament;
-- connect to the database
\c tournament

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

DROP VIEW IF EXISTS matches_played;
DROP VIEW IF EXISTS number_of_wins;
DROP VIEW IF EXISTS player_standings;

CREATE TABLE players (
	player_id SERIAL PRIMARY KEY, 
	player_name TEXT NOT NULL
);

CREATE TABLE matches (
	player_one INTEGER REFERENCES players(player_id), 
	player_two INTEGER REFERENCES players(player_id), 
	match_winner INTEGER REFERENCES players(player_id),
	CHECK (match_winner = player_one OR match_winner = player_two)
);

CREATE VIEW matches_played AS
	SELECT players.player_id, players.player_name, COUNT(matches.match_winner) AS num_matches
	FROM players LEFT JOIN matches
	ON players.player_id = matches.player_one OR players.player_id = matches.player_two
	GROUP BY players.player_id;

CREATE VIEW number_of_wins AS
	SELECT players.player_id, players.player_name, COUNT(matches.match_winner) AS num_wins
	FROM players LEFT JOIN matches
	ON players.player_id = matches.match_winner
	GROUP BY players.player_id
	ORDER BY players.player_id;

CREATE VIEW player_standings AS
	SELECT matches_played.player_id, matches_played.player_name, number_of_wins.num_wins, matches_played.num_matches
	FROM number_of_wins LEFT JOIN matches_played
	ON number_of_wins.player_id = matches_played.player_id   
	ORDER BY num_wins DESC;
