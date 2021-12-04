import time
import random
import threading
import logging
import evdev

import cfg
import server
import client
import random_actions


def exec_random_action():
    threading.Thread(target=random.choices(random_actions.RANDOM_ACTIONS, weights=random_actions.WEIGHTS)[0]).start()


def main():
    logging.basicConfig(filename='run.log', encoding='utf-8', level=cfg.LEVEL, format='%(asctime)s %(message)s')
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
                logging.info(f'Device {name} grabbed')
                serv.run()
                logging.info('Server started')
                client.Client().run(exec_random_action)
                logging.info('Server client started')

                for event in device.read_loop():
                    # key down
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                        logging.debug(event)
                        serv.notify_all()
            except OSError:
                logging.info(f'Device {name} unplugged')
                serv.shutdown()
            except BaseException as e:
                logging.exception('Caught exception', exc_info=e)
                serv.shutdown()
                device.ungrab()
                break
        else:
            try:
                client.Client().run(exec_random_action)
            except KeyboardInterrupt as e:
                logging.exception('Caught exception', exc_info=e)
                break

        time.sleep(cfg.DEVICE_CONNECTION_TIMEOUT)


if __name__ == '__main__':
    main()
