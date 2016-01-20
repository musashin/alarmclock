from flask import Flask

app = Flask(__name__)
cmdQueueFromUIToAlarm = None
currentPlayState = None
playlist = None

from gui import views


