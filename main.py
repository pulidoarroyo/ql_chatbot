# main.py
import tkinter as tk
from agent import QLearningAgent
from gui import ChatbotGUI

def main():
    # 1. Instanciar el agente de Inteligencia Artificial
    agent = QLearningAgent(alpha=0.5, epsilon=0.3)
    
    # 2. Inicializar la ventana principal de Tkinter
    root = tk.Tk()
    
    # 3. Conectar la interfaz gráfica con el agente
    app = ChatbotGUI(root, agent)
    
    # 4. Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()