from hashlib import sha256
import time

class Block:
    # Class Constructor
    def __init__(self, index, transData, prevBlockHash, proofNo, timeStamp):
        self.index = index                             # The index of the block in the chain
        self.transData = transData                     # Completed Transactions
        self.transNum = len(self.transData)            # number of the transactions
        self.prevBlockHash = prevBlockHash             # The hash of the previous block in the Blockchain
        self.proofNo = proofNo                         
        self.timeStamp = timeStamp or time.time()      # Block creation time
        self.blockHash = self.generate_hash()
    
    # The function to calculate the hash of the block
    def generate_hash(self):
        blockString = "{}{}{}{}{}{}".format(self.index, self.transData, self.transNum, self.prevBlockHash, self.proofNo, self.timeStamp)
        blockString = blockString.encode()
        return sha256(blockString).hexdigest()

    def __repr__(self):
        return "{}- {} - {} - {} - {}".format(self.index, self.transData, self.prevBlockHash, self.proofNo, self.timeStamp)