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
    callback = None

    def __init__(self, period: int = 3):
        self.server_list = dict()
        self.last_seqno = 0
        self.status = True
        self.time_last_knock = 0
        self.period = period

    def knock(self, id: str, seqno: int) -> int:
        if id not in self.server_list:
            self.server_list[id] = 0
        # print(id, ":", self.server_list[id], 'to', seqno)
        self.server_list[id] = seqno
        if Heartbeat.callback:
            Heartbeat.callback(id, seqno)
        now = int(time.time())
        if now-self.time_last_knock >= 3*self.period:
            pass
        self.time_last_knock = int(time.time())
        return seqno

