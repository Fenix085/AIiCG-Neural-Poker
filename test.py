import pytest
from poker import *
from cards import Card

def test_pair_detection():
    evaluator = HandEvaluator()
    
    # Create hole cards with a pair of Kings (rank 11)
    hole = [Card(Card.SUITS[0], 'King'), Card(Card.SUITS[2], 'King')]
    
    # Board cards (no pairs)
    board = [
        Card(Card.SUITS[0], '2'),
        Card(Card.SUITS[0], '3'),
        Card(Card.SUITS[0], '4'),
        Card(Card.SUITS[0], '5'),
        Card(Card.SUITS[0], '6'),
    ]
    
    result = evaluator.score(hole, board)
    
    # Should return ONE_PAIR (1) with pair rank 11 (King)
    assert result[0] == HandEvaluator.ONE_PAIR
    assert result[1] == 11  # King's rank index

def test_pair_beats_high_card():
    evaluator = HandEvaluator()
    
    # Hand with pair of 2s
    pair_hole = [Card(Card.SUITS[0], '2'), Card(Card.SUITS[1], '2')]
    # Hand with Ace high (no pair)
    high_hole = [Card(Card.SUITS[0], 'Ace'), Card(Card.SUITS[1], 'King')]
    
    board = [
        Card(Card.SUITS[2], '3'),
        Card(Card.SUITS[2], '5'),
        Card(Card.SUITS[2], '7'),
        Card(Card.SUITS[2], '9'),
        Card(Card.SUITS[2], 'Jack'),
    ]
    
    pair_score = evaluator.score(pair_hole, board)
    high_score = evaluator.score(high_hole, board)
    
    # Pair should beat high card (tuples compare element-wise)
    assert pair_score > high_score