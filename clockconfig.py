import logging
import logging.handlers

app_name = 'clock'
mpd_music_folder = r'/var/lib/mpd/music'
local_music_folder = r'./ressources/music/'
local_playlist_folder = r'./ressources/playlist/'
log_folder = r'./log'
syslog_facility = logging.handlers.SysLogHandler.LOG_LOCAL7
user_config_file = r'user.ini'

mpd_restart_time = 5 #s
default_cross_fade = 3
initial_sound_volume = 10
ramp_up_period = 0.1 #s


