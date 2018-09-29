from flask import Flask, request, jsonify
import requests
import string
import random
import json
import sys
import hashlib
from blockchain import Blockchain

app = Flask(__name__)

# TODO: Implement RSA Algorithm
PUBLIC_RSA_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

blockchain_server = Blockchain()
hosts = set()


@app.route("/mine")
def mine_handle():
    """
    Asynchronously tries to solve Proof Of Power problem.
    After it solved creates new block and commit all of
    uncommited transactions.
    """
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
    msg = ("Mined a new block after {} hashes!\nid: {}\nhash: {}\npow: {}\ntransactions: {}\n".format(
            new_block.get("id"),
            counter - counter_point,
            Blockchain.hash_block(new_block),
            new_block.get("pow"),
            len(new_block.get("transactions"))
        ))
    return msg


@app.route("/make_transaction")
def make_transaction_handle():
    """
    Just push another transaction into queue.

    TODO: Make it calc digital signature using RSA and send to confirm
    to other machines.   
    """
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

    for host in hosts:
        requests.get("http://{}?sender={}?receiver={}?amount={}".format(
            host, sender, receiver, amount
        ))

    return "Transaction was appended!\n"


@app.route("/resolve_conflicts")
def resolve_conflicts_handle():
    changed = False

    for host in hosts:
        chain = json.loads(requests.get("http://{}/chain".format(host)))

        if len(chain) > len(blockchain_server.chain):
            blockchain_server.chain = chain
            changed = True

    if changed:
        print("The chain was updated by third party node!\n")


@app.route("/chain")
def chain_handle():
    """
    Return chain of blocks.
    """
    return jsonify(blockchain_server.chain)


@app.route("/register_host")
def register_host_handle():
    if "host" not in request.args.keys():
        return "Missing parameters!\n"

    hosts.add(request.args.get("host"))

    return "Host was written to the host-list.\n"


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Wrong number of arguments!\npython3 main.py [port]")
        exit(1)

    try:
        port = int(sys.argv[1])
    except Exception:
        print("Couldn't parse port")
        exit(1)

    app.run(port=port, debug=True)