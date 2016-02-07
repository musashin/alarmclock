from gui import app
from flask import render_template, request, jsonify

from messages.commands import SoundCmd



@app.route('/')
@app.route('/index')
def index():

    week_days = ('lundi','mardi','mercredi','jeudi', 'vendredi', 'samedi', 'dimanche')
    schedule = {'lundi':[{'nath': {'state': True, 'time': '12:30', 'id':2}, 'nico': {'state': False, 'time': '9:30'}}]*24,
            'mardi':[{'nath': {'state': True, 'time': '12:30', 'id':2}, 'nico': {'state': True, 'time': '12:30', 'id':2}}]*24,
            'mercredi': [{'nath': {'state': False, 'time': '9:30'}, 'nico': {'state': True, 'time': '12:30', 'id': 2}}]*24,
            'jeudi': [{'nath': {'state': True, 'time': '12:30', 'id': 2}, 'nico': {'state': False, 'time': '9:30'}}]*24,
            'vendredi': [{'nath': {'state': True, 'time': '12:30', 'id': 2}, 'nico': {'state': False, 'time': '9:30'}}]*24,
            'samedi': [{'nath': {'state': True, 'time': '12:30', 'id': 2}, 'nico': {'state': False, 'time': '9:30'}}]*24,
            'dimanche': [{'nath': {'state': True, 'time': '12:30', 'id': 2}, 'nico': {'state': False, 'time': '9:30'}}]*24}

    return render_template("main.html", tracks=app.playlist,
                                        schedule=schedule,
                                        week_days=week_days)


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

@app.route('/set_volume', methods=['POST'])
def set_volume():
    """
    POST request to set music volume
    :return:
    """
    app.cmdsToClock.put(SoundCmd('volume', track=None, vol=request.form['volume']))

    return 'OK'

@app.route('/alarm', methods=['GET'])
def get_laram_details():
    """

    """
    return render_template("alarmdetails.html")