import threading
import hardware.display
from datetime import datetime
from sound.sound import *
import os
import clockconfig
from messages import commands
import logging
from multiprocessing import Queue

exit_event = threading.Event()

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


def handle_commands(cmd_queue, clock_play_state):
    """
    Handle commands from user interface
    :param cmd_queue:
    :return:
    """
    try:
        cmd = cmd_queue.get(False)
    except:
        pass
    else:
        while cmd:

            execute_user_command(cmd, clock_play_state)

            try:
                cmd = cmd_queue.get(False)
            except:
                cmd = None


def execute_user_command(cmd, clock_play_state):
    """
    Execute an user cmd
    :param cmd: class describing the command to execute
    :return:
    """
    if type(cmd) is commands.SoundCmd:

        if cmd.type == 'play':
            if player.play(cmd.track):
                clock_play_state['status'] = 'playing'
                clock_play_state['track'] = cmd.track
        if cmd.type == 'stop':
            if player.stop():
                clock_play_state['status'] = 'idle'
                clock_play_state['track'] = None


    else:
        logging.getLogger(clockconfig.app_name).warning('Unsupported Cmd ({!s} not recognised)'.format(type(cmd)))


def mainloop(**kwargs):

    handle_commands(kwargs['commands_from_user'], kwargs['clock_play_state'])

    update_display(update_alarms())

    kwargs['clock_started_event'].set()

    threading.Timer(clockconfig.clock_period_in_s, mainloop, kwargs=kwargs).start()


def process(**kwargs):
    """
    Main alarm clock loop
    :return:
    """

    for track in player.get_playlist():
        kwargs['playlist'].append(track)

    exit_event.clear()

    threading.Timer(clockconfig.clock_period_in_s, mainloop, kwargs=kwargs).start()

    exit_event.wait()




