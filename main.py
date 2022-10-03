import os
import time
from tkinter import W
from customer import Customer
from transactionworker import TransactionWorker
import threading


worker = TransactionWorker()
MAIN_TIMER = 50


def transactions():
    os.remove("transactions.csv")
    c = Customer("12")
    c.perform_advance("153", 1000)
    c2 = Customer("22")
    c2.perform_advance("12", 1000)
    print("finished creating transactions")

    time.sleep(MAIN_TIMER)
    worker.stop()


def start_worker():
    time.sleep(1)
    worker.start()


def main():
    t1 = threading.Thread(target=start_worker)
    t1.start()
    transactions()

    t1.join()
    print("Thread Done")


if __name__ == "__main__":
    main()
