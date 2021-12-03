# Config file
import os
import time
import webbrowser
from pathlib import Path

import playsound

DEVICE_NAME = 'SIGMACHIP'
DEVICE_CONNECTION_TIMEOUT = 1
USER_ID = 1000
GROUP_ID = 1000
SFX_DIR = Path(__file__).parent / 'sfx'
ENV_FILE = Path(__file__).parent / 'env'  # created by user_env.py
SOUND_ACTION_WEIGHT = 1
VIDEO_ACTION_WEIGHT = 3
SHUTDOWN_ACTION_WEIGHT = 0
DEBUG = True
USE_PLAYSOUND = True


def drop_privileges():
    if os.getuid() == 0:
        os.setgroups([])
        os.setgid(GROUP_ID)
        os.setuid(USER_ID)


def play_sound(sound_path: str):
    drop_privileges()

    if USE_PLAYSOUND:
        playsound.playsound(sound_path, block=False)
    else:
        os.system(f'mpv "{sound_path}"')


def sound_play_function(sound_path: str):
    return lambda: play_sound(sound_path)


def open_link(link: str):
    def func():
        drop_privileges()
        webbrowser.open(link)

    return func


def shutdown_action():
    windows_sfx = str((Path(SFX_DIR) / 'Microsoft Windows XP Shutdown - Sound Effect (HD).m4a').absolute())
    play_sound(windows_sfx)
    time.sleep(3)
    os.system('shutdown now')
