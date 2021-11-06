"""Defines all the functions related to the database"""
from app import db

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
    playlist_list = []
    for result in query_results:
        item = {
            "songId": result[0],
            "playlistId": result[1]
        }
        playlist_list.append(item)

    return songsFoundIn_list


def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()
