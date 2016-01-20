from gui import app
from flask import render_template, request, jsonify

from messages.commands import SoundCmd



@app.route('/')
@app.route('/index')
def index():
    return render_template("main.html")


@app.route('/play_state', methods=['GET'])
def get_play_state():
    print app.playlist
    return jsonify(play=app.currentPlayState['status'] == 'playing',
                   track=app.currentPlayState['track'])


@app.route('/play_request', methods=['POST'])
def request_play():

    print app.currentPlayState
    print app.playlist

    app.cmdsToClock.put(SoundCmd('play', 'toto'))

    return 'OK'