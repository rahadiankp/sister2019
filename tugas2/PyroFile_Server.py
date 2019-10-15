from PyroFile import FileManager
from FailureDetection import PingAck, Heartbeat
from FailureDetection_Client import PingAckClient, HeartbeatClient
import Pyro4
import sys
import random
import string
import getopt
import threading
import time


def write_uri_to_file(uri: str) -> None:
    with open("pyro_host", "w") as fd:
        fd.write(uri)


def write_uri_failure_detector(id: str, fd_type: str, uri_failure_detection = None, append = False):
    if uri_failure_detection:
        type = fd_type.split("_")[0]
        if append:
            with open("failure_detection_host", "a+") as fd:
                fd.write(type + " " + id + " " + uri_failure_detection.asString() + "\n")
        else:
            with open("failure_detection_host", "w") as fd:
                fd.write(type + " " + id + " " + uri_failure_detection.asString() + "\n")


class FailureDetectionHostReload(threading.Thread):
    def __init__(self, id: str, id_list: list):
        self.id = id
        self.id_list = id_list
        threading.Thread.__init__(self)

    def run(self) -> None:
        print("Host reloader active")
        while True:
            time.sleep(2)
            with open("failure_detection_host", "r") as fd_detail:
                for line in fd_detail.readlines():
                    type, fd_id, fd_uri = line.split()
                    fd_conn = make_fd_connection(fd_uri)
                    if type == "alltoall" and not fd_id in self.id_list:
                        fd_client_thread = HeartbeatClient(fd_conn, self.id, 5)
                        fd_client_thread.start()
                        self.id_list.append(fd_id)


def start_server(directory: str, fd_type: str = None, with_ns=False, ns_host="localhost", ns_port=6969, name="pyrofileserver"):
    id = randomString()
    print("Server ID:", id)
    print("Using directory:", directory)
    daemon = Pyro4.Daemon(host=ns_host)
    FileManager.DIRECTORY_PATH = directory
    uri = daemon.register(FileManager)

    # failure detection server
    uri_failure_detection = None
    if fd_type == "pingack_server":
        uri_failure_detection = daemon.register(PingAck)
        write_uri_failure_detector(id, fd_type, uri_failure_detection)
    if fd_type == "heartbeat_server":
        Heartbeat.callback = heartbeat_callback
        uri_failure_detection = daemon.register(Heartbeat)
        write_uri_failure_detector(id, fd_type, uri_failure_detection)
    if fd_type == "alltoall":
        Heartbeat.callback = heartbeat_callback
        uri_failure_detection = daemon.register(Heartbeat)
        write_uri_failure_detector(id, fd_type, uri_failure_detection, append=True)

    if with_ns:
        print("Using Pyro Nameserver...")
        ns = Pyro4.locateNS(ns_host, ns_port)
        ns.register(name, uri)
    write_uri_to_file(uri.asString())

    # failure detection client
    id_list = [id]
    if fd_type:
        with open("failure_detection_host", "r") as fd_detail:
            for line in fd_detail.readlines():
                type, fd_id, fd_uri = line.split()
                fd_conn = make_fd_connection(fd_uri)
                if type == "pingack":
                    fd_client_thread = PingAckClient(fd_conn, 5)
                    fd_client_thread.start()
                    break
                if type == "heartbeat":
                    fd_client_thread = HeartbeatClient(fd_conn, id, 5)
                    fd_client_thread.start()
                    break
                if type == "alltoall" and fd_id not in id_list:
                    fd_client_thread = HeartbeatClient(fd_conn, id, 5)
                    fd_client_thread.start()
                    id_list.append(fd_id)

    if fd_type == "alltoall":
        reload = FailureDetectionHostReload(id, id_list)
        reload.start()

    print("PyroFile URI:", uri)
    print("FailureDetection URI:", uri_failure_detection)
    print("URI with NS:", "PYRONAME:"+name+"@"+ns_host+":"+str(ns_port))
    daemon.requestLoop()


def make_fd_connection(uri: str) -> Pyro4.core.Proxy:
    return Pyro4.Proxy(uri)


def heartbeat_callback(id, seqno):
    print(id, seqno)


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


if __name__ == "__main__":
    WITH_NS = False
    DIRECTORY_PATH = ""
    NAME = "pyrofileserver"
    HOST = "localhost"
    PORT = 6969
    FD_TYPE = None

    options, misc = getopt.getopt(sys.argv[1:], "d:wn:h:p:f:",
                                  ["dpath=", "withns", "name=", "host=", "port=", "fd_type=", "help"])

    for opt, val in options:
        if opt == "--help":
            print("Usage: python PyroFile_Server.py options")
            print("Options:")
            print("-d, --dpath=path\tRequired. Root directory to use")
            print("-w, --withns\tUse Pyro Nameserver")
            print("-n, --name=name\tUse Pyro Nameserver naming. Default to 'pyrofileserver'")
            print("-h, --host=host\tUse Pyro Nameserver host. Default to 'localhost'")
            print("-p, --port=port\tUse Pyro Nameserver port. Default to 6969")
            print("--help\tPrint this information")
            sys.exit(0)
        elif opt in ["-d", "--dpath"]:
            DIRECTORY_PATH = val
        elif opt in ["-w", "--withns"]:
            WITH_NS = True
        elif opt in ["-n", "--name"]:
            NAME = val
        elif opt in ["-h", "--host"]:
            HOST = val
        elif opt in ["-p", "--port"]:
            PORT = int(val)
        elif opt in ["-f", "--fd_type"]:
            FD_TYPE = val

    if DIRECTORY_PATH == "":
        print("Directory Path is not set. Use -d or --dpath to set")
        sys.exit(0)

    if WITH_NS:
        start_server(DIRECTORY_PATH, FD_TYPE, WITH_NS, HOST, PORT, NAME)
    else:
        start_server(DIRECTORY_PATH, FD_TYPE)
