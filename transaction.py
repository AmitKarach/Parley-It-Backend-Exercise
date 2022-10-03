
from datetime import datetime,timedelta
from operator import mod
import pandas as pd
import os




"""
this class is the modle to connect between our worker and client and the data base

only this class is allowed to access the data base and retrive or rewrite a row there 
"""

class Transaction:

    INDEX=0
    DAYS_BETWEEN_TRANS=7

    """
    every transaction contains:
    id- of the transaction
    src_bank_account- where is the transfer is going
    dst_bank_account- where the transfer is from
    amount- how much we need to transfer
    date- when is the next trasaction for the worker
    """
    
    def __init__(self, src_bank_account, dst_bank_account, amount,count,date=None,id=0):
        self.id = id
        self.src_bank_account = src_bank_account
        self.dst_bank_account = dst_bank_account
        self.amount = amount
        self.count =count
        self.next_trasaction_date =date if date != None else datetime.today().date()
        if self.validate():
            if id==0:
                self.insert_to_table()
        else:
            print("not a valid transaction")

    #this function validate the data the customer sends us
    def validate(self):
        if len( self.src_bank_account)<=0:
            return False
        if len( self.dst_bank_account)<=0:
            return False
        if self.amount<0:
            return False
        if self.count<0:
            return False
        return True


    #if its the first time here we are creating the csv file
    def create_table(self):
        df = pd.DataFrame(data={'src_bank_account': [],'dst_bank_account': [], 'amount': []})
        try:
            df.to_csv('transactions.csv', mode='w', index =False)
        except IOError:
            print("File has opened already.")


    #when a transation is first created we need to insert it into the data base here:
    def insert_to_table(self):
        if not os.path.isfile('transactions.csv'):
            self.create_table()
        df =pd.read_csv('transactions.csv')
        self.id = Transaction.INDEX= Transaction.INDEX+1
        df_new_row = pd.DataFrame({
            'trans_id': [self.id],
            'src_bank_account': [self.src_bank_account],
            'dst_bank_account':[self.dst_bank_account],
            'amount': [self.amount/self.count],
            'count': [self.count],
            'next_trasaction_date': [self.next_trasaction_date]
            })
        df = pd.concat([df, df_new_row])
        df.to_csv('transactions.csv', index=False, mode='w')
    
    #enter the data base and change the count of this transaction 
    def update_count(self):
        df =pd.read_csv('transactions.csv', index_col='trans_id')
        row =df.loc[self.id].to_dict()
        row['count']-=1
        df.at[self.id,'count']=row['count']
        df.to_csv('transactions.csv', mode='w')

    #enter the data base and change the date of this transaction
    def update_date(self):
        df =pd.read_csv('transactions.csv', index_col='trans_id')
        row =df.loc[self.id].to_dict()
        next_date = datetime.strptime(row['next_trasaction_date'], "%Y-%m-%d").date()
        row['next_trasaction_date']=next_date+ timedelta(days=Transaction.DAYS_BETWEEN_TRANS)
        df.at[self.id,'next_trasaction_date']=row['next_trasaction_date']
        df.to_csv('transactions.csv', mode='w')

    #returns an array of the relevent transaction for the worker 
    def get_active_transactions():
        df =pd.read_csv('transactions.csv')
        count= (df['count']>0)
        active_df= df.loc[count].to_dict('records')
        return Transaction.to_transaction(active_df)

    # packs the relevant transactions from the DataFrame to a array of transactions
    def to_transaction(dfList):
        transArray= []
        for trans in dfList:
            t1= Transaction(str(trans['src_bank_account']),str(trans['dst_bank_account']),trans['amount'],trans['count'],trans['next_trasaction_date'],trans['trans_id'])
            transArray.append(t1)
        return transArray