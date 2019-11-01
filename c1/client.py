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

if __name__=='__main__':
    f: FileServer = get_fileserver_object()
    print(f.get_nameserver())
    print(f.list_peer())


    print(f.create('slide1.pdf'))
    print(f.list())

    print(f.create('slide2.pdf'))
    print(f.list())

    print(f.delete('slide1.pdf'))
    print(f.list())


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


