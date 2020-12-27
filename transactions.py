import secrets


class Transaction:
    def __init__(self, fromAddress, toAddress, amount, timestamp, blockReward, transID, transFee=0.001):
        self.transID = transID
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.transFee = transFee
        self.timestamp = timestamp
        self.blockReward = blockReward

    # The function to convert Transaction object to dictionary
    def trans_to_dict(self):
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
    
    @staticmethod
    # The function to convert Dictionary to Transaction object
    def dict_to_trans(data):

        transID = data["t_id"]
        fromAddress = data["t_sender"]
        toAddress = data["t_receiver"]
        amount = data["t_amount"]
        blockReward = data["block_reward"]
        transFee = data["t_fee"]
        timestamp = data["t_time"]
        newTrans = Transaction(fromAddress,toAddress,amount,timestamp,blockReward,transID=transID,transFee=transFee)

        return newTrans
    
