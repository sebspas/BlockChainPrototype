import json
import sys
import threading
import time
import urllib
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    # register on all the other known nodes
    if int(my_port) == 5000:
        for node_source in blockchain.nodes:
            for node_dest in blockchain.nodes:
                print("n:" + node_source + " d:" + node_dest)
                register_new_nodes_on_destnode('http://' + node_source, 'http://' + node_dest)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    print(blockchain.nodes)
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


@app.route('/nodes', methods=['GET'])
def nodes_list():
    var = ""
    for n in blockchain.nodes:
        var += n + ","

    response = {
        'nodes': var
    }

    return jsonify(response), 200

@app.route("/")
def hello():
    return "BlockChain Started!"

def register_new_nodes_on_destnode(newnode_adr, dest_node_adr):
    data = {
        'nodes': [newnode_adr]
    }
    adr = dest_node_adr + '/nodes/register'
    req = urllib.request.Request(adr)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:' + str(my_port) + "/")
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                    # we register to the main node
                    if int(my_port) != 5000:
                        my_node_adr = 'http://' + '127.0.0.1' + ':' + str(my_port)
                        dest_main_node_adr = 'http://' + '127.0.0.1' + ':' + str(5000)
                        register_new_nodes_on_destnode(my_node_adr, dest_main_node_adr)
                        blockchain.register_node(dest_main_node_adr)
            except:
                print('Server not yet started')
            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()

if __name__ == '__main__':
    my_port = sys.argv[1]
    start_runner()
    app.run(host='127.0.0.1', port=my_port)
