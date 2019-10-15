from PyroFile import FileManager
from FailureDetection import PingAck, Heartbeat
from FailureDetection_Client import PingAckClient, CentralizedHeartbeatClient
import Pyro4
import sys
import getopt


def write_uri_to_file(uri: str, uri_failure_detection = None) -> None:
    with open("pyro_host", "w") as fd:
        fd.write(uri)
    if uri_failure_detection:
        with open("failure_detection_host", "w") as fd:
            fd.write(uri_failure_detection.asString())


def start_server(directory: str, fd_type: str = None, with_ns=False, ns_host="localhost", ns_port=6969, name="pyrofileserver"):
    print("Using directory:", directory)
    daemon = Pyro4.Daemon(host=ns_host)
    FileManager.DIRECTORY_PATH = directory
    uri = daemon.register(FileManager)

    # failure detection server
    uri_failure_detection = None
    if fd_type == "pingack_server":
        uri_failure_detection = daemon.register(PingAck)
    if fd_type == "heartbeat_server":
        Heartbeat.callback = heartbeat_callback
        uri_failure_detection = daemon.register(Heartbeat)
        print(uri_failure_detection.object)

    if with_ns:
        print("Using Pyro Nameserver...")
        ns = Pyro4.locateNS(ns_host, ns_port)
        ns.register(name, uri)
    write_uri_to_file(uri.asString(), uri_failure_detection)

    # failure detection client
    with open("failure_detection_host", "r") as fd_detail:
        fd_uri = fd_detail.readline()
        fd_conn = make_fd_connection(fd_uri)
        if fd_type == "pingack_client":
            fd_client_thread = PingAckClient(fd_conn, 5)
            fd_client_thread.start()
        if fd_type == "heartbeat_client":
            fd_client_thread = CentralizedHeartbeatClient(fd_conn, 5)
            fd_client_thread.start()

    print("PyroFile URI:", uri)
    print("FailureDetection URI:", uri_failure_detection)
    print("URI with NS:", "PYRONAME:"+name+"@"+ns_host+":"+str(ns_port))
    daemon.requestLoop()


def make_fd_connection(uri: str) -> Pyro4.core.Proxy:
    return Pyro4.Proxy(uri)

def heartbeat_callback(id, seqno):
    print(id, seqno)


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
