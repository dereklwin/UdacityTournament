#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print "Could not connect to {}".format(database_name)

def deleteMatches():
    """Remove all the match records from the database."""

    db, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("SELECT COUNT(player_name) FROM players;")
    count = cursor.fetchone()
    db.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("INSERT INTO players(player_name) VALUES (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

        SELECT Players.PlayerId, Players.PlayerName, NumberOfWinsForPlayer.NumWins, MatchesPlayed.NumMatches
            FROM Players 
                LEFT JOIN NumberOfWinsForPlayer
                    ON Players.PlayerId = NumberOfWinsForPlayer.PlayerId
                LEFT JOIN MatchesPlayed
                    ON Players.PlayerId = MatchesPlayed.PlayerId
            GROUP BY Players.PlayerId;

    """

    db, cursor = connect()
    cursor.execute(
        "SELECT player_id, player_name, num_wins, num_matches FROM player_standings;")
    count = cursor.fetchall()
    db.close()
    return count


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cursor = connect()
    cursor.execute(
        "INSERT INTO matches(player_one, player_two, match_winner) VALUES (%s , %s, %s)", (winner, loser, winner,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

        SELECT Players.PlayerId, Players.PlayerName
            FROM Players LEFT JOIN PlayerStandings
            ON Players.PlayerId = PlayerStandings.PlayerId
            GROUP BY Players.PlayerId;
    """
    db, cursor = connect()
    cursor.execute(
        "SELECT player_id, player_name FROM player_standings;")
    row = cursor.fetchall()
    db.close()

    parings = []
    i = 0

    if len(row)%2 == 0:
        while i < len(row):
            parings.append((row[i][0], row[i][1], row[i + 1][0], row[i + 1][1]))
            i += 2
    else:
        print "Uneven number of players registered"

    return parings