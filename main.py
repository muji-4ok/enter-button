import time
import subprocess
import logging
import evdev

import cfg
import server
import client
from pathlib import Path


def exec_random_action():
    subprocess.Popen(['python ' + str(Path(__file__).parent / 'random_actions.py')], shell=True)


def main():
    logging.basicConfig(filename='run.log', encoding='utf-8', level=cfg.LEVEL, format='%(asctime)s %(message)s')
    while True:
        logging.debug(f'APP: Scanning devices')
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        device = None

        for device_iterator in devices:
            if cfg.DEVICE_NAME == device_iterator.name:
                device = device_iterator

        logging.debug('APP: Device search completed')
        if device is not None:
            name = device.name
            serv = server.Server()
            try:
                device.grab()
                logging.info(f'SERVER: Device {name} grabbed')
                serv.run()
                logging.info('SERVER: Server started')
                client.Client().run(exec_random_action)

                for event in device.read_loop():
                    # key down
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                        logging.debug(event)
                        serv.notify_all()
            except OSError:
                logging.info(f'SERVER: Device {name} unplugged')
                logging.info('SERVER: Shutting down')
                serv.shutdown()
            except KeyboardInterrupt:
                logging.info('SERVER: Shutting down')
                serv.shutdown()
                device.ungrab()
                break
            except BaseException as e:
                logging.exception('SERVER: Unexpected exception', exc_info=e)
                serv.shutdown()
                device.ungrab()
                break

            time.sleep(cfg.DEVICE_CONNECTION_TIMEOUT)
        else:
            try:
                logging.debug('CLIENT: Device not found, running client')
                client.Client().run_here(exec_random_action)
                time.sleep(cfg.DEVICE_CONNECTION_TIMEOUT)
            except KeyboardInterrupt:
                logging.info('CLIENT: Shutting down')
                break
            except BaseException as e:
                logging.exception('CLIENT: Unexpected exception', exc_info=e)
                break


if __name__ == '__main__':
    main()
