# agent.py
import random
from data import STATES, ACTIONS, KEYWORDS

class QLearningAgent:
    def __init__(self, alpha=0.5, epsilon=0.3):
        self.alpha = alpha      # Tasa de aprendizaje (learning rate)
        self.epsilon = epsilon  # Tasa de exploración (exploration rate)
        
        # Inicializar Tabla Q: { 'S0': {'A0': 0.0, 'A1': 0.0...}, 'S1': {...} }
        self.q_table = {s: {a: 0.0 for a in ACTIONS} for s in STATES}

    def get_intent(self, user_input):
        """
        Clasifica el texto del usuario buscando palabras clave.
        Si no encuentra coincidencia, cae en S3 (Desconocido).
        """
        text = user_input.lower()
        
        for state, words in KEYWORDS.items():
            for word in words:
                if word in text:
                    return state
        return "S3"

    def choose_action(self, state):
        """
        Selecciona una acción usando la política Epsilon-Greedy.
        - Con probabilidad epsilon: Explora (acción al azar).
        - Con probabilidad 1-epsilon: Explota (mejor acción actual).
        Retorna: (ID_acción, es_exploración)
        """
        # Mecanismo de Exploración
        if random.random() < self.epsilon:
            action = random.choice(list(ACTIONS.keys()))
            return action, True
        
        # Mecanismo de Explotación (Buscar el valor máximo en la fila del estado)
        state_actions = self.q_table[state]
        max_val = max(state_actions.values())
        
        # Si hay empate en los valores Q, elegimos uno al azar entre los mejores
        best_actions = [a for a, val in state_actions.items() if val == max_val]
        action = random.choice(best_actions)
        
        return action, False

    def update_q_value(self, state, action, reward):
        """
        Aplica la ecuación del Contextual Bandit:
        Q(S, A) = Q(S, A) + alpha * [R - Q(S, A)]
        Returns:
            q_old: El valor que tenía antes de la actualización.
            q_new: El nuevo valor calculado.
        """
        q_old = self.q_table[state][action]
        
        # Aplicación directa de la fórmula simplificada
        q_new = q_old + self.alpha * (reward - q_old)
        
        # Guardar en la tabla Q
        self.q_table[state][action] = round(q_new, 2) # Redondeamos a 2 decimales para la GUI
        
        return q_old, self.q_table[state][action]

