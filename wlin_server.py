import socket
import threading
import json



class WLinServer:
    def __init__(self):
        print('서버 준비완료')
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.bind(('0.0.0.0', 45770))
        self.sk.listen(10)
        self._t = threading.Thread(target=self.server_listener)
        self._t.start()
        self.wl_client_list = []

    def server_listener(self):
        while True:
            c, addr = self.sk.accept()
            print(addr)
            ret = c.recv(1024)
            if ret is None:
                c.send("err".encode())
                continue
            ret = ret.decode()
            try:
                jobj = json.loads(ret)
                if jobj['type'] == 'client_hello':
                    name = jobj['name']
                    self.wl_client_list.append(WLinClient(c, addr, name, self))
                else:
                    raise Exception
            except:
                c.send("err".encode())

class WLinClient:
    def __init__(self, sock: socket.socket, addr, name, server: WLinServer):
        self.addr = addr
        self.name = name
        self.sock = sock
        self.server = server
        sock.send("ok".encode())

    def get_cpu_stat(self):
        self.sock.send('{"type": "request", "req": "cpu"}'.encode())
        ret = self.sock.recv(4096)
        if ret is None:
            self.server.wl_client_list.remove(self)
        return json.loads(ret)

    def get_proc_stat(self):
        self.sock.send('{"type": "request", "req": "proc"}'.encode())
        ret = self.sock.recv(4096)
        if ret is None:
            self.server.wl_client_list.remove(self)
        return json.loads(ret)

    def get_name_stat(self):
        self.sock.send('{"type": "request", "req": "name"}'.encode())
        ret = self.sock.recv(4096)
        if ret is None:
            self.server.wl_client_list.remove(self)
        return json.loads(ret)

    def get_mem_stat(self):
        self.sock.send('{"type": "request", "req": "mem"}'.encode())
        ret = self.sock.recv(4096)
        if ret is None:
            self.server.wl_client_list.remove(self)
        return json.loads(ret)
