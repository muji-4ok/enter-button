import os
import random
import time
import webbrowser
from pathlib import Path

import playsound

COMMUNICATION_FILE_COMMANDER = Path('/home/egork/Projects/py/EnterButton/commander')
COMMUNICATION_FILE_SUDOER = Path('/home/egork/Projects/py/EnterButton/sudoer')
SFX_FOLDER = Path('/home/egork/Projects/py/EnterButton/sfx')
SFX_FILENAMES = os.listdir(SFX_FOLDER)


def send_sudoer_command(data: str):
    with open(COMMUNICATION_FILE_SUDOER, 'w') as f:
        f.write(data)


if not COMMUNICATION_FILE_COMMANDER.exists():
    COMMUNICATION_FILE_COMMANDER.touch()

if not COMMUNICATION_FILE_SUDOER.exists():
    COMMUNICATION_FILE_SUDOER.touch()

print(SFX_FILENAMES)

while True:
    with open(COMMUNICATION_FILE_COMMANDER) as f:
        if f.read() == '1':
            action = random.randint(0, len(SFX_FILENAMES) + 1)

            print(action)

            if action < len(SFX_FILENAMES):
                print(SFX_FILENAMES[action])
                playsound.playsound(SFX_FOLDER / SFX_FILENAMES[action], block=False)
            elif action == len(SFX_FILENAMES):
                print('Rick roll')
                webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                time.sleep(1.5)
                send_sudoer_command('1')
            elif action == len(SFX_FILENAMES) + 1:
                print('Spanish inquisition')
                webbrowser.open('https://www.youtube.com/watch?v=sAn7baRbhx4')
                time.sleep(1.5)
                send_sudoer_command('1')
            else:
                print('Oh no')

    with open(COMMUNICATION_FILE_COMMANDER, 'w') as f:
        f.write('')

    time.sleep(0.5)
