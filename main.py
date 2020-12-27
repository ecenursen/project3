from HappyCoinNode import HappyCoinNode
from tkinter import *
from time import sleep,gmtime,strftime,time
from block import Block
from transactions import Transaction
from blockchain import Blockchain


current_IP = "192.168.1.117"  
current_port = 4000
peers = []

class HappyCoin_App(Tk):

    def __init__(self, *args, **kwargs):  
        Tk.__init__(self, *args, **kwargs) 
        window = Frame(self)   
        window.pack(side = "top", fill = "both", expand = True)  
        window.grid_rowconfigure(0, weight = 1) 
        window.grid_columnconfigure(0, weight = 1) 
   
        self.frames = {}   
   
        for fr in (StartPage, BalanceInfo ,UserTransactions, Blocks): 
            frame = fr(window, self) 
            self.frames[fr] = frame  
            frame.grid(row = 0, column = 0, sticky ="nsew") 

        self.show_frame(StartPage) 
   
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.load()

class StartPage(Frame):

    def __init__(self, parent, controller):  
        Frame.__init__(self, parent) 
        self.par = parent
        self.cont = controller

    def load(self):
        self.tkraise()
        info_label = Label(self,text="Collecting history from peers, please wait..")
        info_label.grid(row=0,column=0)
        
        start_peering()
        self.cont.show_frame(BalanceInfo)

    
class BalanceInfo(Frame): 

    def __init__(self, parent, controller):  
        Frame.__init__(self, parent) 
        self.par = parent
        self.cont = controller

    def load(self,recv_addr=None,trans_amount=None,trans_fee=None):
        self.tkraise()

        if recv_addr==None or recv_addr=="" or trans_amount==None or trans_amount=="":
            print("NULL")
        else:
            if trans_fee == "" or trans_fee == " ":
                trans_fee = 0.001
            else:
                trans_fee = float(trans_fee)
            newTrans = Transaction(fromAddress=node.addr,toAddress=recv_addr,amount=float(trans_amount),timestamp=time(),blockReward=0,transFee=trans_fee)
            node.create_transaction(newTrans)
        
        for widget in self.winfo_children():
            widget.destroy()

        button1 = Button(self, text ="BalanceInfo", relief="sunken", 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 0, column = 0, pady=(0,0))
        button2 = Button(self, text ="UserTransactions", relief="raised", 
        command = lambda : self.cont.show_frame(UserTransactions)) 
        button2.grid(row = 0, column = 1, pady=(0,0))
        button3 = Button(self, text ="Blocks", relief="raised", 
        command = lambda : self.cont.show_frame(Blocks)) 
        button3.grid(row = 0, column = 2, pady=(0,0))
          
        text_frame = Frame(self)
        text_frame.grid(row=2,columnspan=3)

        user_addr = node.addr
        user_uncomfirmed_balance = node.blockchain.get_balance(node.addr,1)
        user_comfirmed_balance = node.blockchain.get_balance(node.addr,0)


        receiver_addr = StringVar()
        trans_amount = StringVar()
        trans_fee = StringVar()
        receiver_addr.set("")
        trans_amount.set("")
        trans_fee.set("")

        text_area = Text(text_frame)
        text_area.grid(row=0,column=0,pady=(0,4))
        text_area.configure(height=7)

        text_area.insert(END,"\nYour address is " + user_addr)
        text_area.insert(END,"\nYour confirmed balance is " + str(user_comfirmed_balance))
        text_area.insert(END,"\nYour unconfirmed balance is " + str(user_uncomfirmed_balance))
        text_area.insert(END,"\n\nTo make transaction please enter receiver address, transaction amount and fee.")
        text_area.insert(END,"\nMinimum transaction fee is required. Minimum transaction fee is 0.001 HappyCoin ")

        transaction_area = Frame(text_frame)
        transaction_area.grid(row=1,column=0,pady=(0,0))

        receiver_label = Label(transaction_area,text="Receiver's Address")
        receiver_label.grid(row=0,column=0,pady=(0,0))
        receiver_area = Entry(transaction_area,textvariable=receiver_addr)
        receiver_area.bind("<Return>", self.load)
        receiver_area.grid(row=0,column=1,pady=(0,0))

        amount_label = Label(transaction_area,text="Transaction Amount")
        amount_label.grid(row=1,column=0,pady=(0,0))
        transaction_amount_area = Entry(transaction_area, textvariable=trans_amount)
        transaction_amount_area.bind("<Return>", self.load)
        transaction_amount_area.grid(row=1,column=1,pady=(0,0))

        fee_label = Label(transaction_area,text="Transaction Fee")
        fee_label.grid(row=2,column=0,pady=(0,0))
        transaction_fee_area = Entry(transaction_area, textvariable=trans_fee)
        transaction_fee_area.bind("<Return>", self.load)
        transaction_fee_area.grid(row=2,column=1,pady=(0,0))

        send_button = Button(transaction_area,text="Send",command= lambda: self.load(receiver_area.get(),transaction_amount_area.get(),transaction_fee_area.get()))
        send_button.grid(row=3,column=1,pady=(0,0))

class UserTransactions(Frame): 
    def __init__(self, parent, controller):  
        Frame.__init__(self, parent) 
        self.par = parent
        self.cont = controller
    
    def load(self):
        
        self.tkraise()
        for widget in self.winfo_children():
            widget.destroy()

        button1 = Button(self, text ="BalanceInfo",relief=RAISED, 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 0, column = 0, pady=(0,0))
        button2 = Button(self, text ="UserTransactions", relief=SUNKEN, 
        command = lambda : self.cont.show_frame(UserTransactions)) 
        button2.grid(row = 0, column = 1, pady=(0,0))
        button3 = Button(self, text ="Blocks", relief=RAISED, 
        command = lambda : self.cont.show_frame(Blocks)) 
        button3.grid(row = 0, column = 2, pady=(0,0))

        transaction_area = Frame(self)
        transaction_area.grid(row=2,columnspan=3,pady=(5,0),sticky='nw')

        transaction_table = Canvas(transaction_area,bg="white",width=1300,height=900)
        transaction_table.grid(row=0,column=0,sticky="news")

        scroll_area = Scrollbar(transaction_area,orient="vertical", command=transaction_table.yview,)
        scroll_area.grid(row=0,column=1,sticky="ns")
        transaction_table.configure(yscrollcommand=scroll_area.set)
        
        table_frame = Frame(transaction_table,bg="blue")
        transaction_table.create_window((0,0),window=table_frame,anchor="nw")

        transactions = node.blockchain.get_all_trans(node.addr)
        t_row = len(transactions)
        t_col = 5

        labels = [[Label() for j in range(t_col)] for i in range(t_row+1)]

        labels[0][0] = Label(table_frame,text="Transaction ID")
        labels[0][1] = Label(table_frame,text="Sender")
        labels[0][2] = Label(table_frame,text="Receiver")
        labels[0][3] = Label(table_frame,text="Amount")
        labels[0][4] = Label(table_frame,text="Time")

        for j in range(0,t_col):
            labels[0][j].grid(row=0,column=j,sticky="news")

        for i in range(0,t_row):
            labels[i+1][0] = Label(table_frame,text=transactions[i].transID)
            labels[i+1][1] = Label(table_frame,text=transactions[i].fromAddress)
            labels[i+1][2] = Label(table_frame,text=transactions[i].toAddress)
            labels[i+1][3] = Label(table_frame,text=transactions[i].amount)
            labels[i+1][4] = Label(table_frame,text=strftime("%Y-%m-%d %H:%M:%S", gmtime(transactions[i].timestamp)))
            for j in range(0,t_col):
                labels[i+1][j].grid(row=i,column=j,sticky="news")

        table_frame.update_idletasks()

        transaction_table.config(scrollregion=transaction_table.bbox("all"))
        

class Blocks(Frame): 
    def __init__(self, parent, controller):  
        Frame.__init__(self, parent) 
        self.par = parent
        self.cont = controller
    
    def load(self):
        self.tkraise()

        for widget in self.winfo_children():
            widget.destroy()

        button1 = Button(self, text ="BalanceInfo", relief=RAISED, 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 0, column = 0, pady=(0,0))
        button2 = Button(self, text ="UserTransactions", relief=RAISED, 
        command = lambda : self.cont.show_frame(UserTransactions)) 
        button2.grid(row = 0, column = 1, pady=(0,0))
        button3 = Button(self, text ="Blocks", relief=SUNKEN, 
        command = lambda : self.cont.show_frame(Blocks)) 
        button3.grid(row = 0, column = 2, pady=(0,0))

        block_area = Frame(self)
        block_area.grid(row=2,columnspan=3,pady=(5,0),sticky='nw')

        block_table = Canvas(block_area,bg="white",width=1300,height=900)
        block_table.grid(row=0,column=0,sticky="news")

        scroll_area = Scrollbar(block_area,orient="vertical", command=block_table.yview,)
        scroll_area.grid(row=0,column=1,sticky="ns")
        block_table.configure(yscrollcommand=scroll_area.set)
        
        table_frame = Frame(block_table,bg="blue")
        block_table.create_window((0,0),window=table_frame,anchor="nw")

        blocks = node.return_blocks()[::-1]
        t_row = len(blocks)
        t_col = 4
        
        labels = [[Label() for j in range(t_col)] for i in range(t_row+1)]

        labels[0][0] = Label(table_frame,text="Block Hash")
        labels[0][1] = Label(table_frame,text="Block Time")
        labels[0][2] = Label(table_frame,text="Number of Transaction")
        labels[0][3] = Label(table_frame,text="No. Confirmation")
        for j in range(0,t_col):
            labels[0][j].grid(row=0,column=j,sticky="news")
      
        for i in range(0,t_row):
            labels[i+1][0] = Label(table_frame,text=blocks[i].blockHash)
            labels[i+1][1] = Label(table_frame,text=strftime("%Y-%m-%d %H:%M:%S", gmtime(blocks[i].timestamp)))
            labels[i+1][2] = Label(table_frame,text=blocks[i].transNum)
            labels[i+1][3] = Label(table_frame,text=blocks[i].confirmations)
            for j in range(0,t_col):
                labels[i+1][j].grid(row=i+1,column=j,sticky="news")

        table_frame.update_idletasks()

        block_table.config(scrollregion=block_table.bbox("all"))
        
def start_peering():
    for peer in peers:
        node.connect_to_node(current_IP,peer)
    node.send_to_nodes({"func":"request_blocks"})
    newTrans = Transaction(fromAddress="XXXXX",toAddress=node.addr,amount=25.0,timestamp=time(),blockReward=0)
    node.create_transaction(newTrans)
    return 

if __name__=="__main__":
    node = HappyCoinNode(current_IP,current_port)
    node.start()
    app = HappyCoin_App() 
    app.title("HappyCoin")
    app.mainloop() 
    node.stop()

"""
node1 = HappyCoinNode(current_IP2,available_ports[0])
node2 = HappyCoinNode(current_IP2,available_ports[1])
node3 = HappyCoinNode(current_IP2,available_ports[2])

print("nodes created")

node1.start()
node2.start()
node3.start()

node1.connect_to_node(current_IP2,available_ports[1])
node1.connect_to_node(current_IP2,available_ports[2])
node3.connect_to_node(current_IP2,available_ports[1])

node1.send_to_nodes({"a":12})
node2.send_to_nodes({"b":23})
node3.send_to_nodes({"c":34})

node1.stop()
node2.stop()
node3.stop()
"""
