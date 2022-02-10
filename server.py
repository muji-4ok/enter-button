import cfg
import socket
import threading
import time
import logging


class Server:
    def __init__(self, logger=logging.getLogger(None)):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setblocking(False)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_address = ('0.0.0.0', cfg.PORT)
        self.__cv = threading.Condition()
        self.__is_shutdown = False
        self.__main_thread = None
        self.__logger = logger

    def __servant(self, connection: socket.socket, client_address):
        with self.__cv:
            try:
                self.__cv.wait()
                while not self.__is_shutdown:
                    self.__logger.debug(f'SERVER: Notifying {client_address}')
                    connection.sendall(bytes(1))
                    self.__cv.wait()
                self.__logger.info(f'SERVER: {client_address} dropped')
                connection.shutdown(socket.SHUT_RDWR)
                connection.close()
            except BrokenPipeError:  # client disconnected
                self.__logger.warning(f'SERVER: {client_address} disconnected')
                connection.close()

    def __running_cycle(self):
        try:
            self.__logger.debug('SERVER: In running cycle')
            while not self.__is_shutdown:
                try:
                    connection, client_address = self.__socket.accept()
                    # Throws an exception if there are no pending connections
                    self.__logger.info(f'SERVER: {client_address} connected')
                    threading.Thread(target=self.__servant, args=[connection, client_address]).start()
                except BlockingIOError as e:
                    time.sleep(cfg.CONNECTION_WAIT_PERIOD)
        finally:
            self.__logger.debug('SERVER: Socket closed')
            self.__socket.close()

    def __enter__(self):
        self.__socket.bind(self.__server_address)
        self.__socket.listen()
        self.__logger.info('SERVER: Server started')
        self.__main_thread = threading.Thread(target=self.__running_cycle)
        self.__main_thread.start()
        return self

    def notify_all(self):
        self.__logger.debug('SERVER: Notifying')
        with self.__cv:
            self.__cv.notify_all()

    def __exit__(self, exc_type, exc_value, traceback):
        self.__is_shutdown = True
        self.notify_all()
