import logging
import logging.handlers

app_name = 'clock'
mpd_music_folder = r'/var/lib/mpd/music'
local_music_folder = r'./ressources/music/'
local_playlist_folder = r'./ressources/playlist/'
log_folder = r'./log'
syslog_facility = logging.handlers.SysLogHandler.LOG_LOCAL7
user_config_file = r'user.ini'
