import cfg
import socket
import threading
import time
import logging


class Server:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setblocking(False)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_address = ('0.0.0.0', cfg.PORT)
        self.__cv = threading.Condition()
        self.__is_shutdown = False
        self.__main_thread = None

    def __servant(self, connection: socket.socket):
        with self.__cv:
            try:
                self.__cv.wait()
                while not self.__is_shutdown:
                    logging.debug(f'Notifying')
                    connection.sendall(bytes(1))
                    self.__cv.wait()
            except BrokenPipeError:     # client disconnected
                connection.close()
            except BaseException:
                connection.shutdown(socket.SHUT_RDWR)
                connection.close()

    def __running_cycle(self):
        try:
            while not self.__is_shutdown:
                try:
                    connection, client_address = self.__socket.accept()
                    # Throws an exception if there are no pending connections
                    logging.info(f'{client_address} connected')
                    threading.Thread(target=self.__servant, args=[connection]).start()
                except BlockingIOError as e:
                    time.sleep(cfg.CONNECTION_WAIT_PERIOD)
        finally:
            self.__socket.close()

    def run(self):
        self.__socket.bind(self.__server_address)
        self.__socket.listen()
        self.__main_thread = threading.Thread(target=self.__running_cycle)
        self.__main_thread.start()

    def notify_all(self):
        with self.__cv:
            self.__cv.notify_all()

    def shutdown(self):
        self.__is_shutdown = True
        self.notify_all()
