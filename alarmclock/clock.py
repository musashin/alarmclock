from threading import Timer
import hardware.display
from datetime import datetime
from sound.sound import *
import os
import clockconfig
from messages import commands
import logging



player = pympc(os.path.join(clockconfig.local_playlist_folder,
                                         'playlist.ini'))

def update_alarms():
    """
    Trigger alarm if required
    :return:
    """
    return False, False


def update_display(alarms_on):
    """
    Update the alarmclock display
    If no alarm is active, the momentary
    snooze button will cause the temperature to be displayed
    In any other situations,the current system time will be displayed
    :return:
    """
    current_time = datetime.now().time()

    hardware.display.update_display(('{0:02d}'.format(current_time.hour)[0],
                                     '{0:02d}'.format(current_time.hour)[1],
                                     '{0:02d}'.format(current_time.minute)[0],
                                     '{0:02d}'.format(current_time.minute)[1]))

def handle_cmds(cmdQueue):
    cmd = cmdQueue.get()

    while cmd:

        if type(cmd) is commands.SoundCmd:
            print 'playing'
            player.play('star-trek')

        else:
            logging.getLogger(clockconfig.app_name).warning('Unsupported Cmd ({!s} not recognised)'.format(type(cmd)))

        cmd = cmdQueue.get()



def mainloop(cmdQueue):
    """
    Main alarmclock loop
    :return:
    """

    handle_cmds(cmdQueue)

    update_display(update_alarms())

    Timer(clockconfig.clock_period_in_s, mainloop).start()



