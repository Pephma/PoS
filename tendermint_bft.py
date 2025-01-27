import random

class Tendermint:
    def __init__(self, validators):
        self.validators = validators  # Lista de validadores

    def reach_consensus(self, proposed_block):
        # Simula o processo de votação para alcançar consenso
        votes = {}
        for validator in self.validators:
            # Cada validador vota no bloco proposto
            votes[validator] = "Approve" if random.random() > 0.2 else "Reject"  # 20% de chance de rejeitar

        # Contagem de votos
        approve_count = list(votes.values()).count("Approve")
        if approve_count > len(self.validators) * 2 / 3:  # Precisão de 2/3 para consenso
            return f"Consenso alcançado: Bloco {proposed_block} aceito."
        else:
            return f"Consenso não alcançado: Bloco {proposed_block} rejeitado."

# Exemplo de uso
validators = ["Validador A", "Validador B", "Validador C", "Validador D"]
tendermint = Tendermint(validators)
result = tendermint.reach_consensus("Bloco 123")
print(result)