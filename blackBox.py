

import random

from traitlets import Integer


transactions=[]

def perform_transaction(src_bank_account, dst_bank_account, amount, direction):
    trans_id =int(random.random()*1000)
    trans_rslt =bool(random.getrandbits(1))
    transactions.append({"transaction_id": trans_id, "transaction_result": trans_rslt})
    return trans_id

#we need to send here how many days the worker is working because we are not waiting 24 hours 
def download_report(daysWorking):
    global transactions
    temp_trans = transactions
    if daysWorking == 5:
        transactions =[]
        return temp_trans
    return transactions