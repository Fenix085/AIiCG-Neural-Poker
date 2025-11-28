import poker

if __name__ == "__main__":
    game = poker.Poker()
    print("Game initialized with players:")
    for player in game.players:
        print(f"{player.name} with {player.get_chips()} chips")

    game.deal_hand_cards()
    for player in game.players:
        print(f"{player.name}'s hand:")
        for card in player.get_hand():
            print(card)
   
    game.deal_flop()
    print("Cards on table after flop:")
    for card in game.cards_on_table:
        print(card)
    

    game.deal_turn()
    print("Cards on table after turn:")
    for card in game.cards_on_table:
        print(card)
    game.deal_river()

    print("Cards on table after river:")
    for card in game.cards_on_table:
        print(card)
    
    print("Game reset.")
    game.reset_game()