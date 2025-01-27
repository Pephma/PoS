import random
from typing import List, Dict

class Validator:
    def __init__(self, id: int, stake: int):
        self.id = id 
        self.stake = stake  
        self.votes = []  

    def vote(self, block):
        vote = "Approve" if random.random() > 0.1 else "Reject"
        self.votes.append((block, vote))
        return vote

class Block:
    def __init__(self, id: int, shard_id: int, previous_block=None):
        self.id = id  # Identificador do bloco
        self.shard_id = shard_id  # Shard ao qual o bloco pertence
        self.previous_block = previous_block  # Bloco anterior na cadeia

class Shard:
    def __init__(self, shard_id: int, validators: List[Validator]):
        self.shard_id = shard_id  # Identificador do shard
        self.validators = validators  # Validadores atribuídos a este shard
        self.blocks = []  # Lista de blocos no shard

    def propose_block(self):
        # Simula a proposta de um novo bloco no shard
        block_id = len(self.blocks) + 1
        previous_block = self.blocks[-1] if self.blocks else None
        new_block = Block(block_id, self.shard_id, previous_block)
        self.blocks.append(new_block)
        return new_block

    def validate_block(self, block):
        # Simula o processo de validação do bloco pelos validadores do shard
        approve_stake = 0
        for validator in self.validators:
            vote = validator.vote(block)
            if vote == "Approve":
                approve_stake += validator.stake

        total_stake = sum(v.stake for v in self.validators)
        if approve_stake > total_stake * 2 / 3:
            return f"Bloco {block.id} no Shard {self.shard_id} finalizado com sucesso."
        else:
            return f"Bloco {block.id} no Shard {self.shard_id} não finalizado: Stake insuficiente."

class CasperFFG:
    def __init__(self, shards: List[Shard]):
        self.shards = shards  # Lista de shards na rede

    def propose_and_validate_blocks(self):

        for shard in self.shards:
            block = shard.propose_block()
            result = shard.validate_block(block)
            print(result)

def main():
    validators_shard_1 = [Validator(i, random.randint(100, 1000)) for i in range(5)]
    validators_shard_2 = [Validator(i + 5, random.randint(100, 1000)) for i in range(5)]

    shard_1 = Shard(shard_id=1, validators=validators_shard_1)
    shard_2 = Shard(shard_id=2, validators=validators_shard_2)

    casper = CasperFFG(shards=[shard_1, shard_2])

    for _ in range(3): 
        print(f"Rodada {_ + 1}:")
        casper.propose_and_validate_blocks()
        print()

if __name__ == "__main__":
    main()