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
        pass
    def write(self):
        pass
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    window.setWindowTitle("Server Base")
    window.setFixedSize(240, 150)
    QtWidgets.QPlainTextEdit(window)
    server = ServerBase(window)
    window.show()
    app.exec_()


