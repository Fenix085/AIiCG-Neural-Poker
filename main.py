import random
from poker import Poker

ACTIONS = [0, 1, 2, 3]  # 0=fold, 1=call, 2=raise+10, 3=raise+20

def random_policy(state):
    """Completely dumb policy: ignores state, picks random action id."""
    return random.choice(ACTIONS)

def print_state(game, title: str):
    print(f"\n=== {title} ===")
    print(f"Stage: {Poker.STAGES[game.current_stage]}")
    print(f"Pot: {game._pot}")
    print("Board:", ", ".join(str(c) for c in game.cards_on_table) or "(empty)")
    for i, p in enumerate(game.players):
        print(
            f"Player {i}: chips={p.get_chips()}, bet={p.get_bet()}, "
            f"folded={p.folded}, hand=" +
            ", ".join(str(c) for c in p.get_hand())
        )

def play_one_random_hand():
    game = Poker(starting_chips=100)

    # From the agent's POV we need a player_id.
    # Let's pretend we're watching Player 0.
    player_id = 0
    state = game.reset(player_id)

    print("Game initialized.")
    print_state(game, "Start of hand")

    done = False
    step_idx = 0

    while not done:
        current_player = game.current_player

        # Encode state for the CURRENT player (optional; for random policy we don't use it)
        state = game.encode_state(current_player)

        # Pick action id
        action_id = random_policy(state)
        action = game.action_from_id(action_id)

        print(
            f"\nStep {step_idx}: Player {current_player}'s turn. "
            f"Action id={action_id}, action={action}"
        )

        # You can either use step() with dict:
        # done = game.step(action)
        # or the discrete wrapper (from the POV of current_player):
        next_state, reward, done = game.step_discrete(current_player, action_id)

        print_state(game, "After action")

        if done:
            print(f"\nHand ended. Last action by Player {current_player}.")
            print(f"Reward for Player 0 this step (if using RL): {reward}")
            break

        step_idx += 1

    print("\n=== Final chip counts ===")
    for i, p in enumerate(game.players):
        print(f"Player {i}: {p.get_chips()} chips")

if __name__ == "__main__":
    play_one_random_hand()
