#poker class

import player
import cards

oPlayer = player.Player
oDeck = cards.Deck

class Poker:
    STAGES = ['Pre-Flop', 'Flop', 'Turn', 'River']

    def __init__(self, starting_chips = 100):
        self.starting_chips = starting_chips
        self.players = [oPlayer("Player 0", starting_chips),
                        oPlayer("Player 1", starting_chips)]
        self.dealer = 0
        self.reset_game()
    
    def reset_game(self):
        self.deck = oDeck()
        self.deck.shuffle()
        for p in self.players:
            p.reset_hand()

        self.cards_on_table = []
        self.pot = 0
        self.current_stage = 0
        self.current_player = (self.dealer + 1) % 2
        self.current_bet = 0

        self.deal_hand_cards()

    def deal_hand_cards(self):
        for _ in range(2):
            for p in self.players:
                card = self.deck.deal(1)
                p.receive_card(card)

    def deal_flop(self):
        self.cards_on_table.extend(self.deck.deal(3))

    def deal_turn(self):
        self.cards_on_table.extend(self.deck.deal(1))
    
    def deal_river(self):
        self.cards_on_table.extend(self.deck.deal(1))