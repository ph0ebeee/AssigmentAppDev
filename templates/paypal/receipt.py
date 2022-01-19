import datetime as datetime
import pyodbc
import root as root

class Receipt(root.Root):
    count_id = 0
    def __init__(self, trans_id, trans_time, trans_value):
        super().__init__('custID', datetime.datetime.now(), 'custID', datetime.datetime.now())    #first is userid, datetime(module)
        Receipt.count_id += 1
        self.trans_id = trans_id
        self.trans_time = trans_time
        self.trans_value = trans_value

    def get_trans_id(self):
        return self.trans_id

    def get_trans_time(self):
        return self.trans_time

    def get_trans_value(self):
        return self.trans_value

    def set_trans_id(self, trans_id):
        self.trans_id = trans_id

    def set_trans_time(self, trans_time):
        self.trans_time = trans_time

    def set_trans_value(self, trans_value):
        self.trans_value = trans_value

def load_result():
    receipt = []
    try:
        result_file = open('receipt_details.txt','r')
        for result in result_file:
            list = result.split(',')
            s = Receipt(list[0])
            s.time = list[1]
            s.total = list[2]
            receipt.append(s)   # to put in the class
    except:
        print("File not found")
    return receipt

load_result()
