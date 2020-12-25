from hashlib import sha256
import time

class Block:
    # Class Constructor
    def __init__(self, index, transData, prevBlockHash, proofNo, timeStamp):
        self.index = index                             # The index of the block in the chain
        self.transData = transData                     # Completed Transactions
        self.prevBlockHash = prevBlockHash             # The hash of the previous block in the Blockchain
        self.proofNo = proofNo                         
        self.timeStamp = timeStamp                     # Block creation time

    def generate_hash(self):
        blockString = self.index + self.transData + self.prevBlockHash + self.proofNo + self.timeStamp
        blockString = blockString.encode()
        return sha256(blockString).hexdigest()
