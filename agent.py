import random
import json
import os

class QLearningAgent:
    def __init__(self, actions=[0, 1, 2, 3], learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = {}

    def get_action(self, state, train=True, episode=0):
        state_str = str(state)
        current_epsilon = self.epsilon * (0.9999 ** episode) if train else 0.0
        if train and random.random() < current_epsilon:
            return random.choice(self.actions)

        q_values = self.q_table.get(state_str, [0.0] * len(self.actions))
        max_q = max(q_values)
        actions_with_max_q = [i for i, v in enumerate(q_values) if v == max_q]
        return random.choice(actions_with_max_q)

    def learn(self, state, action, reward, next_state):
        state_str = str(state)
        next_state_str = str(next_state)
        if state_str not in self.q_table:
            self.q_table[state_str] = [0.0] * len(self.actions)
        next_q_values = self.q_table.get(next_state_str, [0.0] * len(self.actions))
        max_next_q = max(next_q_values)
        self.q_table[state_str][action] += self.lr * (reward + self.gamma * max_next_q - self.q_table[state_str][action])

    def save(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.q_table, f)
    def load(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.q_table = json.load(f)

            