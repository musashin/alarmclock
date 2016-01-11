from flask import Flask

app = Flask(__name__)
cmdQueueFromUIToAlarm = None

from gui import views


