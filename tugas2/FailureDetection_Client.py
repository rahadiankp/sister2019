from FailureDetection import PingAck, Heartbeat
import Pyro4
import threading
import time


class PingAckClient(threading.Thread):
    def __init__(self, server: PingAck, period: int) -> None:
        self.server: PingAck = server
        self.period = period
        threading.Thread.__init__(self)

        self.alive = True

    def run(self) -> None:
        last_recvd_ack = int(time.time())
        try:
            while True:
                self.server.ping()
                now = int(time.time())
                if now-last_recvd_ack >= 2*self.period:
                    print("Peer is down. Ping too long to respond")
                    self.alive = False
                    return
                last_recvd_ack = now
                time.sleep(self.period)
        except Pyro4.errors.ConnectionClosedError:
            print("Peer is down")
            self.alive = False
            return


class CentralizedHeartbeatClient(threading.Thread):
    def __init__(self, server: Heartbeat, period: int):
        self.server: Heartbeat = server
        self.period = period
        threading.Thread.__init__(self)

        self.seqno = 1

        self.alive = True

    def run(self) -> None:
        try:
            while True:
                print(self.server.knock(self.seqno))
                self.seqno += 1
                time.sleep(self.period)
        except Pyro4.errors.ConnectionClosedError:
            print("Peer is down")
            self.alive = False
            return