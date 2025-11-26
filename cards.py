#cards and deck classes

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.rank = Card.VALUES.index(value)

    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    @staticmethod
    def encode_card(cls, card) -> int:
        suit_index = cls.SUITS.index(card.suit)
        value_index = cls.VALUES.index(card.value)
        return suit_index * len(cls.VALUES) + value_index
    

class Deck:
    pass