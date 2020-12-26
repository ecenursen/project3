import socket
import sys
import time
import threading
import json

class HappyCoinConnection(threading.Thread):

    def __init__(self, main_node, sock, addr, host, port):

        super(HappyCoinConnection, self).__init__()

        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.awake = threading.Event()
        print("im:",self.port,"-connected:",self.main_node.port)
        # The addr of the connected node
        self.addr = addr

    def send(self, data):
        try:
            json_data = json.dumps(data)
            json_data = json_data.encode("utf-8")
            self.sock.sendall(json_data)
        except Exception as e:
            print('Unexpected Error in send message')
            print(e)

    #Function to stop thread
    def stop(self):
        self.awake.set()

    def run(self):
        self.sock.settimeout(5.0)          

        while not self.awake.is_set():
            incoming_data = b''

            try:
                incoming_data = self.sock.recv(4096) 

            except socket.timeout:
                print("Socket Timeout!")

            except Exception as e:
                self.awake.set()
                print("Error in HappyCoinConnection run:",e)

            if incoming_data != b'':
                decoded_data = incoming_data.decode('utf-8')
                print(type(decoded_data),"decodeddata:",decoded_data)
                send_data = json.loads(decoded_data)
                print(type(send_data),"senddata:",send_data)
                self.main_node.received_message( self, send_data)

            time.sleep(0.01)

        self.sock.settimeout(None)
        self.sock.close()
    

    def __str__(self):
        return 'HappyCoinConnection: {}:{} <-> {}:{} ({})'.format(self.main_node.host, self.main_node.port, self.host, self.port, self.addr)

    def __repr__(self):
        return '<HappyCoinConnection: HappyCoinNode {}:{} <-> Connection {}:{}>'.format(self.main_node.host, self.main_node.port, self.host, self.port)
