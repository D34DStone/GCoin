from flask import Flask, request, jsonify
import string
import random
import hashlib
from blockchain import Blockchain

app = Flask(__name__)

# TODO: Implement RSA Algorithm
PUBLIC_RSA_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

blockchain_server = Blockchain()

@app.route("/mine")
def mine_handle():

    def int_to_sha256(value):
        return hashlib.sha256(str.encode(str(counter))).hexdigest()

    counter_point = counter = random.randint(1, 1e18)
    previous_pow = blockchain_server.last_block().get("pow")
    while not Blockchain.proof_of_work(previous_pow, int_to_sha256(counter), 4):
        counter += 1

    reward_transaction = Blockchain.create_transaction(
        sender="GCoin",
        receiver=PUBLIC_RSA_KEY,
        amount=1,
        signature=""
    )

    blockchain_server.make_transactions(reward_transaction)
    new_block = blockchain_server.new_block(pow=int_to_sha256(counter))
    msg = ("Mined a new block after {} hashes!\nhash: {}\npow: {}\ntransactions: {}\n".format(
            counter - counter_point,
            Blockchain.hash_block(new_block),
            new_block.get("pow"),
            len(new_block.get("transactions"))
        ))

    return msg


@app.route("/make_transaction")
def make_transaction_handle():
    requested_params = ["sender", "receiver", "amount"]
    for param in requested_params:
        if param not in request.args.keys():
            return "Missing parameters!"

    sender = request.args.get("sender")
    receiver = request.args.get("receiver")
    amount = float(request.args.get("amount"))

    transaction = Blockchain.create_transaction(
        sender=sender,
        receiver=receiver,
        amount=amount,
        signature=""
    )

    blockchain_server.make_transactions(transaction)

    return "Transaction was appended!\n"


@app.route("/chain")
def chain_handle():
    return jsonify(blockchain_server.chain)


if __name__ == "__main__":
    app.run(port=5000, debug=True)