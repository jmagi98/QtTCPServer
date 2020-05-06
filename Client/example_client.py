import json
import socket
import time
import traceback

from client_base import ClientBase

class ExampleClient(ClientBase):
    PORT = 3000

    def echo(self, text):
        cmd = {
            'cmd': 'echo',
            'text': text
        }

        reply = self.send(cmd)

        if self.isValidReply(reply):
            return reply['result']
        else:
            return None
    
    def setTitle(self, title):
        cmd = {
            "cmd": "setTitle",
            "title": title
        }

        reply = self.send(cmd) 
        if self.isValidReply(reply):
            return reply['result']
        else:
            return None

    # Used to show the shortcomings of using this singular client-server architecture
    def sleep(self):
        cmd = {
            "cmd": "sleep",
        }

        reply = self.send(cmd) 
        if self.isValidReply(reply):
            return reply['result']
        else:
            return None
    


if __name__ == '__main__':
    client = ExampleClient(timeout=10)
    if client.connect():
        print('client connected')
        
        print(client.echo('hello world'))
        print(client.setTitle("New Title"))
        print(client.sleep())
        

        if client.disconnect():
            print('client disconnected')
    else:
        print('error connecting')
