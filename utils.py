import keyboard
import pickle
import os
import time
import webbrowser
from pathlib import Path
import cfg
import playsound
import random
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

CUR_DIR = Path(__file__).parent
SFX_DIR = CUR_DIR / 'sfx'
ENV_FILE = CUR_DIR / 'env'  # created by setup.py


def drop_privileges():
    if os.getuid() == 0:
        os.setgroups([])
        os.setgid(cfg.GROUP_ID)
        os.setuid(cfg.USER_ID)


def play_sound(sound_path: str):
    drop_privileges()
    set_user_env()

    if cfg.USE_PLAYSOUND:
        playsound.playsound(sound_path, block=False)
    else:
        os.system(f'mpv "{sound_path}"')


def load_user_env() -> dict[str, str]:
    with open(ENV_FILE, 'rb') as f:
        data = pickle.load(f)

    return data


def set_user_env():
    os.environ.clear()

    for name, value in load_user_env().items():
        os.environ[name] = value


def open_link(link: str):
    if cfg.BAD_BROWSER:
        pid = os.fork()
        assert pid >= 0

        if pid == 0:
            drop_privileges()
            set_user_env()
            webbrowser.open(link)
            time.sleep(1.5)
            exit(0)
        else:
            # FixMe : doesn't work
            os.waitpid(pid, 0)
            keyboard.write(' ')
    else:
        drop_privileges()
        set_user_env()
        webbrowser.open(link)


def shutdown_action():
    windows_sfx = str((Path(SFX_DIR) / 'Microsoft Windows XP Shutdown - Sound Effect (HD).m4a').absolute())
    play_sound(windows_sfx)
    time.sleep(3)
    os.system('shutdown now')


def say_line(line):
    drop_privileges()
    set_user_env()
    Notify.init('enter-button')
    Notify.Notification.new(line).show()
    Notify.uninit()
    #line = 'test'
    os.system(f'espeak-ng -g 5 -s 170 -v "en" "{line}"')


def random_insult():
    drop_privileges()
    set_user_env()
    say_line(random.choice(open("model/insults.txt").readlines()))
