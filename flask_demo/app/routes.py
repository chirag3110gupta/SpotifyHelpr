""" Specifies routing for the application"""
from flask import render_template, request, jsonify, Flask
from app import app
from app import database as db_helper

import logging

handler = logging.FileHandler("test.log")  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)         # Set the log level to debug

USR = 90

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
  app.logger.debug("edit", data)

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
  app.logger.debug("create", data)

  db_helper.create_playlist(data["playlistName"], USR)
  result = {"success": True, "response": "Done"}
  return jsonify(result)


@app.route("/search", methods=["POST"])
def search():
  """ receives posts request to search songs """

  data = request.get_json()
  app.logger.debug("search", data)

  song_list = db_helper.search_songs(data["text"])
  result = {"success": True, "response": "Done", "song_list": song_list}

  return jsonify(result)


@app.route("/playlists")
def playlists():
  """ returns playlist page """
  items = db_helper.fetch_playlistsForUser(USR)
  return render_template("playlist.html", items=items, usr=USR)


@app.route("/songs")
def songs():
  """ returns songs page """
  return render_template("song.html")


@app.route("/")
def homepage():
  """ returns rendered homepage """
  return render_template("home.html")

