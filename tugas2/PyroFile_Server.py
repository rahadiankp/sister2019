from PyroFile import FileManager
import Pyro4
import sys


def write_uri_to_file(uri: str):
    with open("pyro_host", "w") as fd:
        fd.write(uri)


def server_without_nameserver(directory: str):
    daemon = Pyro4.Daemon()
    print("Using directory:", directory)
    FileManager.DIRECTORY_PATH = directory
    uri = daemon.register(FileManager)
    print("PyroFile URI:", uri)
    write_uri_to_file(uri.asString())
    daemon.requestLoop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python PyroFile_Server.py DIRPATH")
        print("DIRPATH\tRoot directory to expose")
        sys.exit(0)
    DIRECTORY_PATH = sys.argv[1]
    server_without_nameserver(DIRECTORY_PATH)
