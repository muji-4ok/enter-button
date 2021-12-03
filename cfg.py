# Config file
import os
import webbrowser
import time

DEVICE_NAME = 'SIGMACHIP'
WAIT_TIME = 1
USER_ID = 1000
GROUP_ID = 1000
SFX_DIR = '/home/roma/E/Windows/Users/Vasily/PycharmProjects/enter-button/sfx'
ENV_FILE = '/home/roma/E/Windows/Users/Vasily/PycharmProjects/enter-button/env'     # created by user_env.py
SOUND_ACTION_WEIGHT = 1
VIDEO_ACTION_WEIGHT = 3
DEBUG = True


def SOUND_PLAY_FUNCTION(sound):
    def func():
        if os.getuid() == 0:
            os.setgroups([])
            os.setgid(GROUP_ID)
            os.setuid(USER_ID)
        os.system('mpv ' + '"' + SFX_DIR + '/' + sound + '"')
    return func


def OPEN_LINK(link):
    def func():
        if os.getuid() == 0:
            os.setgroups([])
            os.setgid(GROUP_ID)
            os.setuid(USER_ID)
        webbrowser.open(link)
    return func

def SHUTDOWN():
    if os.getuid() == 0:
        os.setgroups([])
        os.setgid(GROUP_ID)
        os.setuid(USER_ID)
    os.system('mpv ' + '"' + SFX_DIR + '/' + 'Microsoft Windows XP Shutdown - Sound Effect (HD).m4a' + '"')
    time.sleep(3)
    os.system('shutdown now')
