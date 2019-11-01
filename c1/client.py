from c1.fileserver import FileServer
import Pyro4
import base64
import json
import sys

namainstance = sys.argv[1] or "fileserver"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    print(uri)
    fserver = Pyro4.Proxy(uri)
    return fserver


if __name__ == '__main__':
    f: FileServer = get_fileserver_object()

    try:
        while True:
            command = input("> ")
            cmd, params = command.split()[0], command.split()[1:]

            if cmd == "create":
                print(f.create(params[0]))
            elif cmd == "list":
                print(f.list())
            elif cmd == "delete":
                print(f.delete(params[0]))
            elif cmd == "peers":
                print(f.list_peer())
            elif cmd == "nameserver":
                print(f.get_nameserver())
            elif cmd == "update":
                print(f.update(params[0], params[1].encode()))
            elif cmd == "read":
                print(f.read(params[0]))
            else:
                pass
    except KeyboardInterrupt:
        print("Exit")

    #
    # f.create('slide2.pptx')
    # f.update('slide2.pptx', content = open('slide2.pptx','rb+').read())
    #
    # d = f.read('slide1.pdf')
    # #kembalikan ke bentuk semula ke dalam file name slide1-kembali.pdf
    # open('slide1-kembali.pdf','w+b').write(base64.b64decode(d['data']))
    #
    # k = f.read('slide2.pptx')
    # #kembalikan ke bentuk semula ke dalam file name slide2-kembali.pptx
    # open('slide2-kembali.pptx','w+b').write(base64.b64decode(k['data']))


