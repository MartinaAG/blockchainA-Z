import datetime
import hashlib
import json
from tabnanny import check
from urllib import response
from flask import Flask, jsonify

# Part 1 - Creating a Blockchain

class Blockchain:

    # constructor
    def __init__(self):
        self.chain = []

        # the first genesis block of the chain with the default value of the hash = '0'
        self.create_block(proof = 1, previous_hash = '0')

    #  will be called right after the block has been mined and will add the block to the chain
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    # PoW is the number or piece of data that the miners needs to get to add the new block to the chain
    # this number is hard to find (to not lose its value)
    # but easy to verify (when a minor potential solve it other minors needs to verify it very quickly)
    def proof_of_work(self, previous_proof):
        # brute forcing the number starting from 1
        new_proof = 1
        check_proof = False

        while check_proof is False:
            # the problem that the miners need to solve
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            # check if the first elements are the wanted four leading zeroes
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof


    # get a block and returns its hash
    def get_hash(self, block):
        # dump() takes an object and makes it a string
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


    # check if the blockchain is correct
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # the previous hash attribute of the block is equal to the hash of the previous block
            if block['previous_hash'] != self.get_hash(previous_block):
                return False

            # each block has a correct PoW ('0000')
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            # update the iteration
            previous_block = block
            block_index += 1

        # if the chain is valid
        return True



# Part 2 - Mining our Blockchain

# Creating a web app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a blockchain
blockchain = Blockchain()

# Mining a new block

# an address that we will call when we want to mine a block
@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.get_hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    hash_with_the_leading_zeroes = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
    current_hash = blockchain.get_hash(block)

    response = {'message': 'Congratulations Marty, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'hash': current_hash,
                'proof_hash': hash_with_the_leading_zeroes}

    return jsonify(response), 200



# Getting the full blockchain

@app.route('/get_chain', methods = ['GET'])

def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200



# check if the blockchain is valid
@app.route('/is_valid', methods = ['GET'])

def is_valid():
    is_chain_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'is_chain_valid': is_chain_valid}
    return jsonify(response), 200


# Running tha app
app.run(host = '0.0.0.0', port = 5000)


