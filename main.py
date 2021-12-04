import time
import random
import threading

import evdev

import cfg
import server
import client
import random_actions


def exec_random_action():
    threading.Thread(target=random.choices(random_actions.RANDOM_ACTIONS, weights=random_actions.WEIGHTS)[0]).start()


def main():
    while True:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        device = None

        for device_iterator in devices:
            if cfg.DEVICE_NAME in device_iterator.name:
                device = device_iterator

        if device is not None:
            name = device.name
            serv = server.Server()
            try:
                device.grab()
                print(f'Device {name} grabbed')
                serv.run()
                print('Server started')
                client.Client().run(exec_random_action)
                print('Server client started')

                for event in device.read_loop():
                    # key down
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                        if cfg.DEBUG:
                            print(event)
                        serv.notify_all()
            except OSError:
                print(f'Device {name} unplugged')
                serv.shutdown()
            except BaseException as e:
                print(f'Caught exception {e}')
                serv.shutdown()
                device.ungrab()
                break
        else:
            try:
                client.Client().run(exec_random_action)
            except KeyboardInterrupt as e:
                print(f'Caught exception {e}')
                break

        time.sleep(cfg.DEVICE_CONNECTION_TIMEOUT)


if __name__ == '__main__':
    main()
