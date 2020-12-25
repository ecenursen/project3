from HappyCoinNode import HappyCoinNode
from tkinter import *
from time import sleep

current_IP2 = "192.168.1.120"   
current_IP = ''
available_ports = [12000,3000,4000]    
current_port = 4000   
LARGEFONT =("Verdana", 35) 
transactions = [["nsbdnf","kjbkjh","kknklm"],["nsbdnf","kjbkjh","kknklm"],["nsbdnf","kjbkjh","kknklm"],["nsbdnf","kjbkjh","kknklm"],["nsbdnf","kjbkjh","kknklm"],["nsbdnf","kjbkjh","kknklm"]]

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

        button1 = Button(self, text ="StartNode", 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 1, column = 0, pady=(0,0))
    
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
            print("PRINT REFRESH")
            print("recv_addr:",recv_addr)
            print("transaction amount:",trans_amount)
            print("Transaction fee:",trans_fee)
        
        for widget in self.winfo_children():
            widget.destroy()

        button1 = Button(self, text ="BalanceInfo", 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 0, column = 0, pady=(0,0))
        button2 = Button(self, text ="UserTransactions", 
        command = lambda : self.cont.show_frame(UserTransactions)) 
        button2.grid(row = 0, column = 1, pady=(0,0))
        button3 = Button(self, text ="Blocks", 
        command = lambda : self.cont.show_frame(Blocks)) 
        button3.grid(row = 0, column = 2, pady=(0,0))
          
        text_frame = Frame(self)
        text_frame.grid(row=2,columnspan=3)

        user_addr = "kekrekrek"
        user_balance = 12

        receiver_addr = StringVar()
        trans_amount = StringVar()
        trans_fee = StringVar()
        receiver_addr.set("")
        trans_amount.set("")
        trans_fee.set("")

        text_area = Text(text_frame)
        text_area.grid(row=0,column=0,pady=(0,4))
        text_area.configure(height=6)

        text_area.insert(END,"\nYour address is " + user_addr)
        text_area.insert(END,"\nYour current balance is " + str(user_balance))
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

        button1 = Button(self, text ="BalanceInfo", 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 0, column = 0, pady=(0,0))
        button2 = Button(self, text ="UserTransactions", 
        command = lambda : self.cont.show_frame(UserTransactions)) 
        button2.grid(row = 0, column = 1, pady=(0,0))
        button3 = Button(self, text ="Blocks", 
        command = lambda : self.cont.show_frame(Blocks)) 
        button3.grid(row = 0, column = 2, pady=(0,0))

        transaction_area = Frame(self)
        transaction_area.grid(row=2,columnspan=3,pady=(5,0),sticky='nw')


class Blocks(Frame): 
    def __init__(self, parent, controller):  
        Frame.__init__(self, parent) 
        self.par = parent
        self.cont = controller
    
    def load(self):
        self.tkraise()

        for widget in self.winfo_children():
            widget.destroy()

        button1 = Button(self, text ="BalanceInfo", 
        command = lambda : self.cont.show_frame(BalanceInfo)) 
        button1.grid(row = 0, column = 0, pady=(0,0))
        button2 = Button(self, text ="UserTransactions", 
        command = lambda : self.cont.show_frame(UserTransactions)) 
        button2.grid(row = 0, column = 1, pady=(0,0))
        button3 = Button(self, text ="Blocks", 
        command = lambda : self.cont.show_frame(Blocks)) 
        button3.grid(row = 0, column = 2, pady=(0,0))

        frame_scrollbar = Frame(self)
        frame_scrollbar.grid(row=2,columnspan=3,pady=(5,0),sticky='nw')
        frame_scrollbar.grid_rowconfigure(0, weight=1)
        frame_scrollbar.grid_columnconfigure(0, weight=1)
        frame_scrollbar.grid_propagate(False)

        canvas = Canvas(frame_scrollbar,bg="yellow")
        scrollbar = Scrollbar(frame_scrollbar,orient="vertical",command=canvas.yview)
        scrollbar.grid(row=0,column=1,sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        frame_text = Frame(canvas,bg="blue")
        canvas.create_window((0, 0), window=frame_text, anchor='nw')
        labels = [Label() for i in range(10)]

        for i in range(0,10):
            texts = "TestingText" + str(i)
            labels[i] = Label(frame_text, text =texts)
            labels[i].grid(row=i,column=0,sticky="news")

        frame_text.update_idletasks()

        first5rows_height = sum([labels[i].winfo_height() for i in range(0, 5)])
        frame_scrollbar.config(width= scrollbar.winfo_width(),height=first5rows_height)

        canvas.config(scrollregion=canvas.bbox("all"))

        button_send = Button(self,text="SEND",command=self.send_messagez)
        button_send.grid(row=5,column=1,padx = 20, pady = 10)
        
     
    

app = HappyCoin_App() 
app.title("HappyCoin")
app.grid_rowconfigure(0, weight=1)
app.columnconfigure(0, weight=1)
app.mainloop() 

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