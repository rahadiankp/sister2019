from PyroFile import FileManager
import Pyro4


def server_without_nameserver():
    daemon = Pyro4.Daemon()
    pyrofile_server = Pyro4.expose(FileManager)
    uri = daemon.register(pyrofile_server)
    print("PyroFile URI:", uri)
    daemon.requestLoop()


if __name__ == "__main__":
    server_without_nameserver()