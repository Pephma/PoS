import hashlib
import random
from typing import List
import matplotlib.pyplot as plt

class Stakeholder:
    def __init__(self, address: str, stake: int):
        self.address = address
        self.stake = stake
        self.blocks_proposed = 0

    def __repr__(self):
        return f"Stakeholder(address={self.address}, stake={self.stake}, blocks_proposed={self.blocks_proposed})"


class Block:
    def __init__(self, slot: int, proposer: Stakeholder):
        self.slot = slot
        self.proposer = proposer

    def __repr__(self):
        return f"Block(slot={self.slot}, proposer={self.proposer.address})"


class Ouroboros:
    def __init__(self, stakeholders: List[Stakeholder], slots_per_epoch: int = 10):
        self.stakeholders = stakeholders
        self.slots_per_epoch = slots_per_epoch
        self.blocks: List[Block] = []

    def get_total_stake(self):
        return sum(s.stake for s in self.stakeholders)

    def vrf(self, seed: str, stakeholder: Stakeholder) -> float:
        """
        Simulate a Verifiable Random Function (VRF) for slot leader selection.
        """
        input_data = f"{seed}-{stakeholder.address}".encode()
        hash_value = hashlib.sha256(input_data).hexdigest()
        return int(hash_value, 16) / (2 ** 256)

    def select_slot_leader(self, seed: str) -> Stakeholder:
        """
        Select a slot leader based on stake-weighted randomness.
        """
        total_stake = self.get_total_stake()
        selection = random.uniform(0, total_stake)
        cumulative_stake = 0
        for stakeholder in self.stakeholders:
            cumulative_stake += stakeholder.stake
            if selection <= cumulative_stake:
                return stakeholder
        raise RuntimeError("No stakeholder selected")

    def run_epoch(self, epoch: int):
        """
        Simulate an epoch with multiple slots.
        """
        print(f"\n--- Epoch {epoch} ---")
        seed = f"epoch-{epoch}-seed"
        for slot in range(self.slots_per_epoch):
            slot_leader = self.select_slot_leader(seed)
            block = Block(slot, slot_leader)
            self.blocks.append(block)
            slot_leader.blocks_proposed += 1
            print(f"Slot {slot}: Block proposed by {slot_leader.address} (Stake: {slot_leader.stake})")

    def simulate(self, epochs: int = 3):
        for epoch in range(epochs):
            self.run_epoch(epoch)

    def plot_block_distribution(self):
        stakeholders = [s.address for s in self.stakeholders]
        blocks_proposed = [s.blocks_proposed for s in self.stakeholders]

        plt.figure(figsize=(12, 6))
        plt.bar(stakeholders, blocks_proposed, color='skyblue')
        plt.xlabel("Stakeholders")
        plt.ylabel("Blocks Proposed")
        plt.title("Block Proposal Distribution Among Stakeholders")
        plt.show()

    def plot_stake_distribution(self):
        """
        Plot a pie chart showing the stake distribution among stakeholders.
        """
        stakeholders = [s.address for s in self.stakeholders]
        stakes = [s.stake for s in self.stakeholders]

        plt.figure(figsize=(8, 8))
        plt.pie(stakes, labels=stakeholders, autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightcoral', 'lightskyblue', 'gold', 'lightpink', 'lightblue'])
        plt.title("Stake Distribution Among Stakeholders")
        plt.show()

    def print_detailed_info(self):
        print("\n--- Detailed Stakeholder Information ---")
        for stakeholder in self.stakeholders:
            print(stakeholder)

        print("\n--- Block Information ---")
        for block in self.blocks:
            print(block)


if __name__ == "__main__":
    stakeholders = [
        Stakeholder("Stakeholder1", 1000),
        Stakeholder("Stakeholder2", 2000),
        Stakeholder("Stakeholder3", 1500),
        Stakeholder("Stakeholder4", 2500),
        Stakeholder("Stakeholder5", 1200),
        Stakeholder("Stakeholder6", 1800),
    ]

    ouroboros = Ouroboros(stakeholders, slots_per_epoch=5)

    ouroboros.simulate(epochs=3)

    ouroboros.print_detailed_info()

    ouroboros.plot_block_distribution()

    ouroboros.plot_stake_distribution()