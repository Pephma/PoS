import random

class Algorand:
    def __init__(self, validators):
        self.validators = validators  # Lista de validadores e stakes

    def select_validator(self):
        # Seleciona um validador aleatoriamente com base no stake
        total_stake = sum(stake for _, stake in self.validators)
        selection = random.uniform(0, total_stake)

        cumulative_stake = 0
        for validator, stake in self.validators:
            cumulative_stake += stake
            if selection <= cumulative_stake:
                return validator
        return None

validators = [("Validador A", 100), ("Validador B", 200), ("Validador C", 300)]
algorand = Algorand(validators)
selected_validator = algorand.select_validator()
print(f"Validador selecionado: {selected_validator}")