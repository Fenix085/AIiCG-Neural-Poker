#player class and functions

class Player:
    def __init__(self, name, chips):
        self.name = name
        self._chips = chips
        self._hand = []
        self._bet = 0
        self.folded = False

    def reset_hand(self):
        self._hand = []
        self._bet = 0
        self.folded = False

    def place_bet(self, amount):
        if amount > self._chips:
            raise ValueError("Not enough chips to bet that amount")
        self._chips -= amount
        self._bet += amount

    def receive_card(self, card):
        self._hand.append(card)

    def get_chips(self):
        return self._chips
    
    def get_bet(self):
        return self._bet
    
    def get_hand(self):
        return self._hand
    
    def fold(self):
        self.folded = True