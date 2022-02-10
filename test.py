import logging
import server
import client
from time import sleep
import pytest
# yield is disabled in pytest

logging.basicConfig(filename='test.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestClientServer:
    def test_just_works(self):
        var = [0]
        logger.debug('Test just works')

        def func(x):
            logger.debug('func')
            assert x[0] == 0
            x[0] = 1

        with server.Server() as serv:
            cl = client.Client()
            cl.run(func, {'x': var})
            sleep(2)
            serv.notify_all()
            sleep(0.5)
            cl.shutdown()
        assert var[0] == 1
        sleep(2)

    # ToDo: add multiple client test

    # ToDo: add client disconnect test
