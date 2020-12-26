from hashlib import sha256
import time
from block import *
from transactions import *

class Blockchain:
    # Class Constructor
    def __init__(self):
        self.blocks = []                    # To store all the blocks(chain)
        self.unconfirmedTrans = []          # To store unconfrimed Transactions  
        self.completedTrans = []            # To store done Transactions
        self.cons_initial_block()           # Calling the function to create the first block
    
    # The function for creating new blocks
    def create_block(self, proofNo, prevBlockHash):
        newBlock = Block(
            index = len(self.blocks),                   # The index of the new block
            transData = self.unconfirmedTrans,            
            prevBlockHash = prevBlockHash,
            proofNo = proofNo,
            timeStamp = time.time()
        )
        self.unconfirmedTrans = []
        # Adding new block to Chain
        self.blocks.append(newBlock)
        return newBlock

    # The function for creating first block in chain
    def cons_initial_block(self):
        self.create_block(proofNo = 0, prevBlockHash = 0)
    
    # The function to check validity of all blocks in the chain
    def validity_checker(self):
        # Iterate all chain
        for i in range(1,len(self.blocks)):
            # Getting the current and previous blocks
            block = self.blocks[i]
            prevBlock = self.blocks[i-1]

            # Checking the block indexes
            if(prevBlock.index + 1 != block.index):
                return False
            # Checking the previous block's hash
            elif(prevBlock.generate_hash != block.prevBlockHash):
                return False
            # Checking the timestamps
            elif block.timeStamp <= prevBlock.timeStamp:
                return False
        return True

    # The function to add new transaction
    def add_transaction(self, transaction):
        self.unconfirmedTrans.append(transaction)
    
    # The function to prevent the blockchain from abuse
    @staticmethod
    def proof_checker(lastProof):
        proofNo = 0
        while Blockchain.proof_verifier(proofNo, lastProof) is False:
            proofNo += 1

        return proofNo

    # The function to check the proof
    @staticmethod
    def proof_verifier(lastProof, proof):
        guess = lastProof + proof
        guess = guess.encode()
        guessHash = sha256(guess).hexdigest()
        return guessHash[:4] == "0000"
    
    # The function to get the latest block of the chain
    def latest_block(self):
        return self.blocks[-1]

    # The function to get Hash of the latest block
    def latest_block_hash(self):
        return self.latest_block.blockHash