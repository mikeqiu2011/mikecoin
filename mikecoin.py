import datetime
import hashlib
import json
from uuid import uuid4
from urllib.parse import urlparse
import requests


class MikeCoin:
    def __init__(self):
        self.transactions = []
        self.chain = []
        self.create_block(proof=1, previous_hash=0)

        self.nodes = set()
        self.node_address = str(uuid4()).replace('-', '')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.transactions,
            'proof': proof,
            'prev_hash': previous_hash
        }

        self.transactions = []  # once the transactions are added to the new block, it must be emptied
        self.chain.append(block)
        return block

    def get_node_address(self):
        return self.node_address

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1

        while True:
            hash_value = self.get_hash(new_proof, previous_proof)

            if hash_value[:4] == '0000':
                print(f'hash value is:', hash_value)
                return new_proof

            new_proof += 1

    def get_hash(self, new_proof, previous_proof):
        payload = str(new_proof ** 2 - previous_proof ** 2).encode()
        hash_value = hashlib.sha256(payload).hexdigest()
        return hash_value

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            cur_block = chain[block_index]

            # 1. check if previous block's hash is valid
            if cur_block['prev_hash'] != self.hash(prev_block):
                return False

            # 2. check if previous block's proof of work is valid
            prev_proof = prev_block['proof']
            cur_proof = cur_block['proof']
            hash_value = self.get_hash(cur_proof, prev_proof)
            print(f'hash value is:', hash_value)

            if hash_value[:4] != '0000':
                return False

            prev_block = cur_block
            block_index += 1

        return True

    def add_transaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.transactions.append(transaction)

        return self.get_last_block()['index'] + 1  # next block's index

    def add_node(self, node_addr):
        parsed_url = urlparse(node_addr)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            url = f'http://{node}/chain'
            print(f'url is {url}')
            resp = requests.get(url)
            print(f'resp is {resp}')
            if resp.status_code == 200:
                chain_len = resp.json()['length']
                chain = resp.json()['chain']

                if chain_len > max_length and self.is_chain_valid(chain):
                    print('longer chain found in node: ', node)
                    max_length = chain_len
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    def get_chain(self):
        return self.chain

    def mine_block(self):
        prev_block = self.get_last_block()
        pow = self.proof_of_work(prev_block['proof'])
        prev_hash = self.hash(prev_block)
        self.add_transaction(sender='mike',receiver=self.node_address,amount=1)
        block = self.create_block(pow, prev_hash)

        return block
