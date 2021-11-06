""" Specifies routing for the application"""
from flask import render_template, request, jsonify, Flask
from app import app
from app import database as db_helper

import logging

handler = logging.FileHandler("test.log")  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)         # Set the log level to debug

USR = 90

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.delete_playlist(task_id)
        console.log("removing", task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()
    app.logger.debug(data)

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    app.logger.debug(db_helper.insert_new_song(data['songId'], data['playlistId']))
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_playlistsForUser(USR)
    for item in items:
        songs = db_helper.fetch_songsForPlaylist(item["playlistId"])
        #app.logger.debug(songs)
        item["songs"] = songs

    #app.logger.debug(items)
    return render_template("index.html", items=items)
