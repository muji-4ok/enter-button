from pathlib import Path

import evdev

COMMUNICATION_FILE = Path('/home/egork/Projects/py/EnterButton/commander')

if not COMMUNICATION_FILE.exists():
    print('File doesn\'t exits. Make it without sudo')
    exit(1)

device = evdev.InputDevice('/dev/input/event18')

try:
    device.grab()

    for event in device.read_loop():
        # key down
        if event.type == evdev.ecodes.EV_KEY and event.value == 1:
            print(event)

            with open(COMMUNICATION_FILE, 'w') as f:
                f.write('1')
finally:
    device.ungrab()
