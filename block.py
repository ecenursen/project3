from hashlib import sha256
import time

class Block:
    # Class Constructor
    def __init__(self, transData, prevBlockHash, proofNo, timeStamp):
        self.transData = transData                     # Completed Transactions
        self.transNum = len(self.transData)            # number of the transactions
        self.prevBlockHash = prevBlockHash             # The hash of the previous block in the Blockchain
        self.proofNo = proofNo                         
        self.timeStamp = timeStamp or time.time()      # Block creation time
        self.blockHash = self.generate_hash()
        self.confirmations = 1
    
    # The function to calculate the hash of the block
    def generate_hash(self):
        transIDs = 0
        for trans in self.transData:
            transIDs += trans.transID

        blockString = "{}{}".format(transIDs,self.timeStamp)
        blockString = blockString.encode()
        return sha256(blockString).hexdigest()

    def block_to_dict(self):
        transactions = []
        for trans in self.transData:
            transactions.append(trans.transaction_to_dict())
        data = {
            "b_hash": self.blockHash,
            "b_time": self.timeStamp,
            "t_no": self.transNum,
            "trans": transactions,
            "confirmations": self.confirmations,
            "prev_b_hash": self.prevBlockHash
        }
        return data


    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.transData, self.prevBlockHash, self.proofNo, self.timeStamp, self.confirmations)
