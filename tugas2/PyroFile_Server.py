from PyroFile import FileManager
import Pyro4
import sys
import getopt


def write_uri_to_file(uri: str):
    with open("pyro_host", "w") as fd:
        fd.write(uri)


def start_server(directory: str, with_ns=False, ns_host="localhost", ns_port=6969, name="pyrofileserver"):
    print("Using directory:", directory)
    daemon = Pyro4.Daemon(host=ns_host)
    FileManager.DIRECTORY_PATH = directory
    uri = daemon.register(FileManager)

    if with_ns:
        print("Using Pyro Nameserver...")
        ns = Pyro4.locateNS(ns_host, ns_port)
        ns.register(name, uri)
    write_uri_to_file(uri.asString())

    print("OK PyroFile URI:", uri)
    daemon.requestLoop()


if __name__ == "__main__":
    WITH_NS = False
    DIRECTORY_PATH = "/var/pyrofileserver"
    NAME = "pyrofileserver"
    HOST = "localhost"
    PORT = 6969

    options, misc = getopt.getopt(sys.argv[1:], "d:wnhp", ["dpath=",
                                                           "withns",
                                                           "name=",
                                                           "host=",
                                                           "port=",
                                                           "help"])

    for opt, val in options:
        if opt == "--help":
            print("Usage: python PyroFile_Server.py options")
            print("Options:")
            print("-d, --dpath=path\tRequired. Root directory to use. Default to /var/pyrofileserver")
            print("-w, --withns\tUse Pyro Nameserver")
            print("-n, --name=name\tUse Pyro Nameserver naming. Default to pyrofileserver")
            print("-h, --host=host\tUse Pyro Nameserver host. Default to localhost")
            print("-p, --port=port\tUse Pyro Nameserver port. Default to 6969")
            print("--help\tPrint this information")
            sys.exit(0)
        elif opt in ["-w", "--withns"]:
            WITH_NS = True
        elif opt in ["-n", "--name"]:
            NAME = val
        elif opt in ["-h", "--host"]:
            HOST = val
        elif opt in ["-p", "--port"]:
            PORT = int(val)

    if WITH_NS:
        start_server(DIRECTORY_PATH, WITH_NS, HOST, PORT, NAME)
    else:
        start_server(DIRECTORY_PATH)
