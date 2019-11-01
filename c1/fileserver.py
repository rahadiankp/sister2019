import os
import Pyro4
import base64

class FileServer(object):
    PEERS = []
    NAMESERVER = ""
    PORT = ""
    ROOTDIR = ""

    def __init__(self):
        pass

    def create_return_message(self,kode='000',message='kosong',data=None):
        return dict(kode=kode,message=message,data=data)

    def list_peer(self):
        return self.create_return_message("200", FileServer.PEERS)

    def get_nameserver(self):
        return self.create_return_message("200", FileServer.NAMESERVER)

    def connect_proxy(self, instance_name):
        uri = "PYRONAME:{0}@{1}:{2}".format(instance_name, FileServer.NAMESERVER, FileServer.PORT)
        fserver = Pyro4.Proxy(uri)
        return fserver

    def execute_to_other_peers(self, command: str, data: dict = None):
        data["broadcast"] = False
        if command == "create":
            for peer in FileServer.PEERS:
                fs_object: FileServer = self.connect_proxy(peer)
                fs_object.create(**data)
        elif command == "delete":
            for peer in FileServer.PEERS:
                fs_object: FileServer = self.connect_proxy(peer)
                fs_object.delete(**data)
        elif command == "update":
            for peer in FileServer.PEERS:
                fs_object: FileServer = self.connect_proxy(peer)
                fs_object.update(**data)

    def list(self):
        print("list ops")
        try:
            daftarfile = []
            for x in os.listdir(FileServer.ROOTDIR):
                if x[0:4]=='FFF-':
                    daftarfile.append(x[4:])
            return self.create_return_message('200',daftarfile)
        except:
            return self.create_return_message('500','Error')

    def create(self, name: str, broadcast: bool = True):
        nama = 'FFF-{}' . format(name)
        print("create ops {}" . format(nama))
        try:
            if os.path.exists(FileServer.ROOTDIR+nama):
                return self.create_return_message('102', 'OK','File Exists')
            f = open(FileServer.ROOTDIR+nama,'wb',buffering=0)
            f.close()
            if broadcast:
                self.execute_to_other_peers("create", {"name": name})
            return self.create_return_message('200','OK')
        except:
            return self.create_return_message('500','Error')

    def read(self,name='filename000'):
        nama='FFF-{}' . format(name)
        print("read ops {}" . format(nama))
        try:
            f = open(nama,'r+b')
            contents = f.read().decode()
            f.close()
            return self.create_return_message('101','OK',contents)
        except:
            return self.create_return_message('500','Error')

    def update(self, name, content, broadcast: bool = True):
        nama = 'FFF-{}'.format(name)
        print("update ops {}".format(nama))

        if str(type(content)) == "<class 'dict'>":
            content = content['data']

        try:
            f = open(FileServer.ROOTDIR+nama, 'w+b')
            f.write(content.encode())
            f.close()
            if broadcast:
                self.execute_to_other_peers("update", {"name": name, "content": content})
            return self.create_return_message('101', 'OK')
        except Exception as e:
            return self.create_return_message('500', 'Error', str(e))

    def delete(self, name: str, broadcast: bool = True):
        nama='FFF-{}' . format(name)
        print("delete ops {}" . format(nama))

        try:
            os.remove(FileServer.ROOTDIR+nama)
            if broadcast:
                self.execute_to_other_peers("delete", {"name": name})
            return self.create_return_message('101','OK')
        except:
            return self.create_return_message('500','Error')



if __name__ == '__main__':
    k = FileServer()
    print(k.create('f1'))
    print(k.update('f1',content='wedusku'))
    print(k.read('f1'))
#    print(k.create('f2'))
#    print(k.update('f2',content='wedusmu'))
#    print(k.read('f2'))
    print(k.list())
    #print(k.delete('f1'))

