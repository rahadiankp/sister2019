from PyroFile import FileManager
import Pyro4
import sys


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
    if len(sys.argv) < 2:
        print("Usage: python PyroFile_Server.py DIRPATH")
        print("DIRPATH\tRoot directory to expose")
        sys.exit(0)
    DIRECTORY_PATH = sys.argv[1]
    start_server(DIRECTORY_PATH)
