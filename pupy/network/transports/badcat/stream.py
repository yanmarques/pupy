from network.lib.rpc.core import Stream


class OnionServiceStream(Stream):
    """A stream over a Tor Onion Service"""

    __slots__ = ("conn_id", "_reader", "_writer", "_closed", "_poller")

    MAX_IO_CHUNK = 4096

    def __init__(self, conn_id):
        self.conn_id = conn_id
        self._closed = False

        # badcat functions are only available
        # at runtime, so we can't import at the 
        # global level
        from _pupy import (
            badcat_read_conn,
            badcat_write_conn,
            badcat_poll_conn,
        )

        self._reader = badcat_read_conn
        self._writer = badcat_write_conn
        self._poller = badcat_poll_conn

    @property
    def closed(self):
        return self._closed

    def close(self):
        self._closed = True

    def fileno(self):
        raise RuntimeError('Can not obtain the file descriptor of a OnionServiceStream')

    def poll(self, timeout):
        return self._poller(self.conn_id, 0)

    def read(self, count):
        try:
            buf = self._reader(self.conn_id, min(self.MAX_IO_CHUNK, count))
        except Exception as exc:
            self.close()
            raise EOFError(exc)
        return buf

    def write(self, data, notify=False):
        if not type(data) == str:
            data = data.read()
        try:
            while data:
                body = data[:self.MAX_IO_CHUNK]
                count = self._writer(self.conn_id, body)
                data = data[count:]
        except Exception as exc:
            self.close()
            raise EOFError(exc)
