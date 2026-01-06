import torch
import torch.nn as nn
import torch.nn.functional as F



class PokerNet(nn.Module):
     def __init__(self, input_dim: int, hidden_dim: int = 114, output_dim: int = 4):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

     def forward(self, x):
          """
          x: tensor of shape [input_dim]
          returns: logits of shape [output_dim]
          """
          x = F.relu(self.fc1(x))
          logits = self.fc2(x)
          return logits
     
def select_action(policy: PokerNet, state):
     """
     state: Python list of floats from encode_state
     returns: (action_id, log_prob_of_action)
     """
     state_tensor = torch.tensor(state, dtype = torch.float32)
     logits = policy(state_tensor)
     probs = F.softmax(logits, dim=-1)
     dist = torch.distributions.Categorical(probs)
     action_id = dist.sample()
     log_prob = dist.log_prob(action_id)
     return int(action_id.item()), log_prob