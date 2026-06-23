# agent.py
import random
import json
import os
from data import STATES, ACTIONS, KEYWORDS

Q_TABLE_FILE = "q_table.json"

class QLearningAgent:
    def __init__(self, alpha=0.5, epsilon=0.3):
        self.alpha = alpha
        self.epsilon = epsilon
        self.q_table = {s: {a: 0.0 for a in ACTIONS} for s in STATES}
        self.load_q_table()

    def get_intent(self, user_input):
        text = user_input.lower()
        for state, words in KEYWORDS.items():
            for word in words:
                if word in text:
                    return state
        return "S6"

    def choose_action(self, state):
        if random.random() < self.epsilon:
            action = random.choice(list(ACTIONS.keys()))
            return action, True
        state_actions = self.q_table[state]
        max_val = max(state_actions.values())
        best_actions = [a for a, v in state_actions.items() if v == max_val]
        return random.choice(best_actions), False

    def update_q_value(self, state, action, reward):
        q_old = self.q_table[state][action]
        q_new = q_old + self.alpha * (reward - q_old)
        self.q_table[state][action] = round(q_new, 4)
        self.save_q_table()
        return round(q_old, 4), round(q_new, 4)

    def save_q_table(self):
        with open(Q_TABLE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.q_table, f, ensure_ascii=False, indent=2)

    def load_q_table(self):
        if os.path.exists(Q_TABLE_FILE):
            try:
                with open(Q_TABLE_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                for s in self.q_table:
                    if s in saved:
                        for a in self.q_table[s]:
                            if a in saved[s]:
                                self.q_table[s][a] = saved[s][a]
            except Exception:
                pass

    def reset_q_table(self):
        self.q_table = {s: {a: 0.0 for a in ACTIONS} for s in STATES}
        self.save_q_table()