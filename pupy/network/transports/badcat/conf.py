from .server import OnionServiceServer
from .stream import OnionServiceStream
from network.lib import DummyPupyTransport
from network.transports import Transport


class TransportConf(Transport):
    info = "Badcat Tor Onion Service Transport"
    name="badcat"
    server=OnionServiceServer
    stream=OnionServiceStream
    server_transport=DummyPupyTransport
