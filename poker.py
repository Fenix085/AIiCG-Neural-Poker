#poker class

import player
import cards

oPlayer = player.Player
oDeck = cards.Deck

class Poker:
    STAGES = ['Pre-Flop', 'Flop', 'Turn', 'River']

    def __init__(self, starting_chips = 100):
        self.starting_chips = starting_chips
        self._pot = 0
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
        self._pot = 0
        self.current_stage = 0
        self.current_player = (self.dealer + 1) % 2
        self.current_bet = 0

        self.deal_hand_cards()

    def deal_hand_cards(self):
        for _ in range(2):
            for p in self.players:
                p.receive_card(self.deck.deal(1)[0])

    def deal_flop(self):
        self.cards_on_table.extend(self.deck.deal(3))

    def deal_turn(self):
        self.cards_on_table.extend(self.deck.deal(1))
    
    def deal_river(self):
        self.cards_on_table.extend(self.deck.deal(1))

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def action_handler(self, player_id, action):
        match action['type']:
            case 'fold':
                self.players[player_id].fold()
            case 'call':
                to_call = self.current_bet - self.players[player_id].get_bet()
                self.players[player_id].place_bet(to_call)
                self._pot += to_call
            case 'raise':
                to_call = self.current_bet - self.players[player_id].get_bet()
                raise_amount = action['amount']
                total_bet = to_call + raise_amount
                self.players[player_id].place_bet(total_bet)
                self._pot += total_bet
                self.current_bet += raise_amount
            case _:
                raise ValueError("Invalid action type")