from datetime import datetime,timedelta
import time
import blackBox
from transaction import Transaction


"""
this is the worker 
his job is to wake up evrey day and check if there are transactions he needs to attend to
and if there are he needs to send them to the blackBox and get conformation that the transfer was success
"""

class TransactionWorker:

    #how long wait between worker rounds //24 hours
    TIME_OUT=1
    #how many days does the system need to save the last transations (5 days)
    DAYS_WORKING=1
    DATE= datetime.today().date()

    def __init__(self):
        self.flag = True

    
    #will execute the relevant transaction that it gets
    def execute(trans):
        transaction_id =blackBox.perform_transaction(trans.src_bank_account ,trans.dst_bank_account, trans.amount,'debit')
        if TransactionWorker.validate(transaction_id):
            trans.update_count()
            # if the perform_transaction credits the src_bank_account with the amount we need need 
        trans.update_date()

    #validate that the transaction had gone through if so returns True
    def validate(trans_id):
        lst = blackBox.download_report(TransactionWorker.DAYS_WORKING)
        for sublist in lst:
            if sublist['transaction_id'] == trans_id:
                return sublist['transaction_result']
        return False

    """
    this function is the heart of the worker
    unlass the flag is False (so the main can stop is from running indefinitely) 
    it will wake up and search for transactions that are active and relevant and then preforming the transaction

    """
    def start(self):
        while(self.flag):
            print("today is " ,TransactionWorker.DATE)

            transArray= Transaction.get_active_transactions()
            for trans in transArray:
                next_date = datetime.strptime(trans.next_trasaction_date, "%Y-%m-%d").date()
                if next_date <= TransactionWorker.DATE: #if worker was offline
                    TransactionWorker.execute(trans)
                    
            TransactionWorker.DATE = TransactionWorker.DATE+ timedelta(days=1)
            TransactionWorker.DAYS_WORKING+=1
            if TransactionWorker.DAYS_WORKING ==5:
                TransactionWorker.DAYS_WORKING ==1
            print("going to sleep good night")
            time.sleep(TransactionWorker.TIME_OUT)

    #stops the worker
    def stop(self):
        self.flag = False
