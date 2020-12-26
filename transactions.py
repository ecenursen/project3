
class Transaction:
    def __init__(self, transID, fromAddress, toAddress, amount, timestamp, blockReward, transFee=0.1):
        self.transID = transID
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.transFee = transFee
        self.timestamp = timestamp
        self.blockReward = blockReward
        
    def transction_to_dict(self):
        data = {
            "t_id": self.transID,
            "t_sender": self.fromAddress,
            "t_receiver": self.toAddress,
            "t_amount": self.amount,
            "block_reward": self.blockReward,
            "t_fee": self.transFee,
            "t_time": self.timestamp
        }
        return data
    
    
