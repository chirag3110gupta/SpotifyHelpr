""" Specifies routing for the application"""
from flask import render_template, request, redirect, jsonify, session, Flask
from app import app
from app import database as db_helper

import logging

app.secret_key = "secret"

handler = logging.FileHandler("test.log")  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)         # Set the log level to debug

@app.route("/delete", methods=["POST"])
def delete():
  """ received post requests for entry delete """

  data = request.get_json()

  try:
    db_helper.delete_playlist(data["playlistId"])
    result = {"success": True, "response": "Removed task"}
  except:
    result = {"success": False, "response": "Something went wrong"}

  return jsonify(result)


@app.route("/edit", methods=["POST"])
def update():
  """ received post requests for entry updates """

  data = request.get_json()

  try:
    db_helper.update_playlist(data["playlistId"], data["playlistName"])
    result = {"success": True, "response": "Status Updated"}
  except:
    result = {"success": False, "response": "Something went wrong"}

  return jsonify(result)


@app.route("/create", methods=["POST"])
def create():
  """ receives post requests to create playlist """

  data = request.get_json()

  db_helper.create_playlist(data["playlistName"], USR)
  result = {"success": True, "response": "Done"}
  return jsonify(result)


@app.route("/search", methods=["POST"])
def search():
  """ receives posts request to search songs """

  data = request.get_json()

  song_list = db_helper.search_songs(data["text"])
  result = {"success": True, "response": "Done", "song_list": song_list}

  return jsonify(result)


@app.route("/get_songs", methods=["POST"])
def get_songs():
  """ receives post requests to get songs from playlist """

  data = request.get_json()

  song_list = db_helper.get_songs_by_playlist(data["playlistId"])
  result = {"success": True, "response": "Done", "song_list": song_list, "playlistName": data["playlistName"]}

  return jsonify(result)

@app.route("/add_song", methods=["POST"])
def add_song():
  """ receives post requests to add songs to playlist """

  data = request.get_json()
  if(db_helper.song_exists(data["songId"])):
    db_helper.add_song_to_playlist(data["playlistId"], data["songId"])

    result = {"success": True, "response": "Done", "data": data}
    return jsonify(result)

  result = {"success": False, "response": "Done", "data": data}
  return jsonify(result)



@app.route("/home")
def homepage():
  """ returns rendered homepage """
  if("userId" in session):
    friend_reviews_data = db_helper.get_friend_reviews(session["userId"])
    playlist_data = db_helper.fetch_playlistsForUser(session["userId"])
    return render_template("home.html", friend_reviews_data=friend_reviews_data, playlist_data=playlist_data, usr=session["userId"])

  else:
    return redirect("/login")

@app.route("/login", methods=["POST", "GET"])
def login():
  """ returns rendered login page """
  if(request.method == "POST" and request.form.get("userId") != ""):
    session["userId"] = request.form.get("userId")
    return redirect("/home")

  return render_template("login.html")

@app.route("/logout")
def logout():
  """ redirects user to login page """
  session.pop("userId")
  return redirect("/login")

@app.route("/")
def default():
  if("userId" in session and session["userId"] != -1):
    return redirect("/home")

  else:
    return redirect("/login")
