import unittest
import time
from sound import *
import os

class TestPlayLis(unittest.TestCase):
    """
    Tests all the sounds in the playlist
    """
    def setUp(self):
        """
        Create a test object
        :return:
        """
        self.player = pympc(os.path.join(config.local_playlist_folder,
                                         'playlist.ini'))

    def tearDown(self):
        del self.player

    def testAllSounds(self):
        """
        Verify all sounds can be heard from 10 seconds
        """
        tunes = self.player.get_playlist()

        for tune in tunes:
            self.player.play(tune)
            time.sleep(10)
            self.player.stop()
            user_input = raw_input("Have your heard \'{!s}\' (y/n): ".format(tune))
            self.assertTrue(user_input.lower() == 'y')
