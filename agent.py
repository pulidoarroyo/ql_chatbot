# agent.py
import random
import numpy as np
from data import STATES, ACTIONS, KEYWORDS

class QLearningAgent:
    def __init__(self, alpha=0.5, epsilon=0.3):
        self.alpha = alpha      # Tasa de aprendizaje
        self.epsilon = epsilon  # Tasa de exploración
        
        # Inicializar la Tabla Q con ceros
        # Filas = Estados (S0, S1...), Columnas = Acciones (A0, A1...)
        self.q_table = {s: {a: 0.0 for a in ACTIONS} for s in STATES}

    def get_intent(self, user_input):
        """
        Clasifica el texto del usuario en un Estado (S).
        Retorna la clave del estado (ej. 'S0').
        """
        user_input = user_input.lower()
        # TODO: Implementar la lógica para buscar palabras clave y retornar el Estado
        pass

    def choose_action(self, state):
        """
        Selecciona una Acción (A) basada en el Estado (S) usando la política Epsilon-Greedy.
        Retorna la clave de la acción (ej. 'A0').
        """
        # TODO: Implementar exploración (random) vs explotación (mejor valor en Q-Table)
        pass

    def update_q_value(self, state, action, reward):
        """
        Aplica la ecuación de Bellman simplificada (Contextual Bandit).
        Q(S, A) <- Q(S, A) + alpha * [R - Q(S, A)]
        """
        # TODO: Actualizar el valor en self.q_table y retornar el nuevo valor para la GUI
        pass