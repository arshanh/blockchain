from uuid import uuid4
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request
import threading

from blockchain import Blockchain
from util import getAddrsForHost

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Get neighbor IPs
neighbors = getAddrsForHost('blockchain', 80)

# Instantiate the Blockchain
blockchain = Blockchain(node_identifier, neighbors)

@app.route('/hello', methods=['GET'])
def hello():
    values = request.get_json()

    if not values or 'sender' not in values:
        return 'Missing request body', 400

    sender = values['sender']

    print(f'Recieved hello from {sender}')

    response = {
            'hello-response': node_identifier
            }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # Decouple transport and logic by just calling a wrapper here
    block = blockchain.mine()

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
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

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
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

def send_hello():
    class HelloThread(threading.Thread):
        @classmethod
        def run(cls):
            blockchain.hello()

    thread = HelloThread()
    thread.start()


if __name__ == '__main__':
    send_hello()
    app.run(host='0.0.0.0', port=80)
