import Pyro4
import Pyro4.errors
import serpent
import sys
import getopt


class PyroFileClient(object):
    def __init__(self, uri):
        print("Trying to connect to", uri)
        self.remote = self.make_connection(uri)
        # check connection
        try:
            self.remote.get_cwd()
            print("Connecting to PyroFile OK\n")
        except Pyro4.errors.CommunicationError:
            print("Connecting to PyroFile FAILED. Exiting")
            sys.exit(0)

        # start client
        self.main()

    def make_connection(self, uri) -> Pyro4.core.Proxy:
        pyrofile_server = Pyro4.Proxy(uri)
        return pyrofile_server

    def main(self):
        print("PyroFile - RKP - SISTER 2019")
        print("Type 'help' for more information")
        try:
            while True:
                command = input(">  ")
                if command == "":
                    continue
                args = command.split()

                if args[0] == "ls":
                    self.get_listdir()
                elif args[0] == "cat":
                    if len(args) == 1:
                        print("cat requires 1 additional argument")
                        continue
                    self.read_file(args[1])
                elif args[0] == "touch":
                    if len(args) == 1:
                        print("touch requires 1 or more additional arguments")
                        continue
                    self.create_file(args[1:])
                elif args[0] == "rm":
                    if len(args) == 1:
                        print("rm requires 1 or more additional arguments")
                        continue
                    self.delete_file(args[1:])
                elif args[0] == "nano":
                    if len(args) == 1:
                        print("nano requires 1 additional argument")
                        continue
                    self.update_file(args[1])
                elif args[0] == "exit":
                    print("Exiting. Goodbye.")
                    return
                elif args[0] == "help":
                    print("Available commands:")
                    print("ls\t\t\tShow directory listing")
                    print("cat FILE\t\tRead a FILE")
                    print("touch FILE1 [FILE2] ...\tCreate new blank file(s)")
                    print("rm FILE1 [FILE2] ...\tDelete file(s). Support globing")
                    print("nano FILE\t\tEdit a FILE. Will overwrite content entirely")
                    print("help\t\t\tPrint this information")
                    print("exit\t\t\tExit this prompt")
                else:
                    print("Unknown command")
        except KeyboardInterrupt:
            print("\nExiting. Goodbye.")
            return

    def get_listdir(self):
        file_list = self.remote.get_listdir()
        if not file_list:
            print("Directory is empty")
            return
        print("File List:")
        print("   Name (Length)")
        for (filename, size) in file_list:
            print("->", filename, "("+str(size)+" bytes)")

    def create_file(self, filenames: list):
        for filename in filenames:
            status, message = self.remote.create_file(filename)
            if status:
                print(message)
            else:
                print("Error occurred:", message)

    def read_file(self, filename):
        status, recv_filename, size, content = self.remote.read_file(filename)
        content = serpent.tobytes(content)
        if status:
            print("Opening file", filename, "("+str(size)+") :")
            print(content.decode("utf-8"))
        else:
            print(recv_filename)

    def update_file(self, filename):
        content = ""
        # start inserting content
        print("Insert content to update file:", filename, "Press CTRL+C to finish and save")
        try:
            while True:
                tmp = input()
                tmp += "\n"
                content += tmp
        except KeyboardInterrupt:
            print("\nSaving content to file")
        status, message, write_size = \
            self.remote.update_file(filename, content.encode("utf-8"), len(content.encode("utf-8")))
        if status:
            print(message, write_size, "bytes written\n")
        else:
            print(message, "\n")

    def delete_file(self, filenames: list):
        for filename in filenames:
            status, message = self.remote.delete_file(filename)
            if status:
                print(message)
            else:
                print("Error occurred:", message)


if __name__ == '__main__':
    uri = ""
    if len(sys.argv) == 1:
        try:
            with open("pyro_host", "r") as fd:
                uri = fd.readline()
        except FileNotFoundError:
            print("Could not find pyro_host file. Please manually specify host")
            sys.exit(0)
    else:
        options, misc = getopt.getopt(sys.argv[1:], "h:", ["host=", "help"])
        for opt, val in options:
            if opt == "--help":
                print("Usage: python Pyrofile_Client.py [HOST]")
                print("Options and arguments:")
                print("-h, --host=uri\tHost to use. If not specified, automatically use host in pyro_host file")
                print("--help\t\tPrint this information")
                sys.exit(0)
            elif opt in ["-h", "--host"]:
                uri = val
    client = PyroFileClient(uri)
