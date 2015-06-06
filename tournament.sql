-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players( name text,
                      id serial PRIMARY KEY );

CREATE TABLE matches( winner integer REFERENCES players,
                      loser integer REFERENCES players,
                      id serial PRIMARY KEY );

-- Returns all players's IDs and their number of wins, ordered from most wins to least
CREATE VIEW num_wins AS
    SELECT players.id, count(matches.winner) AS num
    FROM players LEFT JOIN matches
                           ON players.id = winner
    GROUP BY players.id
    ORDER BY num DESC;

-- Returns all players's IDs and their number of losses, ordered from most losses to least
CREATE VIEW num_losses AS
    SELECT players.id, count(matches.loser) AS num
    FROM players LEFT JOIN matches
                           ON players.id = loser
    GROUP BY players.id
    ORDER BY num DESC;

-- Returns all players's IDs and their number of matches, ordered from most matches to least
CREATE VIEW num_matches AS
	SELECT players.id, (num_wins.num + num_losses.num) AS num
	FROM players LEFT JOIN num_wins
	                       ON players.id = num_wins.id
	             LEFT JOIN num_losses
	                       ON players.id = num_losses.id
	ORDER BY num DESC;
