import threading
import time

import requests

from network import register_new_nodes_on_destnode, send_data_to_node


def consensus(blockchain):
    blockchain.sync = False
    replaced = blockchain.resolve_conflicts()
    if replaced is True:
        print("New chain downloaded from the network.")
    else :
        print("No need to downlaod a new chain.")
    blockchain.sync = True


def mine(blockchain, node_identifier):
    while blockchain.sync is False:
        time.sleep(0.5)
    print("Starting mining a new block...")
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    if proof is False:
        print("Block mined by the network, proof invalid...")
        return False

    print("New block mined")
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

    # Send the new block to everyone else on the network
    for n in blockchain.nodes:
        send_data_to_node('http://' + n + '/block/add', block)

    return block


def launch_mining(blockchain, node_identifier):
    def mining():
        consensus(blockchain)
        while True:
            mine(blockchain, node_identifier)

    thread = threading.Thread(target=mining)
    thread.start()


def start_p2p_and_mining(blockchain, my_port, node_identifier, main_node_ip, my_ip):
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get('http://' + my_ip + ':' + str(my_port) + "/chain")
                if r.status_code == 200:
                    print('Node online!')
                    not_started = False
                    # we register to the main node
                    if int(my_port) != 5000:
                        print("Connecting to the main node...")
                        my_node_adr = 'http://' + my_ip + ':' + str(my_port)
                        dest_main_node_adr = 'http://' + main_node_ip + ':' + str(5000)
                        register_new_nodes_on_destnode(my_node_adr, dest_main_node_adr)
                        blockchain.register_node(dest_main_node_adr)
                        print("Adding the other nodes address to my data...")
                    launch_mining(blockchain, node_identifier)
            except:
                print('Server not yet started')
            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()
