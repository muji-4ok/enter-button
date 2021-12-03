import time
import keyboard
from pathlib import Path

COMMUNICATION_FILE_SUDOER = Path('/home/egork/Projects/py/EnterButton/sudoer')

if not COMMUNICATION_FILE_SUDOER.exists():
    print('File doesn\'t exits. Make it without sudo')
    exit(1)

while True:
    with open(COMMUNICATION_FILE_SUDOER) as f:
        data = f.read()

        if data:
            if data == '1':
                keyboard.write(' ')
            else:
                print('Oh no')

    with open(COMMUNICATION_FILE_SUDOER, 'w') as f:
        f.write('')

    time.sleep(0.5)
