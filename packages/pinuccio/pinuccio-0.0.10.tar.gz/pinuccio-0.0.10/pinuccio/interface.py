import struct
from sys import getsizeof


"""
PACKET STRUCTURE

1Byte + NByte + CByte
  N   +   C   + data

Max N value = (2^8) = 256
Max N value = (2^(256*8)) = (2^(2048))
Max data byte = (2^(2048))

"""


BYTES_OBJECT_OVERHEAD = getsizeof(b"")

types = {
    "<B":1,
    "<H":2,
    "<L":4,
    "<Q":8
}




class msg_send_Exception(Exception):
    def __init__(self, message="Error"):
        super().__init__(message)

class msg_recv_Exception(Exception):
    def __init__(self, message="Error"):
        super().__init__(message)


def msg_recv(socket):
    N = recvNBytes(socket, 1)
    N = struct.unpack('<B', N)[0]

    if N != 0:
        C = recvNBytes(socket, N)
        for t in types:
            if types[t] == N:
                C = struct.unpack(t, C)[0]
        
        if C != 0:
            data = recvNBytes(socket, C)
            data = data.decode('utf-8')
        else:
            raise msg_recv_Exception("Error reciving C")
    
    else:
        raise msg_recv_Exception("Error reciving N")
    
    return data


def msg_send(socket, data):
    if type(data) is not str:
        raise msg_send_Exception("'data' must be string")
    if data == "":
        raise msg_send_Exception("'data' must not be empty")

    data = data.encode("utf-8")
    C = int(len(data))
    N = (C.bit_length()+7)//8

    if N>8:
        raise msg_send_Exception("Message too long")

    for t in types:
        if N<=types[t]:
            socket.sendall(struct.pack('<B', types[t]))
            socket.sendall(struct.pack(t, C))
            socket.sendall(data)
            return

    raise msg_send_Exception("Error in msg_send")
    

def recvNBytes(socket, N):
    data = socket.recv(N)
    checkRecvData(data)
    while getsizeof(data)-BYTES_OBJECT_OVERHEAD!=N:
        newData = socket.recv(N-getsizeof(data)+BYTES_OBJECT_OVERHEAD)
        checkRecvData(data)
        data += newData
    return data


def checkRecvData(data):
    if data == b"":
        raise msg_recv_Exception("Socket closed")



def msg_encode(data, key):
    pass

def msg_decode(data, key):
    pass

