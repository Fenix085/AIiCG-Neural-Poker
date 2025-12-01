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
            
    def handle_showdown(self):
        # find players who did NOT fold
        active_players = [p for p in self.players if not p.folded]

        if len(active_players) == 1:
            # fold case: only one player left, they get the pot
            winner = active_players[0]
        else:
            # TODO: proper hand evaluation here for real showdown
            # for now you can just pick the first active player
            winner = active_players[0]

        winner._chips += self._pot
        self._pot = 0

        # Optional: reset bets at end of hand
        for p in self.players:
            p._bet = 0
            
    def move_stage(self):
        if self.current_stage == 0:
            self.deal_flop()
        elif self.current_stage == 1:
            self.deal_turn()
        elif self.current_stage == 2:
            self.deal_river()
        elif self.current_stage == 3:
            self.handle_showdown()
            return
        
        self.current_stage += 1
        self.current_bet = 0
        for p in self.players:
            p._bet = 0

    def step(self, action):
        self.action_handler(self.current_player, action)
        folded_count = sum(1 for p in self.players if p.folded)
        if folded_count == len(self.players) - 1:
            self.handle_showdown()
            return True
        
        self.next_player()
        if self.current_player == (self.dealer + 1) % len(self.players):
            self.move_stage()
        return False