import hashlib
import datetime as date
import tarfile

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = date.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    """
    # create blockchain
    my_blockchain = Blockchain()

    # read data from tar.gz file
    with tarfile.open("mydata.tar.gz", "r:gz") as tar:
        data = tar.extractfile("myfile.txt").read()

    # compute hash of data
    data_hash = hashlib.sha256(data).hexdigest()

    # create new block with hash and add to blockchain
    my_blockchain.add_block(Block(data_hash, ""))

    # print the blockchain
    my_blockchain.print_chain()
    """
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Block Hash:", block.hash)
            print("Previous Hash:", block.previous_hash)
            print()