import random
import torch
from poker import Poker
from network import PokerNet, select_action

ACTIONS = [0, 1, 2, 3]  # 0=fold, 1=call, 2=raise+10, 3=raise+20

def random_action_id():
    return random.choice(ACTIONS)

def run_episode(env: Poker, policy: PokerNet, learner_id: int = 0):
    state = env.reset(player_id = learner_id)

    log_probs = []
    done = False

    while not done:
        current = env.current_player

        if current == learner_id:
            state = env.encode_state(learner_id)
            action_id, log_prob = select_action(policy, state)
            _, _, done = env.step_discrete(learner_id, action_id)
            log_probs.append(log_prob)
        else:
            odd_action_id = random_action_id()
            _, _, done = env.step_discrete(1 - learner_id, odd_action_id)

    final_chips = env.players[learner_id].get_chips()
    start_chips = env.episode_start_chips[learner_id]
    total_reward = final_chips - start_chips

    return log_probs, total_reward

def train(num_episodes: int = 1000, learner_id: int = 0):
    env = Poker(starting_chips=100)
    dummy_state = env.encode_state(learner_id)
    input_dim = len(dummy_state)

    policy = PokerNet(input_dim=input_dim, hidden_dim = 114, output_dim = 4)
    optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)

    rewards_window = []
    WINDOW = 100

    for episode in range(num_episodes):
        learner = random.choice([0, 1])
        log_probs, total_reward = run_episode(env, policy, learner_id=learner)

        rewards_window.append(float(total_reward))
        if len(rewards_window) > WINDOW:
            rewards_window.pop(0)

        if log_probs:
            G = torch.tensor(total_reward / 100.0, dtype=torch.float32)
            log_probs_tensor = torch.stack(log_probs)
            loss = -G * log_probs_tensor.sum()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        else:
            loss = torch.tensor(0.0)

        if (episode + 1) % WINDOW == 0:
            avg_reward = sum(rewards_window) / len(rewards_window)
            win_rate = sum(1 for r in rewards_window if r > 0) / len(rewards_window)
            zero_rate = sum(1 for r in rewards_window if r == 0) / len(rewards_window)

            print(
                f"Episode {episode+1} | "
                f"avg_reward({WINDOW})={avg_reward:.2f} | "
                f"win_rate({WINDOW})={win_rate*100:.1f}% | "
                f"zero_rate({WINDOW})={zero_rate*100:.1f}% | "
                f"last_reward={total_reward} | "
                f"loss={loss.item():.3f}"
            )
        if (episode + 1) % 500 == 0:
            avg0, win0 = evaluate(policy, 200, learner_id=0)
            avg1, win1 = evaluate(policy, 200, learner_id=1)
            print(f"[EVAL P0] avg={avg0:.2f} win={win0*100:.1f}% | [EVAL P1] avg={avg1:.2f} win={win1*100:.1f}%")


    return policy

def debug_random_rewards(num_hands=50):
    env = Poker(starting_chips=100)

    for ep in range(num_hands):
        env.reset(0)   # or env.reset_game() after you move start_chips out
        start = env.players[0].get_chips()
        done = False
        while not done:
            current = env.current_player
            a = random_action_id()
            _, _, done = env.step_discrete(current, a)
        end = env.players[0].get_chips()
        print(f"hand {ep+1}: start={start}, end={end}, delta={end-start}")
    
@torch.no_grad()
def evaluate(policy, num_hands=200, learner_id=0):
    env = Poker(starting_chips=100)
    rewards = []
    for _ in range(num_hands):
        _, r = run_episode(env, policy, learner_id)
        rewards.append(float(r))
    avg = sum(rewards) / len(rewards)
    win = sum(1 for x in rewards if x > 0) / len(rewards)
    return avg, win


if __name__ == "__main__":
    trained_policy = train(num_episodes=10000, learner_id=0)
    torch.save(trained_policy.state_dict(), "poker_policy.pt")
    # debug_random_rewards()