import hashlib
from block import Block

# Show how many last symbols of POW answer should be a 0 (hashed by SHA256)
# 1..32
MINIG_DIFFICULT = 5
GENESIS_ACCOUNT_TITLE = "System"

class Blockchain():
    _blockchain = []
    _uncommited_transactions = []


    def __init__(self):
        genesis_block = Block(
            id = 1,
            pow = "genesis_pow",
            previous_hash = "genesis_hash",
            transactions = {}
        )

        self._blockchain.append(genesis_block)


    def last_block(self):
        if len(self._blockchain) is 0:
            return None

        return self._blockchain[len(self._blockchain) - 1]


    def create_transaction(self, transaction):
        self._uncommited_transactions.append(transaction)


    @classmethod
    def proof_of_work(cls, prev_pow, pow):
        return hashlib.sha256(str.encode(prev_pow + pow)).hexdigest()[-5:] == "0" * 5


    @classmethod
    def check_chain(cls, chain, third_party_transactions = []):

        # Check for pow and hashes equality
        for i in range(1, len(chain) - 1):
            if not Blockchain.proof_of_work(chain[i - 1].get_pow(), chain[i].get_pow()):
                return False

            if chain[i].get_previous_hash() != chain[i - 1].hash():
                return False

        # Check if there is no accounts that spend more coins than they have
        transactions = []

        for block in chain:
            transactions = transactions + block._get_transactions()

        transactions += third_party_transactions

        accounts = dict()

        for transaction in transactions:
            accounts[transaction.get("from")] -= transaction.get("amount")
            accounts[transaction.get("to")] += transaction.get("amount")

        for account_title in accounts.keys():
            if account_title is GENESIS_ACCOUNT_TITLE:
                continue

            if accounts.get(account_title) < 0:
                return False

        return True


    def mine_block(self, previous_pow):
        last_block = self.last_block()
        previous_pow = last_block.get_pow()
        current_pow = 0

        while not Blockchain.proof_of_work(previous_pow, str(current_pow)):
            current_pow += 1

        


b = Blockchain()

print(b.mine_block("12345"))
