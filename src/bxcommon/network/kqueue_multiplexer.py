import select

from bxcommon.network.abstract_multiplexer import AbstractMultiplexer
from bxcommon.network.socket_connection import SocketConnection
from bxcommon.utils import logger


class KQueueMultiplexer(AbstractMultiplexer):

    def __init__(self, communication_strategy):
        super(KQueueMultiplexer, self).__init__(communication_strategy)

        self._kqueue = select.kqueue()
        self._kqueue.control([], 0, 0)


    def run(self):
        try:
            self._start_server()

            timeout = self._communication_strategy.on_first_sleep()

            while True:
                self._establish_outbound_connections()

                events = self._kqueue.control([], 1000, timeout)

                for event in events:
                    assert event.ident in self._socket_connections

                    socket_connection = self._socket_connections[event.ident]
                    assert isinstance(socket_connection, SocketConnection)

                    if event.filter == select.KQ_FILTER_READ and socket_connection.is_server:
                        self._handle_incoming_connections(socket_connection)

                    elif event.filter == select.KQ_FILTER_READ:
                        self._receive(socket_connection)

                    elif event.filter == select.KQ_FILTER_WRITE:
                        socket_connection.can_send = True
                        self._send(socket_connection)

                self._send_all_connections()

                if self._communication_strategy.on_chance_to_exit():
                    logger.debug("Ending KQueue loop. Shutdown has been requested.")
                    break

                timeout = self._communication_strategy.on_sleep(not events)
        finally:
            self.close()

    def close(self):
        super(KQueueMultiplexer, self).close()

        self._kqueue.close()

    def _register_socket(self, socket_to_register, is_server=False, initialized=True):
        super(KQueueMultiplexer, self)._register_socket(socket_to_register, is_server, initialized)

        read_event = select.kevent(
            socket_to_register, select.KQ_FILTER_READ, select.KQ_EV_ADD | select.KQ_EV_ENABLE | select.KQ_EV_CLEAR)
        write_event = select.kevent(
            socket_to_register, select.KQ_FILTER_WRITE, select.KQ_EV_ADD | select.KQ_EV_ENABLE | select.KQ_EV_CLEAR)

        self._kqueue.control([read_event, write_event], 0, 0)
