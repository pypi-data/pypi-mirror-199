import socket, json
from . import utils
from . import interface as sc
from .SThread import SThread
import uuid

notAllowedNames = ['', 'all']

class Server():
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.socket = None
        self.connected_clients = {}

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()
        self.server_loop()

    
    def send(self, connection, data, to="None", key=None):
        """return True if message was sent without errors else False"""
        if self.socket:
            try:
                data = json.dumps(data)
                utils.info("send:", data, "| to:", to)
                sc.msg_send(connection, data)
                return True
            except TypeError:
                utils.error(data,"json Encode Error")
                return False
        return False
        
    def recv(self, connection, key=None):
        """return None if socket is closed else return readed data"""
        if self.socket:
            try:
                data = sc.msg_recv(connection)
                utils.info("recv:", data)
            except Exception as e:
                utils.error(e,"Socket Error")
                return None
        
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                utils.error("Error", data,"json Decode Error")
                return self.recv(connection, key)
            return data
        return None
    

    def server_loop(self):
        while True:
            conn, addr = self.socket.accept()
            client_thread = SThread(target=self.client_startup)
            client_thread._args=(conn, client_thread)
            client_thread.start()

    def client_startup(self, conn, thread):
        data = self.recv(conn)
        if data is None:
            return
        if not self.actionCheck(conn, data):
            self.closeSocket(conn)
            return

        if data["action"] == "subscribe":
            self.subscribeAction(conn, data, thread)
            utils.info("clients:", list(self.connected_clients.keys()))
        else:
            self.sendStatus(conn, 458)
            self.closeSocket(conn)
            return
    
    def handle(self, conn, name):
        while True:
            data = self.recv(conn)
            if data is None:
                self.removeClient(name)
                return
            if not self.actionCheck(conn, data):
                self.removeClient(name)
                return

            if data["action"] == "send":
                self.sendAction(conn, data, name)
            
            elif data["action"] == "getClients":
                self.getClientsAction(conn)
            
            elif data["action"] == "close":
                self.closeAction(conn, name)
                return
            
            else:
                self.unknownAction(conn, name)


    def actionCheck(self, conn, data, to="None"):
        if type(data) is not dict:
            self.sendStatus(conn, 451, to)
            return False
        if "action" not in data:
            self.sendStatus(conn, 452, to)
            return False
        return True

    def closeSocket(self, conn):
        if conn:
            conn.close()
    
    def removeClient(self, name):
        if name in self.connected_clients:
            self.closeSocket(self.connected_clients[name][0])
            del self.connected_clients[name]
            utils.info("client",name,"disconnected")

    def stopThread(self, name):
        if name in self.connected_clients:
            thread = self.connected_clients[name][1]
            del self.connected_clients[name]
            thread.stop()
    

    def subscribeAction(self, conn, data, thread):
        client_name = None
        if "name" in data:
            client_name = data["name"]
            if client_name in self.connected_clients:
                self.sendStatus(conn, 454)
                return
            if client_name in notAllowedNames:
                self.sendStatus(conn, 453)
                return
        else:
            client_name = str(uuid.uuid4())
            while client_name in self.connected_clients:
                client_name = str(uuid.uuid4())

        self.connected_clients[client_name] = ([conn, thread])
        utils.info("client",client_name,"connected")
        utils.info("clients:", list(self.connected_clients.keys()))
        self.sendStatus(conn, 200, client_name)
        self.send(conn, {'action':'subscribeName', 'subscribeName':client_name}, client_name)
        self.handle(conn, client_name)
    
    def closeAction(self, name):
        self.removeClient(name)

    def getClientsAction(self, conn, name="None"):
        clients_name = list(self.connected_clients.keys())
        self.send(conn, {'action':'clientsList', 'clients':clients_name}, name)

    def sendAction(self, conn, data, name):
        if "to" in data:
            dst_client = data["to"]
            if dst_client in self.connected_clients:
                if "msg" in data:
                    self.send(self.connected_clients[dst_client][0], {'action':'msg', 'msg':data['msg'], 'from':name}, dst_client)
                    self.sendStatus(conn, 200, name)
                else:
                    self.sendStatus(conn, 457, name)
            elif dst_client=="all":
                if "msg" in data:
                    for client in self.connected_clients:
                        if client != name:
                            self.send(self.connected_clients[client][0], {'action':'msg', 'msg':data['msg'], 'from':name}, client)
                    self.sendStatus(conn, 200, name)
            else:
                self.sendStatus(conn, 456, name)
        else:
            self.sendStatus(conn, 455, name)

    def unknownAction(self, conn, name="None"):
        self.sendStatus(conn, 459, name)


    def sendStatus(self, conn, status, to="None"):
        self.send(conn, {'action':'status', 'status':status}, to)


