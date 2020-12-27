from hashlib import sha256
import time
from transactions import Transaction

class Block:
    # Class Constructor
    def __init__(self, transData, prevBlockHash, timestamp, transNum, blockHash, confirmations = 1):
        self.transData = transData                     # Completed Transactions
        self.transNum = transNum                       # number of the transactions
        self.prevBlockHash = prevBlockHash             # The hash of the previous block in the Blockchain                       
        self.timestamp = timestamp or time.time()      # Block creation time
        self.blockHash = blockHash
        self.confirmations = confirmations
    
    @staticmethod
    # The function to calculate the hash of the block
    def generate_hash(transData, timestamp, difficInc):
        transIDs = 0
        if transData != "First Block":
            for trans in transData:
                transIDs += trans.transID
        else:
            transIDs = "First Block"
        blockString = "{}{}{}".format(transIDs, timestamp, difficInc)
        blockString = blockString.encode()
        return sha256(blockString).hexdigest()


    # The function to convert Block object to dictionary
    def block_to_dict(self):
        transactions = []
        for trans in self.transData:
            transactions.append(trans.trans_to_dict())
        data = {
            "b_hash": self.blockHash,
            "b_time": self.timestamp,
            "t_no": self.transNum,
            "trans": transactions,
            "confirmations": self.confirmations,
            "prev_b_hash": self.prevBlockHash
        }
        return data
    
    @staticmethod
    # The function to convert Dictionary to Block object
    def dict_to_block(data):
        
        transData = []
        for trans in data["trans"]:
            transData.append(Transaction.dict_to_trans(trans))
        transNum = data["t_no"]
        prevBlockHash = data["prev_b_hash"]
        timestamp = data["b_time"]
        blockHash = data["b_hash"]
        confirmations = data["confirmations"]
    
        newBlock = Block(transData,prevBlockHash,timestamp,transNum,blockHash,confirmations)

        return newBlock


    def __repr__(self):
        return "{} - {} - {} - {}".format(self.transData, self.prevBlockHash, self.timestamp, self.confirmations)
