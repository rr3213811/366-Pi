import hashlib
import json

class DataStoreObject:
    def __init__(self, index, data, prev_hash, correction_value=0):
        self.index = index
        self.data = data
        self.prev_hash = prev_hash
        self.correction_value = correction_value
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the hash of the data store object using cryptographic algorithm.
        """
        data_string = json.dumps({
            'index': self.index,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'correction_value': self.correction_value
        }, sort_keys=True).encode()

        return hashlib.sha256(data_string).hexdigest()

    def update_correction_value(self, target_pattern):
        """
        Update the correction value to meet the specified hash pattern.
        """
        self.correction_value = 0
        while not self.current_hash.startswith(target_pattern):
            self.correction_value += 1
            self.current_hash = self.calculate_hash()

    def update_hash(self):
        """
        Update the hash of the object based on the new Correction Value.
        """
        self.current_hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_initial_block()]

    def create_initial_block(self):
        """
        Create the initial block with 0000 as the Prev Hash.
        """
        return DataStoreObject(index=1, data="Initial Block", prev_hash="0000")

    def add_data(self, data):
        """
        Add new data to the blockchain.
        """
        index = len(self.chain) + 1
        prev_hash = self.chain[-1].current_hash
        new_block = DataStoreObject(index, data, prev_hash)
        self.chain.append(new_block)
        return new_block

    def find_and_update_correction_value(self, target_pattern, index):
        """
        Find a particular object's Correction Value and update its hash.
        """
        obj = self.chain[index - 1]
        obj.update_correction_value(target_pattern)
        # Update hashes for subsequent blocks
        for block in self.chain[index:]:
            block.update_hash()

    def is_valid(self):
        """
        Check if the blockchain is valid by verifying hashes.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.current_hash != current_block.calculate_hash():
                return False
            
            if current_block.prev_hash != prev_block.current_hash:
                return False
        
        return True

# Testing the blockchain
if __name__ == "__main__":
    blockchain = Blockchain()

    # Adding some data
    blockchain.add_data("Data 1")
    blockchain.add_data("Data 2")
    blockchain.add_data("Data 3")

    # Output the blockchain
    for block in blockchain.chain:
        print(f"Index: {block.index}, Data: {block.data}, Prev Hash: {block.prev_hash}, Correction Value: {block.correction_value}, Current Hash: {block.current_hash}")

    # Check validity
    print("Blockchain is valid:", blockchain.is_valid())

    # Update correction value and hash
    blockchain.find_and_update_correction_value("0000", 2)

    # Output the blockchain after correction value update
    for block in blockchain.chain:
        print(f"Index: {block.index}, Data: {block.data}, Prev Hash: {block.prev_hash}, Correction Value: {block.correction_value}, Current Hash: {block.current_hash}")
