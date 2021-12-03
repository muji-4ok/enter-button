import os

import evdev
import time
import subprocess
import random
import pickle
from pathlib import Path

import cfg


def main():
    env_file = Path(cfg.ENV_FILE)
    env = None
    # environment without root privileges
    with open(env_file, 'rb') as f:
        env = pickle.load(f)
    # environment with root privileges
    env_su = os.environ.copy()

    while True:
        device = None
        # find device
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device_iterator in devices:
            if cfg.DEVICE_NAME in device_iterator.name:
                device = device_iterator

        if device is None:
            continue

        name = device.name
        try:
            device.grab()
            print('Device {} grabbed'.format(name))

            for event in device.read_loop():
                # key down
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                    if cfg.DEBUG:
                        print(event)

                    thread = subprocess.Popen(['python random_actions.py'], shell=True, env=env,
                                              stdout=subprocess.DEVNULL)
        except OSError:
            print('Device {} unplugged'.format(name))
        except KeyboardInterrupt:
            device.ungrab()
            print('\nDevice {} ungrabbed, terminating program'.format(name))
            return
        time.sleep(cfg.WAIT_TIME)


main()
