from gui import app
from flask import render_template, request, jsonify

from messages.commands import SoundCmd



@app.route('/')
@app.route('/index')
def index():
    print app.playlist
    return render_template("main.html", tracks=app.playlist)


@app.route('/play_state', methods=['GET'])
def get_play_state():

    return jsonify(play=app.currentPlayState['status'] == 'playing',
                   track=app.currentPlayState['track'])


@app.route('/play_request', methods=['POST'])
def request_play():
    """
    POST request for playing a track
    :return:
    """

    app.cmdsToClock.put(SoundCmd('play', track=request.form['track']))

    return 'OK'

@app.route('/stop_request', methods=['POST'])
def request_stop():
    """
    POST request to stop playing music
    :return:
    """

    app.cmdsToClock.put(SoundCmd('stop', track=None))

    return 'OK'