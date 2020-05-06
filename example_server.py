import json
import sys
import time
import traceback

from PySide2 import QtCore
from PySide2 import QtNetwork
from PySide2 import QtWidgets

from server_base import ServerBase

class ExampleServer(ServerBase):

    PORT = 3000

    def __init__(self, parent_window):
        super(ExampleServer, self).__init__(parent_window)

        self.window = parent_window

    def process_cmd(self, cmd, data, reply):    
        print('overriden')
        if cmd == 'echo':
            self.echo(data, reply)
        elif cmd == 'setTitle':
            self.setTitle(data, reply)
        elif cmd == 'sleep':
            self.sleep(data, reply)
        
        else:
            super(ExampleServer, self).process_cmd(cmd, data, reply)


    def echo(self, data, reply):
        reply['result'] = data['text']
        reply['success'] = True
        print(reply)

    def setTitle(self, data, reply):
        self.window.setWindowTitle(data['title']) 
        reply['result'] = True 
        reply['success'] = True


    def sleep(self, data, reply):
        for i in range(6):
            print('sleeping: ' + str(i))
            time.sleep(1)

        reply['result'] = True
        reply['success'] = True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    window.setWindowTitle("Server Base")
    window.setFixedSize(240, 150)
    QtWidgets.QPlainTextEdit(window)
    server = ExampleServer(window)
    window.show()
    app.exec_()