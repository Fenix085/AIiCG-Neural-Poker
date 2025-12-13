#poker class

import player
import cards

oPlayer = player.Player
oDeck = cards.Deck
oCard = cards.Card

class Poker:
    STAGES = ['Pre-Flop', 'Flop', 'Turn', 'River']

    def __init__(self, starting_chips = 100):
        self.starting_chips = starting_chips
        self._pot = 0
        self.players = [oPlayer("Player 0", starting_chips),
                        oPlayer("Player 1", starting_chips)]
        self.dealer = 0
        self.evaluator = HandEvaluator()
        self.reset_game()

    def reset(self, player_id: int = 0):
        self.reset_game()
        return self.encode_state(player_id)

    
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
            
    def action_from_id(self, action_id):
        match action_id:
            case 0:
                return {'type': 'fold'}
            case 1:
                return {'type': 'call'}
            case 2:
                return {'type': 'raise', 'amount': 10}
            case 3:
                return {'type': 'raise', 'amount': 20}
            case _:
                raise ValueError("Invalid action id")
            
    def handle_showdown(self):
        active_players = [(i, p) for i, p in enumerate(self.players) if not p.folded]
        
        if len(active_players) == 1:
            # fold case: only one player left, they get the pot
            winner_id, winner = active_players[0]
        else:
            scored = []
            for i, _ in active_players:
                hole_cards = self.players[i].get_hand()
                board_cards = self.cards_on_table
                score = self.evaluator.score_high_card(hole_cards, board_cards)
                scored.append((i, score))

            best_score = max(score for _, score in scored)
            best_players = [i for i, score in scored if score == best_score]

            winner_id = best_players[0]
            winner = self.players[winner_id]
        
        winner.add_chips(self._pot)
        self._pot = 0
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
    
    def multi_hot_hole_cards(self, player_id) -> list:
        vec = [0.0] * 52
        hand = self.players[player_id].get_hand()
        for card in hand:
            card_id = oCard.encode_card(card)
            vec[card_id] = 1.0
        return vec
    
    def multi_hot_board_cards(self) -> list:
        vec = [0.0] * 52
        for card in self.cards_on_table:
            card_id = oCard.encode_card(card)
            vec[card_id] = 1.0
        return vec
    
    def encode_state(self, player_id):
        hole_vec = self.multi_hot_hole_cards(player_id)
        board_vec = self.multi_hot_board_cards()

        player = self.players[player_id]
        opponent = self.players[1 - player_id]

        scale = float(self.starting_chips)
        stacks = [player.get_chips() / scale, opponent.get_chips() / scale]
        pot_feat = [self._pot / scale]
        to_call = max(0, self.current_bet - player.get_bet())
        to_call_feat = [to_call / scale]

        stage_vec = [0.0] * len(Poker.STAGES)
        stage_vec[self.current_stage] = 1.0

        is_button = 1.0 if player_id == self.dealer else 0.0
        is_first = 1.0 if player_id == (self.dealer + 1) % len(self.players) else 0.0
        position_feat = [is_button, is_first]

        state = (
            hole_vec +
            board_vec +
            stacks +
            pot_feat +
            to_call_feat +
            stage_vec +
            position_feat
        )
        return state
    
class HandEvaluator:
    def score_high_card(self, hole_cards, board_cards):
        all_cards = hole_cards + board_cards
        best_rank = max(card.rank for card in all_cards)
        return best_rank