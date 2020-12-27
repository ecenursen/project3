from hashlib import sha256
import time
from block import *
from transactions import Transaction
import bitcoin_keygen
import secrets

class Blockchain:
    # Class Constructor
    def __init__(self):
        self.blocks = []                    # To store all the blocks(chain)
        self.unconfirmedTrans = []          # To store unconfrimed Transactions  
        self.completedTrans = []            # To store done Transactions
        self.cons_initial_block()           # Calling the function to create the first block
    
    # The function for selecting 4 transaction to create new block
    def trans_selector(self, myAddress):
        # tek trans basa ekle

        transactions = []
        if(len(self.unconfirmedTrans) < 4):
            print("less than 4 transaction")
            return transactions
        else:
            # Creating new amount value for Reward transaction
            newAmount = 0
            for i in range(4):
                newAmount += self.unconfirmedTrans[i].transFee
            # Creating new trans for reward
            rewardTrans = Transaction("XXXXXX", myAddress, newAmount, timestamp=time.time(), blockReward=True)
            transactions.append(rewardTrans)
            
            # Selecting 4 transactions from the unconfirmed transaction to create new block
            for i in range(4):
                transactions.append(self.unconfirmedTrans[0])
                self.unconfirmedTrans.remove(self.unconfirmedTrans[0])

        return transactions

    # The function for creating first block in chain
    def cons_initial_block(self):
        timestamp = time.time()
        blockHash = Block.generate_hash("First Block",timestamp,1)
        self.blocks.append(Block("First Block",0,timestamp,0,blockHash))
    
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
    
    # The function to get the latest block of the chain
    def latest_block(self):
        return self.blocks[-1]


    # The function to find all confirmed transactions from the chain for given address
    def get_trans(self, myAddress):
        transactions = []
        for block in self.blocks:
            if block == self.blocks[0]:
                continue
            for transaction in block.transData:
                if (transaction.fromAddress == myAddress or transaction.toAddress == myAddress):
                    transactions.append(transaction)
        return transactions

    # The function to find all transactions(confirmed + unconfirmed) for given address
    def get_all_trans(self, myAddress):
        # Getting all confirmed trans from blocks
        transactions = self.get_trans(myAddress)
        # Getting unconfirmed trans
        for transaction in self.unconfirmedTrans:
            if (transaction.fromAddress == myAddress or transaction.toAddress == myAddress):
                transactions.append(transaction)
        return transactions
    
    # The function to get the balance value of the given address
    def get_balance(self, myAddress, includeUnconf):
        balance = 0
        # Getting requiered transactions(all or only confirmed)
        if includeUnconf:
            transactions = self.get_all_trans(myAddress)
        else:
            transactions = self.get_trans(myAddress)

        for trans in transactions:
            if(trans.fromAddress == myAddress):
                balance -= trans.amount
                balance -= trans.transFee
            elif(trans.toAddress == myAddress):
                balance += trans.amount

        return balance

    # The function to add new block from outside
    def add_block_outside(self, newBlock):
        # Checking whether new block in Chain or not
        for block in self.blocks:
            if(block.blockHash == newBlock.blockHash):
                return False
        
        # Checking there is any same transaction with new block and other blocks
        for transNewBlock in newBlock.transData:
            for block in self.blocks:
                for transBlock in block.transData:
                    if(transNewBlock.transID == transBlock.transID):
                        return False
    
        # Checking there is any same transaction with chain and new block
        for transBlock in newBlock.transData:
            for transChain in self.unconfirmedTrans:
                if(transBlock.transID == transChain.transID):
                    self.unconfirmedTrans.remove(transChain)

        # Incrementing confirmation number for other old blocks
        for block in self.blocks:
            block.confirmations += 1
        # Make new block's confirmation = 1
        newBlock.confirmations = 1   
        self.blocks.append(newBlock)           
        return True
    
    #function for adding transaction from outside
    def add_trans_outside(self,newTrans):
        for block in self.blocks:
            if  block == self.blocks[0]:
                continue
            for trans in block.transData:
                if newTrans.transID == trans.transID:
                    print("from here",newTrans.transID)
                    return False

        sender_balance = self.get_balance(newTrans.fromAddress,1)

        if sender_balance < (newTrans.amount + newTrans.transFee):
            if newTrans.fromAddress == "XXXXX":
                self.add_transaction(newTrans)
                return True
            return False
        
        self.add_transaction(newTrans)
        return True

    @staticmethod
    # The function
    def mine_block(transData, diffic):
        difficCheck = "0" * diffic
        difficInc = 0
        blockHash = Block.generate_hash(transData,time.time(),difficInc)
        print("start finding hash")
        while blockHash[:diffic] != difficCheck:
            blockHash = Block.generate_hash(transData, time.time(), difficInc)
            difficInc += 1
        print("found hash:",blockHash)
        return blockHash

    def block_miner(self, minerAddress):
        # Checking whether there is enough transaction to create new block
        if not self.trans_selector(minerAddress):
            return False
        
        # Getting 4+1 trans
        transData = self.trans_selector(minerAddress)
        # Finding block hash by iterating
        blockHash = self.mine_block(transData,5)
        newBlock = Block(
            transData=transData,
            prevBlockHash=self.blocks[-1].blockHash,
            timestamp=time.time(),
            transNum=len(transData),
            blockHash=blockHash
        )
        # Incrementing confirmation number for other old blocks
        for block in self.blocks:
            block.confirmations += 1
        # Adding new block to Chain
        print("newblock:",newBlock)
        self.blocks.append(newBlock)

        return newBlock

def keys_address_generator():

    # Private key generator
    bits = secrets.randbits(256)
    bitsHex = hex(bits)
    privateKey = bitsHex[2:]
    publicKey = bitcoin_keygen.private2public(privateKey)
    address = bitcoin_keygen.public2address(publicKey)
    return privateKey, publicKey, address
        


privkey, publick, add = keys_address_generator()
print(privkey)
print(publick)
print(add)