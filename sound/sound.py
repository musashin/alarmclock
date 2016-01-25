from mpd import MPDClient
import time
import ConfigParser
import shutil
import os
import clockconfig
from utils.decorators import *
from threading import Timer

class pympc:
    """
    A simple python client to MPC will all I need
    This is based on python-mpd2
    for help see http://pythonhosted.org/python-mpd2/topics/commands.html
    """
    @fail_if_exception
    def __init__(self, playlist_file):

        self.current_volume = 50
        self.ramp_up_thread = None
        self.playlist = list()
        self.client = MPDClient()               # create client object
        self.client.timeout = None              # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.client.connect("localhost", 6600)  # connect to localhost:6600
        self.client.clear()
        self.client.repeat(1)
        self.client.single(1)
        self.client.consume(0)
        self.__update__music__lib()
        self.load_config(playlist_file)
        self.client.stop()

    def __del__(self):
        if self.ramp_up_thread:
            self.ramp_up_thread.join()
        self.client.close()
        self.client.disconnect()

    def __update__music__lib(self):
        src_files = os.listdir(clockconfig.local_music_folder)
        for file_name in src_files:
            full_file_name = os.path.join(clockconfig.local_music_folder, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, clockconfig.mpd_music_folder)
        time.sleep(clockconfig.mpd_restart_time)
        self.client.update()

    def load_config(self, playlist_file):
        config = ConfigParser.RawConfigParser()
        config.read(playlist_file)

        for channel in config.sections():
            try:
                uri = config.get(channel, 'uri')

                try:
                    crossfade = int(config.get(channel, 'crossfade'))
                except:
                    crossfade = clockconfig.default_cross_fade

                id = self.client.addid(uri)
                self.playlist.append({'name': channel, 'uri': uri, 'id': id, 'crossfade': crossfade})
            except Exception as e:
                logging.getLogger(clockconfig.app_name).warning('Could not add sound {!s} [{!s}]'.format(channel, e))

    @return_false_if_exception
    def play(self, name):
        id = [entry['id'] for entry in self.playlist if entry['name'] == name][0]
        crossfade = [entry['crossfade'] for entry in self.playlist if entry['name'] == name][0]

        self.client.setvol(int(clockconfig.initial_sound_volume))

        self.ramp_up_thread = Timer(clockconfig.ramp_up_period, self.ramp_up_volume,
                                    [crossfade, clockconfig.initial_sound_volume, clockconfig.initial_sound_volume, self.current_volume]).start()

        self.client.playid(id)

    @return_false_if_exception
    def set_volume(self, volume_in_percent):

        self.current_volume = volume_in_percent

        self.client.setvol(min(100, int(self.current_volume)))

    def ramp_up_volume(self, crossfade_time, initial_volume, current_volume, target_volume):
        """
        Ramp-up the sound volume in a thread
        :param crossfade_time: Time during which the volume will ramp-up
        :param initial_volume: Volume when sound was started [0-100]
        :param current_volume: Current Sound Volume [0-100]
        :param target_volume: target Final Volume [0-100]
        :return:
        """
        try:

            current_volume += (target_volume - initial_volume)/crossfade_time * clockconfig.ramp_up_period

            self.client.setvol(min(100, int(current_volume)))

            if current_volume < target_volume and current_volume < 100:

                self.ramp_up_thread = Timer(clockconfig.ramp_up_period, self.ramp_up_volume,
                                      [crossfade_time, initial_volume, current_volume, self.current_volume]).start()
            else:
                self.ramp_up_thread = None
        except Exception as e:
            print e
            self.client.setvol(self.current_volume)

    @return_false_if_exception
    def stop(self):
        self.client.stop()

    def is_playing(self):
        return self.client.status()['state'] == 'play'

    @fail_if_exception
    def get_playlist(self):
        return [entry['name'] for entry in self.playlist]


