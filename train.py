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
            next_state, reward, done = env.step_discrete(learner_id, action_id)
            log_probs.append(log_prob)
        else:
            odd_action_id = random_action_id()
            _, _, done = env.step_discrete(1 - learner_id, odd_action_id)
            reward = 0.0

    total_reward = reward
    return log_probs, total_reward

def train(num_episodes: int = 1000, learner_id: int = 0):
    env = Poker(starting_chips=100)
    dummy_state = env.encode_state(learner_id)
    input_dim = len(dummy_state)

    policy = PokerNet(input_dim=input_dim, hidden_dim = 114, output_dim = 4)
    optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)

    for episode in range(num_episodes):
        log_probs, total_reward = run_episode(env, policy, learner_id)

        G = torch.tensor(total_reward, dtype = torch.float32)

        if log_probs:
            log_probs_tensor = torch.stack(log_probs)
            loss = -G * log_probs_tensor.sum()
        else:
            loss = torch.tensor(0.0)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}, total_reward = {total_reward}, loss = {loss.item():.3f}")

    return policy

if __name__ == "__main__":
    trained_policy = train(num_episodes=1000, learner_id=0)
    torch.save(trained_policy.state_dict(), "poker_policy.pt")