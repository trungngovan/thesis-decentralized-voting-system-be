class Consensus:
    @staticmethod
    def proof_of_work(block, difficulty=4):
        """Proof of work algorithm"""

        block.nonce = 0
        target = "0" * difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined: {block.hash}")
        return block
