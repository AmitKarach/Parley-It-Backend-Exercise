from bleach import Cleaner
from transaction import Transaction

"""
this is our Customer
he has a bank_account and a balance 
"""
class Customer:

    PAYMENTS = 12

    def __init__(self, bank_account: str):
        if Customer.validate_client(bank_account):
            self.balance = 0
            self.bank_account = bank_account
        else:
            print("not a valid client")

    
    #the Customer asks to strat a transation between him and the dst_bank_account
    def perform_advance(self, dst_bank_account: str, amount):
        if Customer .validate_perform(dst_bank_account, amount):
            self.balance += amount
            Transaction(self.bank_account, dst_bank_account,
                        amount, Customer .PAYMENTS)
        else:
            print("not a valid transaction")

    def validate_perform(dst_bank_account, amount):
        if len(dst_bank_account) <= 0:
            return False
        if amount < 0:
            return False
        return True

    def validate_client(bank_account):
        if len(bank_account) <= 0:
            return False
        return True
