import time
import hashlib
import json

class Blockchain():
    chain = []
    uncommited_transactions = []


    @classmethod
    def create_transaction(cls, **argd):
        return {
            "sender": argd.get("sender"),
            "receiver": argd.get("receiver"),
            "amount": argd.get("amount"),
            "signature": argd.get("signature")
        }


    @classmethod
    def create_block(cls, **argd):
        return {
            "id": argd.get("id"),
            "previous_hash": argd.get("previous_hash"),
            "transactions": argd.get("transactions"),
            "pow": argd.get("pow"),
            "timestamp": time.time()
        }


    @classmethod
    def hash_block(cls, block):
        return hashlib.sha256(str.encode(json.dumps(block))).hexdigest()


    @classmethod
    def proof_of_work(cls, previous_pow, current_pow, difficult):
        hash = hashlib.sha256(str.encode(previous_pow + current_pow)).hexdigest()
        return hash[-difficult:] == "0" * difficult


    def __init__(self):
        self.chain.append(Blockchain.create_block(
            id=0,
            previous_hash="0",
            transactions=[],
            pow="0"
        ))


    def last_block(self):
        return self.chain[len(self.chain) - 1]


    def make_transactions(self, transaction):
        self.uncommited_transactions.append(transaction)


    def new_block(self, pow):
        previous_block = self.last_block()

        id = previous_block.get("id")

        previous_hash = Blockchain.hash_block(previous_block)

        transactions = self.uncommited_transactions
        self.uncommited_transactions = []

        block = Blockchain.create_block(
            id=id + 1,
            previous_hash=previous_hash,
            transactions=transactions, 
            pow=pow
        )

        self.chain.append(block)

        return block



