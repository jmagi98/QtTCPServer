import json
import sys
import time
import traceback

from PySide2 import QtCore
from PySide2 import QtNetwork
from PySide2 import QtWidgets
'''
Only supports one connection - multiple connections will cause it to be dropped

'''
class ServerBase(QtCore.QObject):
    PORT = 3002
    HEADER_SIZE = 10

    def __init__(self, parent):
        super(ServerBase, self).__init__(parent)
        self.port = self.__class__.PORT
        self.initialize()

    def initialize(self):
        print('hello world')
        self.server = QtNetwork.QTcpServer(self) 
        self.server.newConnection.connect(self.establish_connection)
        print('here')
        # check if server is successfully listening on our specified port
        if self.listen():
            print('Server is listening on port: ' + str(self.port))
        else:
            print('error, not listening')
        

    def listen(self):
        # Built in to QTTcpServer
        if not self.server.isListening():
            # returns if the server is listening or not as boolean
            return self.server.listen(QtNetwork.QHostAddress.LocalHost, self.port)
        return False

    def establish_connection(self):
        self.socket = self.server.nextPendingConnection()

        # check if the connection is made
        if self.socket.state() == QtNetwork.QTcpSocket.ConnectedState:
            # set up methods for connection
            self.socket.disconnected.connect(self.on_disconnect)
            self.socket.readyRead.connect(self.read)
            print('connection established')
            
    def on_disconnect(self):
        self.socket.disconnected.disconnect()
        self.socket.readyRead.disconnect()

        self.socket.deleteLater()
        print('Disconnected connection')

    def read(self):
        bytes_remaining = -1
        json_data = ''

        # built in method that returns boolean
        while self.socket.bytesAvailable():
            if bytes_remaining <= 0:
                byte_array = self.socket.read(ServerBase.HEADER_SIZE)
                bytes_remaining, valid = byte_array.toInt()
                if not valid:
                    bytes_remaining = -1
                    self.write_error("invalid header")

                    # purge unknown data
                    self.socket.readAll()

            # Body
            else:
                byte_array = self.socket.read(bytes_remaining)
                bytes_remaining -= len(byte_array)
                json_data += byte_array.data().decode()

                if bytes_remaining == 0:
                    bytes_remaining = -1
                    data = json.loads(json_data)

                    self.process_data(data)
                    json_data = ''


    def write(self, reply):
        print("here")
        json_data = json.dumps(reply)

        if self.socket.state() == QtNetwork.QTcpSocket.ConnectedState:
            header = "{0}".format(len(json_data.encode())).zfill(ServerBase.HEADER_SIZE)
            data = QtCore.QByteArray('{0}{1}'.format(header, json_data).encode())
            self.socket.write(data)
        else:
            print("Error: not still connected")

    def write_error(self, error_msg):
        reply = {
            'success': False,
            'msg': error_msg
        }

        self.write(reply)

    def process_data(self, data):
        reply = {
            'success': False
        }

        cmd = data['cmd']

        if cmd == 'ping':
            reply['success'] = True

        else:
            self.process_cmd(cmd, data, reply)
            if not reply['success']:
                reply['cmd'] = cmd
                if not 'msg' in reply.keys():
                    reply['msg'] = "Unkown Error"
        

        

        self.write(reply)
    def process_cmd(self, cmd, data, reply):

        reply['msg'] = "invalid command: {0}".format(cmd )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    window.setWindowTitle("Server Base")
    window.setFixedSize(240, 150)
    QtWidgets.QPlainTextEdit(window)
    server = ServerBase(window)
    window.show()
    app.exec_()


