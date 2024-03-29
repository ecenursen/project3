import socket
import sys
import time
import threading
import random
import hashlib

from HappyCoinConnection import HappyCoinConnection
from block import Block
from transactions import Transaction
from blockchain import Blockchain,keys_address_generator

class HappyCoinNode(threading.Thread):
    def __init__(self, host, port):
        super(HappyCoinNode, self).__init__()

        self.awake = threading.Event()

        # Server details, host (or ip) to bind to and the port
        self.host = host
        self.port = port

        # Nodes that have established a connection with this node
        self.nodes_connected = []  # Nodes that are connect with us N->(US)->N

        #for saving the copy of blockchain
        self.blockchain = Blockchain()
        self.creating_node_addresses()

        # Start server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(12.0)
        self.sock.listen(12)

    #for creating the addresses and keys
    #if node is previously created then it reads keys and addresses from file
    def creating_node_addresses(self):
        try:
            f = open("wallet.txt", mode='r+', encoding='utf-8')
            lines = f.readlines()
            self.privkey = lines[0].split("\n")[0]
            self.publickey = lines[1].split("\n")[0]
            self.addr = lines[2].split("\n")[0]
            self.receive_gift = False
            f.close()
        except:
            self.receive_gift = True
            self.privkey, self.publickey, self.addr = keys_address_generator()
            f = open("wallet.txt", mode='w+', encoding='utf-8')
            f.write(self.privkey+"\n")
            f.write(self.publickey+"\n")
            f.write(self.addr+"\n")
            f.close()



    def delete_closed_connections(self):
        for n in self.nodes_connected:
            if n.awake.is_set():
                n.join()
                del self.nodes_connected[self.nodes_connected.index(n)]

    def send_to_nodes(self, data):
        for n in self.nodes_connected:
            self.send_to_node(n, data)

    def send_to_node(self, n, data):
        self.delete_closed_connections()
        if n in self.nodes_connected:
            try:
                n.send(data)

            except Exception as e:
                print("HappyCoinNode send_to_node: Error while sending data to the node (" + str(e) + ")")
        else:
            print("HappyCoinNode send_to_node: Could not send the data, node is not found!")

    def connect_to_node(self, host, port):
        if host == self.host and port == self.port:
            print("connect_to_node: Cannot connect with yourself!!")
            return False

        # Check if node is already connected with this node!
        for node in self.nodes_connected:
            if node.host == host and node.port == port:
                print("connect_to_node: Already connected with this node.")
                return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))

            # Basic information exchange (not secure) of the addr's of the nodes!
            sock.send(self.addr.encode('utf-8')) # Send my addr to the connected node!
            connected_node_addr = sock.recv(4096).decode('utf-8') # When a node is connected, it sends it addr!

            thread_client = HappyCoinConnection(self, sock, connected_node_addr, host, port)
            thread_client.start()

            self.nodes_connected.append(thread_client)

        except Exception as e:
            print("Could not connect with node. (" + str(e) + ")")

    def disconnect_to_node(self, node):
        if node in self.nodes_connected:
            node.stop()
            node.join()  # When this is here, the application is waiting and waiting
            del self.nodes_connected[self.nodes_connected.index(node)]

        else:
            print("Cannot disconnect with a node with which we are not connected.")

    def stop(self):
        self.awake.set()

    def run(self):
        while not self.awake.is_set():  # Check whether the thread needs to be closed
            try:
                connection, client_address = self.sock.accept()
                
                # Basic information exchange (not secure) of the addr's of the nodes!
                connected_node_addr = connection.recv(4096).decode('utf-8') # When a node is connected, it sends it addr!
                connection.send(self.addr.encode('utf-8')) # Send my addr to the connected node!

                thread_client = HappyCoinConnection(self,connection, connected_node_addr, client_address[0], client_address[1])
                thread_client.start()

                self.nodes_connected.append(thread_client)
                
            except socket.timeout:
                #mining
                
                mined_block = self.blockchain.block_miner(self.addr)
                print("MINED BLOCK:",mined_block)
                if mined_block != False:
                    print("NOT FALSE")
                    self.send_new_block(mined_block)
                
                print("lend:",len(self.return_blocks()))
                print('HappyCoinNode: Connection timeout!')

            except Exception as e:
                raise e

            time.sleep(0.01)

        print("HappyCoinNode stopping...")
        for t in self.nodes_connected:
            t.stop()

        time.sleep(1)

        for t in self.nodes_connected:
            t.join()

        self.sock.settimeout(None)   
        self.sock.close()
        print("HappyCoinNode stopped")

    # function for handling the received message
    def received_message(self, node, data):
        if data["func"] == "request_blocks":
            self.send_start_blocks(node)
        elif data["func"] == "new_transaction":
            self.recv_new_transaction(Transaction.dict_to_trans(data["trans"]))
        elif data["func"] == "new_block":
            print("RECEIVED A NEW BLOCK")
            self.recv_new_block(Block.dict_to_block(data["block"]))
        elif data["func"] == "start_sending_blocks" or data["func"] == "end_sending_blocks":
            print("Blocks incoming")
        else:
            print("Unknown message:",data)
        print("Incoming message from:",node.port," to me:",self.port,"-",str(data))

    # function for returning the blocks that node has
    def return_blocks(self):
        print("return_len:",len(self.blockchain.blocks))
        if len(self.blockchain.blocks) == 0:
            return []
        ret_blocks = self.blockchain.blocks[1:]
        for blocks in self.blockchain.blocks:
            print("trans:",blocks.transData)
        print("blocks:",self.blockchain.blocks[1:])
        return ret_blocks

    #function for returning the unadded_transaction that node has 
    def return_unadded_transactions(self):
        return self.blockchain.unconfirmedTrans

    def send_new_block(self,new_block):
        self.send_to_nodes({"func":"new_block","block":new_block.block_to_dict()})
        print("I SEND THE NEW BLOCK")
        time.sleep(0.5)

    def recv_new_block(self,nBlock):
        print("RECEIVE NEW BLOCK OUTSIDE:",nBlock)
        result = self.blockchain.add_block_outside(nBlock)
        if result:
            print("Received a new block successfully")
        else:
            print("Received block has problems")

    #function for sending new transaction to all peers
    def send_new_transaction(self,new_trans):
        self.send_to_nodes({"func":"new_transaction","trans":new_trans.trans_to_dict()})
        time.sleep(0.5)

    #function for adding the newly received transaction to node
    def recv_new_transaction(self,trans):
        result = self.blockchain.add_trans_outside(trans)
        if result:
            print("Received a new transaction successfully")
        else:
            print("Received transaction has problems")

    #function for sending all blocks and transaction to newly connected peer
    def send_start_blocks(self,nodez):
        data = {"func": "start_sending_blocks"}
        self.send_to_node(nodez,data)
        time.sleep(0.2)
        send_blocks = self.return_blocks()
        for block in send_blocks:
            self.send_to_node(nodez,{"func":"new_block","block":block.block_to_dict()})
            time.sleep(0.2)
        for trans in self.blockchain.unconfirmedTrans:
            self.send_new_transaction(trans)
        data = {"func": "end_sending_blocks"}
        self.send_to_node(nodez,data)

    def create_transaction(self,nTrans):
        res = self.blockchain.add_trans_outside(nTrans)
        if res:
            self.send_new_transaction(nTrans)
        else:
            print("Problem creating transaction")

    def __str__(self):
        return 'HappyCoinNode: {}:{}'.format(self.host, self.port)

    def __repr__(self):
        return '<HappyCoinNode {}:{} addr: {}>'.format(self.host, self.port, self.addr)
