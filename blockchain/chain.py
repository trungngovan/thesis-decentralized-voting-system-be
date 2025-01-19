from blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.votes = {}  # Theo dõi user đã vote trong từng vote_id

    def create_genesis_block(self):
        return Block(index=0, previous_hash="0", vote_data="Genesis Block", vote_id=0, user_id=0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, vote_data, vote_id, user_id):
        if self.has_user_voted(vote_id, user_id):
            raise ValueError("User has already voted in this vote!")

        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            vote_data=vote_data,
            vote_id=vote_id,
            user_id=user_id,
        )
        if self.is_valid_block(new_block, previous_block):
            self.chain.append(new_block)
            self.record_vote(vote_id, user_id)
        else:
            raise ValueError("Invalid block!")

    def has_user_voted(self, vote_id, user_id):
        return user_id in self.votes.get(vote_id, set())

    def record_vote(self, vote_id, user_id):
        if vote_id not in self.votes:
            self.votes[vote_id] = set()
        self.votes[vote_id].add(user_id)

    def is_valid_block(self, new_block, previous_block):
        if new_block.previous_hash != previous_block.hash:
            return False
        if new_block.hash != new_block.calculate_hash():
            return False
        return True
