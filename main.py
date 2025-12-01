import poker

def print_state(game, stage_name):
    print(f"\n=== {stage_name} ===")
    print(f"Stage index: {game.current_stage}")
    print(f"Pot: {game._pot}")
    for i, p in enumerate(game.players):
        print(f"Player {i} ({p.name}): "
              f"chips={p.get_chips()}, bet={p.get_bet()}, folded={p.folded}")
    print("Board:", ", ".join(str(c) for c in game.cards_on_table))

if __name__ == "__main__":
    game = poker.Poker(starting_chips=100)

    print("Game initialized with players:")
    for i, p in enumerate(game.players):
        print(f"Player {i}: {p.name} with {p.get_chips()} chips")

    # Hands were probably already dealt in reset_game(), but if not:
    # game.deal_hand_cards()

    print("\nInitial hands:")
    for i, p in enumerate(game.players):
        print(f"Player {i} hand: " + ", ".join(str(c) for c in p.get_hand()))

    # --- PRE-FLOP ---

    preflop_actions = [
        {'type': 'raise', 'amount': 10},
        {'type': 'call'},
    ]

    print_state(game, "Preflop start")

    for action in preflop_actions:
        print(f"\nCurrent player: {game.current_player}, action: {action}")
        done = game.step(action)   # your step() should return whether hand is over
        print_state(game, "After action")
        if done:
            print("\nHand ended during preflop.")
            break

    if not done:
        # Stage should have advanced in step() to flop, or you manually call:
        # game.move_stage()
        print("\nDealing flop...")
        # game.deal_flop()
        print_state(game, "After flop")

        # --- FLOP ---

        flop_actions = [
            {'type': 'call'},
            {'type': 'call'},
        ]

        for action in flop_actions:
            print(f"\nCurrent player: {game.current_player}, action: {action}")
            done = game.step(action)
            print_state(game, "After flop action")
            if done:
                print("\nHand ended during flop.")
                break

    if not done:
        # Again, either step() moves stage, or you call:
        # game.move_stage()
        print("\nDealing turn...")
        # game.deal_turn()
        print_state(game, "After turn card dealt")

        # --- TURN ---

        turn_actions = [
            {'type': 'raise', 'amount': 20},
            {'type': 'fold'},
        ]

        for action in turn_actions:
            print(f"\nCurrent player: {game.current_player}, action: {action}")
            done = game.step(action)
            print_state(game, "After turn action")
            if done:
                print("\nHand ended during turn.")
                break

    print("\n=== Final state after hand ===")
    print_state(game, "End of hand")
