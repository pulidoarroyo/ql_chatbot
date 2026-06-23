# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from data import STATES, ACTIONS

class ChatbotGUI:
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.root.title("ql_chatbot")
        self.root.geometry("1150x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f0f2f5")

        self.current_state = None
        self.current_action = None
        self.interaction_count = 0
        self._msg_counter = 0

        self._build_ui()
        self.update_q_table_view()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#1a73e8", height=38)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header,
                 text="Scholtz - Pulido",
                 font=("Arial", 10, "bold"), bg="#1a73e8", fg="white").pack(pady=8)

        main = tk.Frame(self.root, bg="#f0f2f5")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Panel izquierdo - Chat
        left = tk.LabelFrame(main, text=" Bot Interactivo (Q-Learning) ",
                             font=("Arial", 11, "bold"), bg="white",
                             fg="#1a73e8", bd=2, relief=tk.GROOVE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        chat_frame = tk.Frame(left, bg="white")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.chat_history = tk.Text(chat_frame, state=tk.DISABLED,
                                    bg="#f8f9fa", font=("Arial", 10),
                                    wrap=tk.WORD, relief=tk.FLAT, bd=0)
        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_history.yview)
        self.chat_history.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history.pack(fill=tk.BOTH, expand=True)

        entry_outer = tk.Frame(left, bg="#e8eaed", bd=1, relief=tk.SOLID)
        entry_outer.pack(fill=tk.X, padx=8, pady=(0, 5))

        self.user_entry = tk.Entry(entry_outer, font=("Arial", 11),
                                   bd=0, relief=tk.FLAT, bg="#e8eaed", fg="#9aa0a6")
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7, padx=8)
        self.user_entry.insert(0, "Escribe tu mensaje...")
        self.user_entry.bind("<Return>", lambda e: self.send_message())
        self.user_entry.bind("<FocusIn>", self._clear_ph)
        self.user_entry.bind("<FocusOut>", self._restore_ph)

        btn_send = tk.Button(entry_outer, text="Enviar",
                             font=("Arial", 10, "bold"),
                             bg="#1a73e8", fg="white", bd=0,
                             command=self.send_message, width=9,
                             cursor="hand2")
        btn_send.pack(side=tk.RIGHT, ipady=7, ipadx=4)

        fb_frame = tk.Frame(left, bg="white")
        fb_frame.pack(fill=tk.X, padx=8, pady=(4, 10))

        tk.Label(fb_frame, text="Evaluar ultima respuesta:",
                 font=("Arial", 9, "italic"), bg="white",
                 fg="#5f6368").pack(side=tk.LEFT, padx=(0, 8))

        self.btn_like = tk.Button(fb_frame, text="Like (+1)",
                                  font=("Arial", 10, "bold"),
                                  bg="#28a745", fg="white", bd=0,
                                  state=tk.DISABLED,
                                  command=lambda: self.evaluate_response(1),
                                  cursor="hand2")
        self.btn_like.pack(side=tk.LEFT, padx=4, ipadx=10, ipady=4)

        self.btn_dislike = tk.Button(fb_frame, text="Dislike (-1)",
                                     font=("Arial", 10, "bold"),
                                     bg="#dc3545", fg="white", bd=0,
                                     state=tk.DISABLED,
                                     command=lambda: self.evaluate_response(-1),
                                     cursor="hand2")
        self.btn_dislike.pack(side=tk.LEFT, padx=4, ipadx=10, ipady=4)

        # Panel derecho - IA
        right = tk.LabelFrame(main, text=" Cerebro del Agente: Q-Learning ",
                              font=("Arial", 11, "bold"), bg="white",
                              fg="#202124", bd=2, relief=tk.GROOVE, width=530)
        right.pack(side=tk.RIGHT, fill=tk.BOTH)
        right.pack_propagate(False)

        params = tk.Frame(right, bg="#e8f0fe")
        params.pack(fill=tk.X, padx=10, pady=(10, 6))

        param_lines = [
            "Estados (Intenciones): Lo que el usuario quiere decir.",
            "Acciones (Respuestas): Lo que el Bot decide contestar.",
            "Epsilon (epsilon): %s  (exploracion aleatoria)   |   Alfa (alpha): %s  (tasa de aprendizaje)" % (self.agent.epsilon, self.agent.alpha)
        ]
        for line in param_lines:
            tk.Label(params, text=line, font=("Arial", 8), bg="#e8f0fe",
                     fg="#1967d2").pack(anchor=tk.W, padx=6, pady=1)

        tk.Label(right, text="Tabla Q  (Estado vs Accion)",
                 font=("Arial", 10, "bold"), bg="white",
                 fg="#202124").pack(anchor=tk.W, padx=10, pady=(6, 2))

        table_wrap = tk.Frame(right, bg="white")
        table_wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 6))

        cols = ["Estado"] + list(ACTIONS.keys())
        self.q_tree = ttk.Treeview(table_wrap, columns=cols,
                                   show="headings", height=9)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 8, "bold"))
        style.configure("Treeview", font=("Courier New", 9), rowheight=22)

        self.q_tree.heading("Estado", text="Estado / Accion")
        self.q_tree.column("Estado", width=125, anchor=tk.W, stretch=False)

        for act_id, act_text in ACTIONS.items():
            short = act_text[:12] + ".." if len(act_text) > 12 else act_text
            self.q_tree.heading(act_id, text='%s: "%s"' % (act_id, short))
            self.q_tree.column(act_id, width=68, anchor=tk.CENTER, stretch=False)

        self.q_tree.tag_configure("odd", background="#f8f9fa")
        self.q_tree.tag_configure("even", background="white")

        h_scroll = ttk.Scrollbar(table_wrap, orient=tk.HORIZONTAL,
                                  command=self.q_tree.xview)
        self.q_tree.configure(xscrollcommand=h_scroll.set)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.q_tree.pack(fill=tk.BOTH, expand=True)

        math_outer = tk.LabelFrame(right,
                                   text=" Actualizacion Matematica (Contextual Bandit, gamma=0) ",
                                   font=("Arial", 9, "bold"),
                                   bg="#1e293b", fg="#f8fafc",
                                   bd=1, relief=tk.SOLID)
        math_outer.pack(fill=tk.X, padx=10, pady=(4, 6), ipady=4)

        tk.Label(math_outer,
                 text="Q(St, At) <- Q(St, At) + alpha * [Rt - Q(St, At)]",
                 font=("Courier New", 9, "bold"),
                 bg="#1e293b", fg="#94a3b8").pack(anchor=tk.W, padx=8, pady=(4, 2))

        self.lbl_math = tk.Label(math_outer,
                                 text="Esperando primera interaccion...",
                                 font=("Courier New", 9),
                                 bg="#1e293b", fg="#38bdf8",
                                 justify=tk.LEFT)
        self.lbl_math.pack(anchor=tk.W, padx=8, pady=(0, 4))

        status_bar = tk.Frame(right, bg="#f1f3f4")
        status_bar.pack(fill=tk.X, padx=10, pady=(0, 8))

        self.lbl_count = tk.Label(status_bar,
                                  text="Interacciones evaluadas: 0",
                                  font=("Arial", 8), bg="#f1f3f4", fg="#5f6368")
        self.lbl_count.pack(side=tk.LEFT)

        btn_reset = tk.Button(status_bar, text="Reiniciar Tabla Q",
                              font=("Arial", 8), bg="#f1f3f4", fg="#dc3545",
                              bd=0, cursor="hand2",
                              command=self._confirm_reset)
        btn_reset.pack(side=tk.RIGHT)

    def _clear_ph(self, event):
        if self.user_entry.get() == "Escribe tu mensaje...":
            self.user_entry.delete(0, tk.END)
            self.user_entry.configure(fg="black")

    def _restore_ph(self, event):
        if not self.user_entry.get():
            self.user_entry.insert(0, "Escribe tu mensaje...")
            self.user_entry.configure(fg="#9aa0a6")

    def _confirm_reset(self):
        if messagebox.askyesno("Reiniciar Tabla Q",
                               "Deseas reiniciar todos los valores Q a 0?\nSe perdera el aprendizaje acumulado."):
            self.agent.reset_q_table()
            self.interaction_count = 0
            self.lbl_count.configure(text="Interacciones evaluadas: 0")
            self.lbl_math.configure(text="Tabla Q reiniciada a 0.")
            self.update_q_table_view()

    def _insert_chat(self, text, fg, bold=False, small=False):
        self._msg_counter += 1
        tag = "t%d" % self._msg_counter
        self.chat_history.configure(state=tk.NORMAL)
        font_size = 8 if small else 10
        weight = "bold" if bold else "normal"
        self.chat_history.insert(tk.END, text, tag)
        self.chat_history.tag_config(tag, foreground=fg,
                                     font=("Arial", font_size, weight))
        self.chat_history.configure(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def send_message(self):
        user_text = self.user_entry.get().strip()
        if not user_text or user_text == "Escribe tu mensaje...":
            return

        self.user_entry.delete(0, tk.END)

        self._insert_chat("Tu: %s\n" % user_text, "#202124", bold=True)

        state = self.agent.get_intent(user_text)
        action, explored = self.agent.choose_action(state)
        bot_response = ACTIONS[action]

        self.current_state = state
        self.current_action = action

        self._insert_chat("Bot: %s\n" % bot_response, "#1a73e8")

        mode = "Exploracion (azar)" if explored else "Explotacion (mejor Q)"
        self._insert_chat(
            "   Intencion: %s (%s)  |  Accion: %s  |  %s\n\n" % (state, STATES[state], action, mode),
            "#70757a", small=True)

        self.btn_like.configure(state=tk.NORMAL)
        self.btn_dislike.configure(state=tk.NORMAL)

    def evaluate_response(self, reward):
        if self.current_state is None:
            return

        q_old, q_new = self.agent.update_q_value(
            self.current_state, self.current_action, reward)

        self.interaction_count += 1
        self.lbl_count.configure(text="Interacciones evaluadas: %d" % self.interaction_count)

        delta = round(self.agent.alpha * (reward - q_old), 4)
        math_text = (
            "Recompensa (R) = %d\n"
            "Q_anterior(%s, %s) = %s\n\n"
            "Formula aplicada:\n"
            "  Q = %s + %s * (%d - %s)\n"
            "  Q = %s + (%s)\n"
            "  Q_nuevo = %s"
        ) % (reward, self.current_state, self.current_action, q_old,
             q_old, self.agent.alpha, reward, q_old,
             q_old, delta, q_new)

        self.lbl_math.configure(text=math_text)

        reward_color = "#28a745" if reward == 1 else "#dc3545"
        reward_str = "+1" if reward == 1 else "-1"
        self._insert_chat(
            "   [Evaluado con recompensa: %s]\n\n" % reward_str,
            reward_color, small=True)

        self.update_q_table_view()
        self.current_state = None
        self.current_action = None
        self.btn_like.configure(state=tk.DISABLED)
        self.btn_dislike.configure(state=tk.DISABLED)

    def update_q_table_view(self):
        for item in self.q_tree.get_children():
            self.q_tree.delete(item)

        for i, (state, actions_dict) in enumerate(self.agent.q_table.items()):
            row = ["%s: %s" % (state, STATES[state])]
            for act in ACTIONS.keys():
                val = actions_dict[act]
                row.append("%.4f" % val)
            tag = "odd" if i % 2 == 0 else "even"
            self.q_tree.insert("", tk.END, values=row, tags=(tag,))