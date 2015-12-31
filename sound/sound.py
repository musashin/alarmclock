from mpd import MPDClient
import time
import ConfigParser
import shutil
import os
import config

class pympc:
    """
    A simple python client to MPC will all I need
    This is based on python-mpd2
    for help see http://pythonhosted.org/python-mpd2/topics/commands.html

    TODO: add expection support!!!
    """
    def __init__(self, playlist_file):
        self.playlist = list()
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.client.connect("localhost", 6600)  # connect to localhost:6600
        self.client.clear()
        self.client.repeat(1)
        self.client.single(1)
        self.client.consume(0)
        self.__update__music__lib()
        self.load_config(playlist_file)

    def __del__(self):
        self.client.close()
        self.client.disconnect()

    def __update__music__lib(self):
        src_files = os.listdir(config.local_music_folder)
        for file_name in src_files:
            full_file_name = os.path.join(config.local_music_folder, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, config.mpd_music_folder)
        time.sleep(10)
        self.client.update()

    def load_config(self, playlist_file):
        config = ConfigParser.RawConfigParser()
        config.read(playlist_file)

        for channel in config.sections():
            uri = config.get(channel, 'uri')
            id = self.client.addid(uri)
            self.playlist.append({'name': channel, 'uri': uri, 'id':id})

    def play(self, name):
        id = [entry['id'] for entry in self.playlist if entry['name'] == name][0]
        self.client.playid(id)

    def stop(self):
        self.client.stop()

    def is_playing(self):
        return self.client.status()['state'] == 'play'

    def get_playlist(self):
        return [entry['name'] for entry in self.playlist]


