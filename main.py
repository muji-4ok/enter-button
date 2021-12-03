import os
import subprocess
import time

import evdev

import cfg


def main():
    # environment with root privileges
    env_su = os.environ.copy()

    while True:
        # find device
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        device = None

        for device_iterator in devices:
            if cfg.DEVICE_NAME in device_iterator.name:
                device = device_iterator

        if device is None:
            time.sleep(cfg.DEVICE_CONNECTION_TIMEOUT)
            continue

        name = device.name

        try:
            device.grab()
            print(f'Device {name} grabbed')

            for event in device.read_loop():
                # key down
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                    if cfg.DEBUG:
                        print(event)

                    subprocess.Popen(['python random_actions.py'], shell=True, env=env_su)
        except OSError:
            print(f'Device {name} unplugged')
        except Exception as e:
            print(f'Caugh exception {e}')
            device.ungrab()
            break


if __name__ == '__main__':
    main()
