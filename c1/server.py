from c1.fileserver import FileServer
import threading
import Pyro4
import sys
import time
import os

namainstance = sys.argv[1]


def start_without_ns():
    daemon = Pyro4.Daemon()
    file_server = Pyro4.expose(FileServer)
    uri = daemon.register(file_server)
    print("my URI : ", uri)
    daemon.requestLoop()


def start_with_ns(peers: list, nameserver: str = "localhost", port: int = 7777):
    # name server harus di start dulu dengan  pyro4-ns -n localhost -p 7777
    # gunakan URI untuk referensi name server yang akan digunakan
    # untuk mengetahui instance apa saja yang aktif gunakan pyro4-nsc -n localhost -p 7777 list

    try:
        os.mkdir(namainstance)
    except FileExistsError:
        pass

    daemon = Pyro4.Daemon(host=nameserver)
    ns = Pyro4.locateNS(nameserver, port)
    FileServer.PEERS = peers
    FileServer.NAMESERVER = nameserver
    FileServer.PORT = str(port)
    FileServer.ROOTDIR = namainstance + "/"
    x_FileServer = Pyro4.expose(FileServer)
    print(type(ns))
    uri_fileserver = daemon.register(x_FileServer)
    ns.register("{}" . format(namainstance), uri_fileserver)

    # add ins to peer list
    with open("instance_hosts", "a+") as f:
        f.writelines(namainstance+"\n")

    # new thread for PeerSearch
    ps = PeerSearch(namainstance, peers)
    ps.start()

    daemon.requestLoop()
    ps.kill()
    ps.join()
    print("Removing", namainstance, "from NS")
    ns.remove("{}".format(namainstance))


class PeerSearch(threading.Thread):
    def __init__(self, instance_name:str, peer_list: list):
        self.alive = True
        self.peer_list = peer_list
        self.instance_name = instance_name
        threading.Thread.__init__(self)

    def run(self) -> None:
        while self.alive:
            with open("instance_hosts", "r") as f:
                for ins in f.readlines():
                    if ins.strip("\n") not in self.peer_list and ins.strip("\n") != self.instance_name:
                        self.peer_list.append(ins.strip("\n"))
            print(self.peer_list)
            time.sleep(2)

    def kill(self):
        self.alive = False


if __name__ == '__main__':
    peers = []
    start_with_ns(peers)
