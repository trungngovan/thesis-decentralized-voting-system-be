import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, vote_data, vote_id, user_id, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.vote_data = vote_data
        self.vote_id = vote_id
        self.user_id = user_id
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.previous_hash}{self.vote_data}{self.vote_id}{self.user_id}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:10]}...)"
