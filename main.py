# main.py
import tkinter as tk
from agent import QLearningAgent
from gui import ChatbotGUI

def main():
    agent = QLearningAgent(alpha=0.5, epsilon=0.3)
    
    root = tk.Tk()
    
    app = ChatbotGUI(root, agent)
    
    root.mainloop()

if __name__ == "__main__":
    main()