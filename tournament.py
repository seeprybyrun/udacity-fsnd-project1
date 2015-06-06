#!/usr/bin/env python

import psycopg2


def registerPlayer(playerName):
    _queryAndCommitToDatabase("INSERT INTO players VALUES ((%s));",
                              playerName)


def reportMatch(winnerIdNumber, loserIdNumber):
    _queryAndCommitToDatabase("INSERT INTO matches VALUES ((%s),(%s));",
                              winnerIdNumber, loserIdNumber)


def countPlayers():
    numberOfPlayers = _queryDatabase("SELECT count(*) FROM players;")
    return int(numberOfPlayers[0][0]) # need to cast to an int because the
                                      # query returns a string


def deleteMatches():
    _queryAndCommitToDatabase("DELETE FROM matches;")


def deletePlayers():
    _queryAndCommitToDatabase("DELETE FROM players;")


def playerStandings():
    query = """SELECT players.id, name, num_wins.num AS wins,
                      num_matches.num AS matches
               FROM players, num_wins, num_matches
               WHERE players.id = num_wins.id
                 AND players.id = num_matches.id
               ORDER BY wins DESC;
            """

    queryResults = _queryDatabase(query)

    # need to cast to ints because query fields are always returned as strings;
    standings = [ {'ID_NUMBER': int(player[0]),
                   'NAME': player[1],
                   'NUMBER_OF_WINS': int(player[2]),
                   'NUMBER_OF_MATCHES': int(player[3]) }
                  for player in queryResults ]

    return [ (player['ID_NUMBER'],
              player['NAME'],
              player['NUMBER_OF_WINS'],
              player['NUMBER_OF_MATCHES'] )
             for player in standings ]


def swissPairings():
    standings = [ {'ID_NUMBER': player[0],
                   'NAME': player[1] }
                  for player in playerStandings() ]

    pairedPlayers = _pairConsecutiveElements(standings)

    return [ (firstPlayer['ID_NUMBER'],
              firstPlayer['NAME'],
              secondPlayer['ID_NUMBER'],
              secondPlayer['NAME'] )
             for firstPlayer,secondPlayer in pairedPlayers ]


def _connectToDatabase():
    return psycopg2.connect("dbname=tournament")


def _queryDatabase(query):
    databaseConnection = _connectToDatabase()
    cursor = databaseConnection.cursor()
    cursor.execute(query)
    queryResult = cursor.fetchall()
    databaseConnection.close()
    return queryResult


def _queryAndCommitToDatabase(query, *argumentsForQuery):
    databaseConnection = _connectToDatabase()
    cursor = databaseConnection.cursor()
    cursor.execute(query, argumentsForQuery)
    databaseConnection.commit()
    databaseConnection.close()


def _pairConsecutiveElements(iterable):
    return zip(iterable[::2],iterable[1::2])
