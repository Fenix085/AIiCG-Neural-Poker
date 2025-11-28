#player class and functions

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.bet = 0
        self.folded = False

    def reset_hand(self):
        self.hand = []
        self.bet = 0
        self.folded = False

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips to bet that amount")
        self.chips -= amount
        self.bet += amount