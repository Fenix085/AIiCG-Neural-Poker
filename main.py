import torch
import torch.nn.functional as F

from poker import Poker
from network import PokerNet

ACTIONS = {
    0: "fold",
    1: "call/check",
    2: "raise+10",
    3: "raise+20"
}

def ai_choose_action(policy: PokerNet, state_list):
    state = torch.tensor(state_list, dtype=torch.float32)
    logits = policy(state)
    probs = F.softmax(logits, dim=-1)
    action_id = int(torch.argmax(probs).item())
    return action_id, probs.detach().tolist()

def print_state(env: Poker, human_id: int):
    print("\n=== Table ===")
    print("Stage:", Poker.STAGES[env.current_stage])
    board = env.cards_on_table
    print("Board:", ",".join(map(str, board)) if board else "(empty)")
    print("Pot:", env._pot)

    for i, p in enumerate(env.players):
        hand = p.get_hand()
        hand_str = ", ".join(map(str, hand)) if hand else "(no cards?)"
        role = "Human" if i == human_id else "AI"
        print(f"Player {i} [{role}] chips = {p.get_chips()} bet = {p.get_bet()} folded = {p.folded} hand = {hand_str if i == human_id else hand_str + " (for debug purposes)"}")
    
    to_call = max(0, env.current_bet - env.players[human_id].get_bet())
    print("Current bet:", env.current_bet, "You need to call:", to_call)
    print("==============")

def ask_human_action():
    print("Choose action:")
    for k, v in ACTIONS.items():
        print(f"{k}: {v}")
    while True:
        s = input("Your action: ")
        if s.isdigit() and int(s) in ACTIONS:
            a = int(s)
            if a in ACTIONS:
                return int(s)
        print("Invalid action. Enter 0, 1, 2 or 3.")

def main():
    human_id = 0
    ai_id = 1

    env = Poker(starting_chips=100)

    dummy_state = env.encode_state(player_id = human_id)
    input_dim = len(dummy_state)

    policy = PokerNet(input_dim=input_dim, hidden_dim = 114, output_dim = 4)
    policy.load_state_dict(torch.load("poker_policy.pt", map_location = "cpu"))
    policy.eval()

    env.reset(player_id = human_id)
    done = False

    while not done:
        current = env.current_player

        if current == human_id:
            print_state(env, human_id)
            action_id = ask_human_action()
            _, _, done = env.step_discrete(human_id, action_id)

        else:
            state = env.encode_state(ai_id)
            action_id, probs = ai_choose_action(policy, state)
            print(f"\nAI chooses {action_id} ({ACTIONS[action_id]}) probs={['%.2f' % x for x in probs]}")
            _, _, done = env.step_discrete(ai_id, action_id)

    print_state(env, human_id)
    print("\n=== Hand over ===")
    print("Final chips:")
    print("Human:", env.players[human_id].get_chips())
    print("AI:", env.players[ai_id].get_chips())

if __name__ == "__main__":
    main()