import hashlib
import time
import json

class Block():
    _id = None
    _timestamp = None
    _pow = None
    _previous_hash = None
    _transactions = None

    def __init__(self, **argd):
        self._id = argd.get("id")
        self._timestamp = time.time()
        self._pow = argd.get("pow")
        self._previous_hash = argd.get("previous_hash")
        self._transactions = argd.get("transactions")

    def append_transaction(self, transaction):
        self._transactions.append(transaction)

    def hash(self):
        temp = str(self._id) + str(self._pow) + str(self._timestamp) + str(self._previous_hash)
        return hashlib.sha256(temp).hexdigest()

    def get_pow(self):
        return self._pow

    def get_transactions(self):
        return self._transactions

    def get_previous_hash(self):
        return self._previous_hash