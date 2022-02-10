import socket
import cfg
import threading
import logging


class Client:
    def __init__(self, logger=logging.getLogger(None)):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__shutdown = False
        self.__logger = logger
        self.__running = False

    def __find_server(self):
        self.__logger.debug('CLIENT: Finding server')
        for address in cfg.IP_ADDRESSES:
            server_address = (address, cfg.PORT)
            try:
                self.__socket.connect(server_address)
                self.__logger.info(f'CLIENT: Connected to {server_address}')
                return True
            except (ConnectionRefusedError, OSError):
                self.__logger.warning(f'CLIENT: {server_address} unavailable')
        self.__logger.warning('CLIENT: No servers found')
        return False

    def __wait_and_exec(self, func, args):
        try:
            while not self.__shutdown:
                data = self.__socket.recv(1).decode()  # ToDo: add timeout
                if len(data) == 0:
                    break
                self.__logger.debug('CLIENT: Command received')
                func(**args)
        finally:
            self.__socket.close()

    def run_here(self, func, args={}):
        self.__running = True
        if self.__find_server():
            self.__wait_and_exec(func, args)

    def run(self, func, args={}):
        if self.__running:
            raise RuntimeError('Already running')
        self.__logger.info('CLIENT: Client started')
        threading.Thread(target=self.run_here, args=[func, args]).start()

    def shutdown(self):  # ToDo: add timeout
        self.__running = False
        self.__shutdown = True
        self.__socket.close()
