from gui import app
from flask import render_template, request, jsonify
from sound.sound import *
import os
import clockconfig


player = pympc(os.path.join(clockconfig.local_playlist_folder,
                                         'playlist.ini'))

@app.route('/')
@app.route('/index')
def index():
    return render_template("main.html")


@app.route('/play_state', methods=['GET'])
def get_play_state():
    return jsonify(play=False,
                   track='test')


@app.route('/play_request', methods=['POST'])
def request_play():

    player.play("star-trek")
    return 'OK'