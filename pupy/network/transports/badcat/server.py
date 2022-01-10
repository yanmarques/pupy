import logging

from network.lib.connection import PupyConnection
from network.lib.streams.PupySocketStream import PupyChannel


class OnionServiceServer(object):
    def __init__(self, service, hostname = "", ipv6 = False, port = 0,
                authenticator = None, protocol_config = {}, stream = None,
                transport = None, transport_kwargs = None, pupy_srv = None, logger = None):
        self.active = False
        self._closed = False
        self.service = service
        self.authenticator = authenticator
        self.port = port
        self.protocol_config = protocol_config
        self.clients = set()
        self.stream_class = stream
        self.transport_class = transport
        self.transport_kwargs = transport_kwargs
        self.pupy_srv = pupy_srv
        self.logger = logger or logging.getLogger("%s/%s" % (self.service.get_service_name(), self.port))

        from _pupy import (
            badcat_accept_conn,
            badcat_write_conn,
        )
        self._acceptor = badcat_accept_conn

    def close(self):
        """Closes (terminates) the server and all of its clients. If applicable,
        also unregisters from the registry server"""
        if self._closed:
            return
        self._closed = True
        self.active = False
        self.clients.clear()

    def fileno(self):
        """returns the listener socket's file descriptor"""
        raise RuntimeError("Can not obtain file descriptor of OnionServiceServer")

    def accept(self):
        """accepts an incoming socket connection (blocking)"""
        self.logger.info('Accepting Onion connections on: {}'.format(self.port))
        try:
            conn_id = self._acceptor(self.port)
        except Exception as exc:
            print 'failed listening: {}'.format(exc)
            self.logger.exception(exc)
            raise EOFError(exc)

        if not self.active:
            return

        self.logger.info("accepted %s", conn_id)
        self.clients.add(conn_id)

        # build a connection
        config = dict(self.protocol_config,
                      connid='{}:{}'.format(self.port, conn_id),
                      logger=self.logger,
                      credentials=None)
        stream = self.stream_class(conn_id)
        connection = None

        try:
            self.logger.debug('%s Authenticated. Starting connection', conn_id)

            connection = PupyConnection(
                self.pupy_srv,
                self.service,
                PupyChannel(stream),
                config=config
            )

            self.logger.debug('%s Connection complete', conn_id)
        except Exception as exc:
            self.logger.exception(exc)
        finally:
            self.logger.debug('%s Report connection: %s', conn_id, connection)

        try:
            if connection and connection._local_root:
                connection.init()
                connection.loop()
        except Exception as exc:
            self.logger.exception(exc)
        finally:
            self.logger.debug('%s Connection finished: %s', conn_id, connection)
            self.clients.discard(conn_id)

    def start(self):
        self.active = True

        if not self.port:
            self.port = 8000
        try:
            while self.active:
                self.accept()
        except KeyboardInterrupt:
            print("")
            self.logger.warn("keyboard interrupt!")
        finally:
            self.logger.info("server has terminated")
            self.close()

