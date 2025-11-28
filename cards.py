#cards and deck classes
import random

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit, value):
        if suit not in Card.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if value not in Card.VALUES:
            raise ValueError(f"Invalid value: {value}")

        self.suit = suit
        self.value = value
        self.rank = Card.VALUES.index(value)

    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    @classmethod
    def encode_card(cls, card) -> int:
        suit_index = cls.SUITS.index(card.suit)
        value_index = cls.VALUES.index(card.value)
        return suit_index * len(cls.VALUES) + value_index
    
    @classmethod
    def decode_card(cls, id) -> "Card":
        suit_index = id // len(cls.VALUES)
        value_index = id % len(cls.VALUES)
        return cls(cls.SUITS[suit_index], cls.VALUES[value_index])
    

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.SUITS for value in Card.VALUES]
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards