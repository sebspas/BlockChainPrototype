import sys
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain
from mining import mine, start_p2p_and_mining, consensus
from network import send_data_to_node, register_new_nodes_on_destnode

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine_request():
    block = mine(blockchain, node_identifier)

    if block is False:
        response = {
            'message': "Block added by the network"
        }
    else:
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

    return jsonify(response), 200


@app.route('/block/add', methods=['POST'])
def add_block():
    block = request.get_json()

    print("Received by the network:")
    print(str(block.get('index')) + " " + str(blockchain.last_block['index'] + 1))

    if block.get('index') == blockchain.last_block['index'] + 1:
        blockchain.add_block(block)
    elif block.get('index') >= blockchain.last_block['index'] + 2 \
            or block.get('index') == blockchain.last_block['index']:
        print("consensus")
        consensus(blockchain)

    return jsonify("Ok"), 200


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

    # Send the transaction to everyone on the network
    for n in blockchain.nodes:
        send_data_to_node('http://' + n + '/transactions/add', blockchain.current_transactions[-1])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/transactions/add', methods=['POST'])
def add_transaction():
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

    # check if the node to add is not ourselves
    for node in nodes:
        parse_url = urlparse(node).netloc

        if parse_url not in blockchain.nodes and parse_url != '127.0.0.1:' + my_port:
            blockchain.register_node(node)

    # register on all the other known nodes
    if int(my_port) == 5000:
        for node_source in blockchain.nodes:
            for node_dest in blockchain.nodes:
                register_new_nodes_on_destnode('http://' + node_source, 'http://' + node_dest)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus_request():
    replaced = consensus(blockchain)

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


if __name__ == '__main__':
    my_port = sys.argv[1]
    start_p2p_and_mining(blockchain, my_port, node_identifier)
    app.run(host='127.0.0.1', port=my_port)
