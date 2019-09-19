from PyroFile import FileManager
import Pyro4

def write_uri_to_file(uri: str):
    with open("pyro_host", "w") as fd:
        fd.write(uri)

def server_without_nameserver():
    daemon = Pyro4.Daemon()
    pyrofile_server = Pyro4.expose(FileManager)
    uri = daemon.register(pyrofile_server)
    print("PyroFile URI:", uri)
    write_uri_to_file(uri.asString())
    daemon.requestLoop()


if __name__ == "__main__":
    server_without_nameserver()