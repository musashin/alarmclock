from mpd import MPDClient
import time
import ConfigParser

class pympc:
    """
    A simple python client to MPC will all I need
    This is based on python-mpd2
    for help see http://pythonhosted.org/python-mpd2/topics/commands.html

    TODO: add expection support!!!
    """
    def __init__(self, playlist_file):
        self.playlist = list()
        self.load_config(playlist_file)
        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.client.connect("localhost", 6600)  # connect to localhost:6600
        self.client.clear()
        self.client.repeat(1)
        self.client.single(1)
        self.client.consume(1)

    def __del__(self):
        self.client.close()
        self.client.disconnect()

    def load_config(self, playlist_file):
        config = ConfigParser.RawConfigParser()
        config.read(playlist_file)

        for channel in config.sections():
            uri = config.get(channel, 'uri')
            self.playlist.append({'name': channel, 'uri': uri})

    def play(self, name):
        self.client.clear()
        uri = [entry['uri'] for entry in self.playlist if entry['name'] == name][0]
        self.client.add(uri)
        self.client.play()

    def stop(self):
        self.client.stop()
        self.client.clear()

    def is_playing(self):
        return self.client.status()['state'] == 'play'

    def get_playlist(self):
        return [entry['name'] for entry in self.playlist]

if __name__ =='__main__':
    player = pympc('/root/PycharmProjects/alarmclock/ressources/playlist/playlist.ini')

    print player.get_playlist()
    print player.is_playing()
    player.play('alarm')
    print player.is_playing()
    time.sleep(10)
    player.stop()
