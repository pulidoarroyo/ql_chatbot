# gui.py
import tkinter as tk
from tkinter import ttk

class ChatbotGUI:
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.root.title("Bot Interactivo Q-Learning - UNEG")
        self.root.geometry("900x600")
        
        # Variables de estado temporal para la última interacción
        self.current_state = None
        self.current_action = None

        self.setup_ui()

    def setup_ui(self):
        """Configura los paneles izquierdo (Chat) y derecho (Tabla Q y Matemáticas)."""
        # TODO: Crear Frame para el chat (área de texto, entry, botón enviar)
        # TODO: Crear Frame para los botones Like/Dislike
        # TODO: Crear Frame (Treeview) para mostrar la Tabla Q en tiempo real
        # TODO: Crear Frame para mostrar la fórmula y variables aplicadas
        pass

    def send_message(self):
        """Procesa el mensaje del usuario, obtiene respuesta del agente y actualiza el chat."""
        # TODO: Leer el input del usuario, llamar a agent.get_intent() y agent.choose_action()
        # TODO: Mostrar la respuesta en el chat y habilitar botones Like/Dislike
        pass

    def evaluate_response(self, reward):
        """Se ejecuta al presionar Like (+1) o Dislike (-1)."""
        # TODO: Llamar a agent.update_q_value() con self.current_state, self.current_action y reward
        # TODO: Actualizar la vista de la Tabla Q y el panel de matemáticas en la interfaz
        pass