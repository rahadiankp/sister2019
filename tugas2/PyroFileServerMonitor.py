class Monitor(object):
    def __init__(self, type: str = "pingack", host: str = "localhost", port: int = 60001):
        self.type = type
        self.host = host
        self.port = port
        self.ping