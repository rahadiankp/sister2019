from Pyro4 import expose
import time


@expose
class PingAck(object):
    def __init__(self):
        pass

    def ping(self) -> str:
        return "PONG"


@expose
class Heartbeat(object):
    def __init__(self, t: int = 3):
        self.seqno = 4
        self.status = True
        self.time_last_knock = 0

    def knock(self, seqno: int) -> int:
        print(self.seqno)
        self.seqno = seqno
        self.time_last_knock = int(time.time())
        return seqno

