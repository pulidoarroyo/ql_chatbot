# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from data import STATES, ACTIONS

class ChatbotGUI:
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.root.title("Bot Interactivo (Q-Learning) - UNEG")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f2f5")
        
        # Variables para rastrear el estado y acción de la última interacción
        self.current_state = None
        self.current_action = None
        
        self.setup_ui()
        self.update_q_table_view()

    def setup_ui(self):
        # Contenedor Principal (Dividido en 2 columnas)
        main_container = tk.Frame(self.root, bg="#f0f2f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ==========================================
        # PANEL IZQUIERDO: Chat Bot e Interacción
        # ==========================================
        left_panel = tk.LabelFrame(main_container, text=" Bot Interactivo (Q-Learning) ", font=("Arial", 12, "bold"), bg="white", fg="#1a73e8", bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Área del Historial del Chat
        self.chat_history = tk.Text(left_panel, state=tk.DISABLED, bg="#f8f9fa", font=("Arial", 10), wrap=tk.WORD)
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel de entrada de texto y envío
        entry_frame = tk.Frame(left_panel, bg="white")
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.user_entry = tk.Entry(entry_frame, font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 5))
        self.user_entry.bind("<Return>", lambda event: self.send_message())
        
        btn_send = tk.Button(entry_frame, text="Enviar", font=("Arial", 10, "bold"), bg="#1a73e8", fg="white", bd=0, command=self.send_message, width=10, cursor="hand2")
        btn_send.pack(side=tk.RIGHT)
        
        # Panel de Retroalimentación (Likes/Dislikes)
        feedback_frame = tk.Frame(left_panel, bg="white")
        feedback_frame.pack(fill=tk.X, padx=10, pady=10)
        
        lbl_feedback = tk.Label(feedback_frame, text="Evaluar respuesta anterior:", font=("Arial", 9, "italic"), bg="white", fg="#5f6368")
        lbl_feedback.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_like = tk.Button(feedback_frame, text="👍 Like (+1)", font=("Arial", 10, "bold"), bg="#28a745", fg="white", bd=0, state=tk.DISABLED, command=lambda: self.evaluate_response(1), cursor="hand2")
        self.btn_like.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=2)
        
        self.btn_dislike = tk.Button(feedback_frame, text="👎 Dislike (-1)", font=("Arial", 10, "bold"), bg="#dc3545", fg="white", bd=0, state=tk.DISABLED, command=lambda: self.evaluate_response(-1), cursor="hand2")
        self.btn_dislike.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=2)

        # ==========================================
        # PANEL DERECHO: Telemetría e IA
        # ==========================================
        right_panel = tk.LabelFrame(main_container, text=" Cerebro del Agente: Q-Learning ", font=("Arial", 12, "bold"), bg="white", fg="#202124", bd=2, width=480)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Parámetros del algoritmo
        params_frame = tk.Frame(right_panel, bg="white")
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        lbl_info = tk.Label(params_frame, text=f"Epsilon (ε): {self.agent.epsilon} (Exploración)  |  Tasa Aprendizaje (α): {self.agent.alpha}", font=("Arial", 9, "bold"), bg="#e8f0fe", fg="#1967d2", padx=5, pady=5)
        lbl_info.pack(fill=tk.X)
        
        # Visualizador de la Tabla Q (Treeview)
        table_frame = tk.Frame(right_panel, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        lbl_table_title = tk.Label(table_frame, text="Tabla Q (Estado vs Acción)", font=("Arial", 10, "bold"), bg="white", fg="#202124")
        lbl_table_title.pack(anchor=tk.W, pady=(0, 5))
        
        # Columnas de la tabla
        columns = ["Estado"] + list(ACTIONS.keys())
        self.q_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        self.q_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar cabeceras de columnas
        self.q_tree.heading("Estado", text="Estado \\ Acción")
        self.q_tree.column("Estado", width=110, anchor=tk.CENTER)
        for act in ACTIONS.keys():
            self.q_tree.heading(act, text=act)
            self.q_tree.column(act, width=75, anchor=tk.CENTER)
            
        # Panel de Actualización Matemática
        self.math_frame = tk.LabelFrame(right_panel, text=" 2. Actualización Matemática ", font=("Arial", 10, "bold"), bg="#1e293b", fg="#f8fafc", bd=1)
        self.math_frame.pack(fill=tk.X, padx=10, pady=10, ipady=10)
        
        self.lbl_formula_base = tk.Label(self.math_frame, text="Fórmula: Q(S,A) ← Q(S,A) + α · [R - Q(S,A)]", font=("Courier New", 9, "bold"), bg="#1e293b", fg="#94a3b8")
        self.lbl_formula_base.pack(anchor=tk.W, padx=10, pady=2)
        
        self.lbl_math_details = tk.Label(self.math_frame, text="Esperando interacción...", font=("Courier New", 10), bg="#1e293b", fg="#38bdf8", justify=tk.LEFT)
        self.lbl_math_details.pack(anchor=tk.W, padx=10, pady=5)

    # ==========================================
    # LÓGICA DE INTERACCIÓN Y ENLACE CON AGENTE
    # ==========================================
    def append_to_chat(self, sender, message, color="black", subtext=None):
        """Inserta texto de forma limpia en el historial del chat."""
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n", sender)
        self.chat_history.tag_config(sender, foreground=color, font=("Arial", 10, "bold" if sender != "Bot" else "normal"))
        
        if subtext:
            self.chat_history.insert(tk.END, f" {subtext}\n", "sub")
            self.chat_history.tag_config("sub", foreground="#70757a", font=("Arial", 8, "italic"))
            
        self.chat_history.insert(tk.END, "\n")
        self.chat_history.configure(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def send_message(self):
        user_text = self.user_entry.get().strip()
        if not user_text:
            return
            
        self.user_entry.delete(0, tk.END)
        self.append_to_chat("Tú", user_text, color="#202124")
        
        # 1. Determinar Estado (Intención)
        state = self.agent.get_intent(user_text)
        state_desc = STATES[state]
        
        # 2. Elegir Acción (Respuesta) usando Epsilon-Greedy
        action, explored = self.agent.choose_action(state)
        bot_response = ACTIONS[action]
        
        # Guardar contexto de la iteración actual
        self.current_state = state
        self.current_action = action
        
        # Mostrar en el chat
        strategy_info = "🤖 Exploración (Azar)" if explored else "🧠 Explotación (Conocimiento)"
        sub_msg = f"Clasificado: {state} ({state_desc}) | Modo: {strategy_info}"
        self.append_to_chat("Bot", bot_response, color="#1a73e8", subtext=sub_msg)
        
        # Habilitar botones de feedback y deshabilitar temporalmente la entrada
        self.btn_like.configure(state=tk.NORMAL)
        self.btn_dislike.configure(state=tk.NORMAL)

    def evaluate_response(self, reward):
        if self.current_state is None or self.current_action is None:
            return
            
        # 3. Aplicar Ecuación de Bellman a través del Agente
        q_old, q_new = self.agent.update_q_value(self.current_state, self.current_action, reward)
        
        # Actualizar Panel Matemático en pantalla
        reward_str = f"+1 (Like)" if reward == 1 else "-1 (Dislike)"
        math_text = (
            f"Recompensa (R) = {reward}\n"
            f"Q_anterior({self.current_state}, {self.current_action}) = {q_old}\n\n"
            f"Fórmula Aplicada:\n"
            f"Q({self.current_state}, {self.current_action}) = {q_old} + {self.agent.alpha} * ({reward} - {q_old})\n"
            f"Q_nuevo = {q_new}"
        )
        self.lbl_math_details.configure(text=math_text)
        
        # Refrescar la interfaz
        self.update_q_table_view()
        
        # Agregar confirmación visual en el chat de la recompensa otorgada
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f" [Evaluado con recompensa: {reward_str}]\n\n", "eval")
        self.chat_history.tag_config("eval", foreground="#28a745" if reward == 1 else "#dc3545", font=("Arial", 8, "bold"))
        self.chat_history.configure(state=tk.DISABLED)
        self.chat_history.see(tk.END)
        
        # Limpiar e invalidar estado hasta el siguiente mensaje
        self.current_state = None
        self.current_action = None
        self.btn_like.configure(state=tk.DISABLED)
        self.btn_dislike.configure(state=tk.DISABLED)

    def update_q_table_view(self):
        """Limpia el visor y redibuja las filas vigentes de la Tabla Q."""
        for item in self.q_tree.get_children():
            self.q_tree.delete(item)
            
        for state, actions_dict in self.agent.q_table.items():
            row_values = [f"{state}: {STATES[state]}"]
            for act in ACTIONS.keys():
                row_values.append(f"{actions_dict[act]:.2f}")
            self.q_tree.insert("", tk.END, values=row_values)