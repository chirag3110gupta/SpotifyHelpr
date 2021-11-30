"""Defines all the functions related to the database"""
from app import db
from sqlalchemy.sql import text

def fetch_songs() -> dict:
  """Reads all tasks listed in the songs table

  Returns:
      A list of dictionaries
  """

  conn = db.connect()
  query_results = conn.execute("Select * from Songs;").fetchall()
  conn.close()
  song_list = []
  for result in query_results:
    item = {
      "songId": result[0],
      "name": result[1],
      "artist": result[2],
      "genre": result[3],
      "url": result[4],
      "likenessFactor": result[5]
    }
    song_list.append(item)

  return song_list


def fetch_playlists() -> dict:
  """Reads all tasks listed in the playlists table

  Returns:
      A list of dictionaries
  """

  conn = db.connect()
  query_results = conn.execute("Select * from Playlists;").fetchall()
  conn.close()
  playlist_list = []
  for result in query_results:
    item = {
      "playlistId": result[0],
      "playlistNamename": result[1],
      "userId": result[2]
    }
    playlist_list.append(item)

  return playlist_list


def fetch_songsFoundIn() -> dict:
  """Reads all tasks listed in the songsFoundIn table

  Returns:
      A list of dictionaries
  """

  conn = db.connect()
  query_results = conn.execute("Select * from SongsFoundIn;").fetchall()
  conn.close()
  songsFoundIn_list = []
  for result in query_results:
    item = {
      "songId": result[0],
      "playlistId": result[1]
    }
    songsFoundIn_list.append(item)

  return songsFoundIn_list


def fetch_playlistsForUser(userId: int) -> dict:
  """Reads all playlists for a specific user

  Returns:
      A list of dictionaries
  """

  conn = db.connect()
  query_results = conn.execute(f"SELECT * FROM Playlists WHERE userId={userId};").fetchall()
  results_list = []

  for result in query_results:
    song_count = conn.execute(f"SELECT COUNT(songId) FROM SongsFoundIn WHERE playlistId={result[0]}").fetchall()
    item = {
      "playlistId": result[0],
      "playlistName": result[1],
      "userId": result[2],
      "songCount": song_count
    }
    results_list.append(item)

  conn.close()

  return results_list


def fetch_songsForPlaylist(playlistId: int) -> dict:
  """Reads all songs for a specific playlist

  Returns:
      A list of dictionaries
  """

  conn = db.connect()
  query_results = conn.execute(f"SELECT * FROM Songs WHERE songId IN (SELECT songId FROM SongsFoundIn WHERE playlistId = {playlistId})").fetchall()
  conn.close()
  results_list = []
  for result in query_results:
    item = {
      "songId": result[0],
      "name": result[1],
      "artist": result[2],
      "genre": result[3],
      "url": result[4],
      "likenessFactor": result[5]
    }
    results_list.append(item)

  return results_list

def create_playlist(playlistName: str, userId: int) -> None:
    """Insert new playlist to Playlists table.

    Args:
        playlistName (str): new playlist name

    Returns: The playlist ID for the inserted entry
    """

    conn = db.connect()
    query = f"INSERT INTO Playlists SELECT MAX(playlistId) + 1, '{playlistName}', {userId} FROM Playlists"
    db.execute(text(query).execution_options(autocommit=True))
    conn.close()


def delete_playlist(playlistId: int) -> None:
    """Delete playlist in Playlists table.

    Args:
        playlistId (int): playlistId to delete
    """

    conn = db.connect()
    query = f"DELETE from Playlists WHERE playlistId={playlistId}"
    db.execute(text(query).execution_options(autocommit=True))
    conn.close()


def update_playlist(playlistId: int, playlistName: str) -> None:
    """Update playlist in Playlists table.

    Args:
        playlistId (int): playlistId to update
        playlistName (str): playlistName to update
    """

    print("playlistId", playlistId)
    print("playlistName", playlistName)

    conn = db.connect()
    query = f"UPDATE Playlists SET playlistName='{playlistName}' WHERE playlistId={playlistId}"
    db.execute(text(query).execution_options(autocommit=True))
    conn.close()


def search_songs(search: str) -> dict:
  """ Search songs in Songs table.

  Args:
    search (str): search query for name
  """


  conn = db.connect()
  query = f"SELECT * FROM Songs WHERE name LIKE '{search}%' ORDER BY name"
  query_results = conn.execute(text(query)).fetchall()
  conn.close()
  song_list = []
  for result in query_results:
      item = {
          "songId": result[0],
          "name": result[1],
          "artist": result[2],
          "genre": result[3],
          "url": result[4],
          "likenessFactor": result[5]
      }
      song_list.append(item)

  return song_list

def get_songs_by_playlist(playlistId: int) -> dict:
  """ Get songs by playlistId

  Args:
    playlistId (int): id for songs to get
  """

  conn = db.connect()
  query = f"SELECT name, artist, r.avg_rating FROM Songs NATURAL JOIN (SELECT songId FROM SongsFoundIn WHERE playlistId = {playlistId}) s LEFT JOIN (SELECT songId, avg(rating) AS avg_rating FROM Reviews GROUP BY songId) r ON Songs.songId = r.songId;"
  query_results = conn.execute(text(query)).fetchall()
  conn.close()
  song_list = []
  for result in query_results:
      item = {
          "name": result[0],
          "artist": result[1],
          "avg_rating": result[2]
      }
      song_list.append(item)

  return song_list

def get_friend_reviews(userId: int) -> dict:
  """ Get reviews by userId of friends

  Args:
    userId (int): id for reviews to get of friends
  """

  conn = db.connect()
  query = f"SELECT Users.userName, sub.name, sub.artist, sub.body, sub.rating FROM (SELECT Reviews.userId, Songs.name, Songs.artist, Reviews.body, Reviews.rating FROM Songs NATURAL JOIN Reviews) sub JOIN Users ON Users.userId = sub.UserId WHERE sub.userId IN (SELECT friendId FROM Friends WHERE userId = {userId}) UNION SELECT Users.userName, sub.name, sub.artist, sub.body, sub.rating FROM (SELECT Reviews.userId, Songs.name, Songs.artist, Reviews.body, Reviews.rating FROM Songs NATURAL JOIN Reviews) sub JOIN Users ON Users.userId = sub.UserId WHERE sub.userId IN (SELECT userId FROM Friends WHERE friendId = {userId});"
  query_results = conn.execute(text(query)).fetchall()
  conn.close()
  song_list = []
  for result in query_results:
      item = {
          "userName": result[0],
          "name": result[1],
          "artist": result[2],
          "body": result[3],
          "rating": result[4]
      }
      song_list.append(item)

  return song_list

def song_exists(songId: str) -> bool:
  conn = db.connect()
  query = f"SELECT * FROM Songs WHERE songId='{songId}';"
  query_results = conn.execute(text(query)).fetchall()
  conn.close()

  return len(query_results) != 0

def add_song_to_playlist(playlistId: int, songId: str) -> None:
  conn = db.connect()
  query = f"INSERT INTO SongsFoundIn Values('{songId}', {playlistId})"
  db.execute(text(query).execution_options(autocommit=True))
  conn.close()

