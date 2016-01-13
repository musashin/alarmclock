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


def handle_commands(cmd_queue):
    """
    Handle commands from user interface
    :param cmd_queue:
    :return:
    """
    cmd = cmd_queue.get()

    while cmd:

        execute_user_command(cmd)

        cmd = cmd_queue.get()


def execute_user_command(cmd):
    """
    Execute an user cmd
    :param cmd: class describing the command to execute
    :return:
    """
    if type(cmd) is commands.SoundCmd:

        player.play('star-trek')

    else:
        logging.getLogger(clockconfig.app_name).warning('Unsupported Cmd ({!s} not recognised)'.format(type(cmd)))


def mainloop(cmdQueue):
    """
    Main alarmclock loop
    :return:
    """

    handle_commands(cmdQueue)

    update_display(update_alarms())

    Timer(clockconfig.clock_period_in_s, mainloop).start()



