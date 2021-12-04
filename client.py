import socket
import cfg
import threading
import logging


class Client:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __find_server(self):
        logging.debug('CLIENT: Finding server')
        for address in cfg.IP_ADDRESSES:
            server_address = (address, cfg.PORT)
            try:
                self.__socket.connect(server_address)
                logging.info(f'CLIENT: Connected to {server_address}')
                return True
            except (ConnectionRefusedError, OSError):
                logging.debug(f'CLIENT: {server_address} unavailable')
        logging.info('CLIENT: No servers found')
        return False

    def __wait_and_exec(self, func):
        try:
            while True:
                data = self.__socket.recv(1).decode()
                if len(data) == 0:
                    break
                logging.debug('CLIENT: Command received')
                func()
        finally:
            self.__socket.close()

    def run_here(self, func):
        if self.__find_server():
            self.__wait_and_exec(func)

    def run(self, func):
        logging.debug('CLIENT: Client started')
        threading.Thread(target=self.run_here, args=[func]).start()
