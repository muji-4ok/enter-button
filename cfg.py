# Config file
import os
import webbrowser
import time
from pathlib import Path

DEVICE_NAME = 'SIGMACHIP'
WAIT_TIME = 1
USER_ID = 1000
GROUP_ID = 1000
SFX_DIR = Path(__file__).parent / 'sfx'
ENV_FILE = Path(__file__).parent / 'env'     # created by user_env.py
SOUND_ACTION_WEIGHT = 1
VIDEO_ACTION_WEIGHT = 3
DEBUG = True


def sound_play_function(sound):
    def func():
        if os.getuid() == 0:
            os.setgroups([])
            os.setgid(GROUP_ID)
            os.setuid(USER_ID)
        os.system('mpv ' + '"' + sound + '"')
    return func


def open_link(link):
    def func():
        if os.getuid() == 0:
            os.setgroups([])
            os.setgid(GROUP_ID)
            os.setuid(USER_ID)
        webbrowser.open(link)
    return func


def shutdown_action():
    if os.getuid() == 0:
        os.setgroups([])
        os.setgid(GROUP_ID)
        os.setuid(USER_ID)
    os.system('mpv ' + '"' + (Path(SFX_DIR) / 'Microsoft Windows XP Shutdown - Sound Effect (HD).m4a').absolute() + '"')
    time.sleep(3)
    os.system('shutdown now')
