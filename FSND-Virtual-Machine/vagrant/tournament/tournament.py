#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()

    # Deletes all rows from matches table
    c.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()

    # Deletes all rows in tournament table
    c.execute("DELETE FROM tournament;")

    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()

    # Gets number of players in tournament
    c.execute("""SELECT COUNT(*)
                 FROM tournament;""")
    data = c.fetchall()
    playercount = data[0][0]

    DB.close()
    return playercount


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()

    # Cleans name to protect from sql injection and puts it into the table
    name = str(bleach.clean(name))
    c.execute("""INSERT INTO tournament (playername)
                 VALUES (%s);""", (name,))

    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()

    # Finds returns all players with their sats
    c.execute("""SELECT tournament.id, playername, wins, matches
                 FROM tournament left join matches
                 ON tournament.id = matches.id
                 ORDER BY wins;""")

    # Appends to list to return
    standings = []
    for row in c.fetchall():
        # Checks to see if matches and wins are none.
        # If they are then use a zero
        if row[2] is not None and row[3] is not None:
            standings.append((row[0], str(row[1]), row[2], row[3]))
        else:
            standings.append((row[0], str(row[1]), 0, 0))

    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()

    # Used to update match for winner
    # First finds the winner
    c.execute("""SELECT matches,wins
                 FROM matches
                 WHERE id=(%s);""", (winner,))
    info = c.fetchall()
    # Updates if the winner already has a row in matches
    if info:
        c.execute("""UPDATE matches
                     SET matches=(%s), wins=(%s)
                     WHERE id=(%s);""", (info[0][0], info[0][1], winner,))
    # Inserts new row if winner doen't already have a row in matches
    else:
        c.execute("""INSERT INTO matches (id, matches, wins)
                     VALUES ((%s), 1, 1);""", (winner,))

    # Updates users mataches
    c.execute("""SELECT matches,wins
                 FROM matches
                 WHERE id=(%s);""", (loser,))
    info = c.fetchall()
    # Updates if the loser already has a row in matches
    if info:
        c.execute("""UPDATE matches
                     SET matches=(%s), wins=(%s)
                     WHERE id=(%s);""", (info[0][0], info[0][1], loser,))
    # Inserts new row if loser doen't already have a row in matches
    else:
        c.execute("""INSERT INTO matches (id, matches, wins)
                     VALUES ((%s), 1, 0);""", (loser,))

    DB.commit()
    DB.close()


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
    """

    DB = connect()
    c = DB.cursor()

    # Gets all of the players' id and names and orders using their wins
    c.execute("""SELECT tournament.id, playername
                 FROM tournament left join matches
                 ON tournament.id = matches.id
                 ORDER BY wins;""")

    # List that will have all the pairings to return
    pairings = []
    # Pairs all players by two because they were sorted by wins
    stats = c.fetchall()
    for i in range(0, len(stats), 2):
        pairings.append((stats[0][0], stats[0][1], stats[1][0], stats[1][1]))

    DB.close()
    return pairings
