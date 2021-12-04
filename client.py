import socket
import cfg
import threading
import logging


class Client:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __find_server(self):
        for address in cfg.IP_ADDRESSES:
            try:
                server_address = (address, cfg.PORT)
                self.__socket.connect(server_address)
                logging.info(f'Connected to {server_address}')
                return True
            except (ConnectionRefusedError, OSError):
                pass
        logging.info('No servers found')
        return False

    def __wait_and_exec(self, func):
        try:
            while True:
                data = self.__socket.recv(1).decode()
                if len(data) == 0:
                    break
                logging.debug('Command received')
                func()
        finally:
            self.__socket.close()

    def __run(self, func):
        if self.__find_server():
            self.__wait_and_exec(func)

    def run(self, func):
        threading.Thread(target=self.__run, args=[func]).start()
