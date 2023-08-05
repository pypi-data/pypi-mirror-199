from . import utils
from . import interface as sc
import socket, json


class Client():
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))


    def send(self, data, key=None):
        """return True if message was sent without errors else False"""
        if self.socket:
            try:
                data = json.dumps(data)
                utils.info("send:", data)
                sc.msg_send(self.socket, data)
                return True
            except TypeError:
                utils.error(data,"json Encode Error")
                return False
        return False

    def recv(self, key=None):
        """return None if socket is closed else return readed data"""
        if self.socket:
            try:
                data = sc.msg_recv(self.socket)
                utils.info("recv:", data)
            except Exception as e:
                utils.error(e,"Socket Error")
                self.close()
                return None
        
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                utils.error("Error", data,"json Decode Error")
                return self.recv(self.socket, key)
            return data
        return None
    

    #Actions
    def close(self):
        if self.socket:
            try:
                self.send({"action":"close"})
                self.socket.close()
            finally:
                self.socket = None

    def subscribe(self, name=""):
        if self.socket:
            if name=="":
                return self.send({"action":"subscribe"})
            else:
                return self.send({"action":"subscribe", "name":name})
        return False

    def getClients(self):
        if self.socket:
            return self.send({"action":"getClients"})
        return False
