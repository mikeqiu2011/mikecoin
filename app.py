from flask import Flask, jsonify, request
from mikecoin import MikeCoin
import sys

app = Flask(__name__)
mike_coin = MikeCoin()


@app.route('/mine_block', methods=['POST'])
def mine_block():
    block = mike_coin.mine_block()
    resp = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'transactions': block['transactions'],
        'prev_hash': block['prev_hash']
    }

    return jsonify(resp), 201


@app.route('/chain', methods=['GET'])
def get_chain():
    resp = {
        'chain': mike_coin.get_chain(),
        'length': len(mike_coin.get_chain())
    }

    return jsonify(resp), 200

@app.route('/isvalid', methods=['GET'])
def is_valid():
    is_valid = mike_coin.is_chain_valid()
    resp = {
        'is_valid': is_valid
    }

    return jsonify(resp), 200

@app.route('/transaction', methods=['POST'])
def add_transaction():
    body = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in body for key in transaction_keys):
        return 'some keys are missing', 400

    index = mike_coin.add_transaction(body['sender'], body['receiver'], body['amount'])

    resp = {'message': f'This transaction will be added into block number {index}'}
    return jsonify(resp), 201

@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    print(f'payload is {json}')
    nodes = json['nodes']
    if nodes is None:
        return 'no nodes', 400

    for node in nodes:
        mike_coin.add_node(node)

    resp = {
        'message': f'{len(mike_coin.nodes)} nodes added successfully!',
        'nodes': list(mike_coin.nodes)
    }
    print(f'resp is {resp}')
    return jsonify(resp), 201



@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = mike_coin.replace_chain()
    resp = {
        'is_chain_replaced': is_chain_replaced,
        'chain': mike_coin.chain
    }

    return jsonify(resp), 200


# run the app
app.run(host='0.0.0.0', port=sys.argv[1])
