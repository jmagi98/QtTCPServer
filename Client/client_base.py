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
            self.client_socket.setblocking(0)
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
    def send(self, cmd):
        json_cmd = json.dumps(cmd)
        message = []
        # header
        message.append('{0:10d}'.format(len(json_cmd.encode())))
        # payload
        message.append(json_cmd)

        try:
            msg = "".join(message)
            self.client_socket.sendall(msg.encode())
            
        except:
            traceback.print_exc()
            return None
        return self.recv()
    
    def recv(self):
        total_data = []
        data = ""
        reply_length = 0
        bytes_remaining = ClientBase.HEADER_SIZE

        start = time.time()

        while time.time() - start < self.timeout:
            try:
                data = self.client_socket.recv(bytes_remaining)
            except:
                time.sleep(0.01)
                continue

            # Check if we recieved data
            if data:
                total_data.append(data)
                bytes_remaining -= len(data)

                # if we  have already gotten the full header
                if bytes_remaining <= 0:

                    # decode all the data in total data
                    for i in range(len(total_data)):
                        total_data[i] = total_data[i].decode()

                    # Reset to start getting the body
                    if reply_length == 0:
                        # full header
                        header = "".join(total_data)
                        # Use header to get payload len
                        reply_length = int(header)
                        
                        # set bytes remaining to that len
                        bytes_remaining = reply_length

                        # clear total data
                        total_data = []
                    else:
                        reply_json = ''.join(total_data)
                        return json.loads(reply_json)
        raise RuntimeError("Timeout waiting for response...")

    def isValidReply(self, reply):
        if not reply:
            print("Error: Did not recieve reply")
            return False
        else:
            if not reply['success']:
                print('here')
                print("Error: Did not recieve successful reply")
                return False
            else:
                return True



    # commands. All need 'cmd' key because that is what is used by the server
    def ping(self):
        cmd = {
            "cmd": "ping"
        }

        reply = self.send(cmd)
        return self.isValidReply(reply)

