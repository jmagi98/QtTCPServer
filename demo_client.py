import json
import socket
import time
import traceback

class ClientBase(object):
    PORT = 3002
    HEADER_SIZE = 10

    def __init__(self, timeout=2):
        self.timeout = timeout
        self.port = self.__class__.PORT
        self.discard_count = 0

    
    def connect(self, port = -1):
        if port >= 0:
            self.port = port
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", self.port))
        except:
            traceback.print_exc()
            return False
        return True


    def disconnect(self):
        try:
            self.client_socket.close()
        except:
            traceback.print_exc()
            return False
        return True


if __name__ == '__main__':
    client = ClientBase()
    if client.connect():
        print('client connected')
        
        if client.disconnect():
            print('client disconnected')
    else:
        print('error connecting')
