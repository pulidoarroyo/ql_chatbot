# ql_chatbot - Interactive Chatbot with Q-Learning Reinforcement Learning

This project is an interactive desktop chatbot developed in Python using the **Tkinter** graphical library. The bot uses the **Q-Learning** reinforcement learning algorithm (simplified as a *Contextual Bandit* with a discount factor $\gamma = 0$) to dynamically learn to respond optimally based on the user's intent and real-time feedback (Likes/Dislikes).

## 🚀 Features

- **Keyword-based Intent Classification**: Detects intents such as greetings, inquiries about prices, hours, location, technical support, and farewells.
- **Epsilon-Greedy Decision Making**: Balanced alternation between exploration (random actions to discover new responses) and exploitation (selecting the best learned response).
- **Interactive Feedback**: The user can rate the bot's responses (+1 / -1) to update the Q-values table.
- **Real-Time Visualization**:
  - Displays the updated Q-value table.
  - Step-by-step visualization of the mathematical formula applied in each update.
  - Color-coded chat history.
- **Persistence**: The Q-table is automatically saved in a `q_table.json` file.

---

## 📁 Project Structure

The project is organized as follows:

```text
ql_chatbot/
│
├── main.py          # Application entry point. Initializes the agent and launches the Tkinter interface.
├── q_table.json     # Persistent JSON file where trained Q-table values are saved.
├── README.md        # Project structure and requirements documentation.
├── .gitignore       # Git ignore file.
└── src/             # Source files directory.
    ├── __init__.py  # Marks the src directory as a Python package.
    ├── agent.py     # QLearningAgent class. Implements agent logic, action selection, and Q-value updates.
    ├── data.py      # Definition of States (Intents), Actions (Responses), and Keywords for matching.
    └── gui.py       # ChatbotGUI class. Interactive graphical interface and agent visualizations in Tkinter.
```

---

## 🛠️ Project Requirements

### System Requirements
- **Python 3.x** installed on the system.

### Dependencies
The project uses native Python libraries, so it **does not require installing third-party dependencies** (`pip install`).
- `tkinter` (included by default in most Python distributions).
- `random` (Python standard library).
- `json` (Python standard library).
- `os` (Python standard library).

*Note for Linux systems:* If you run the application on Linux and have issues opening the graphical interface, make sure to install Tkinter by running:
```bash
sudo apt-get install python3-tk
```

---

## ⚙️ How to Run the Project

1. Clone or download the repository to your local machine.
2. Open a terminal in the project's root directory: `ql_chatbot`.
3. Run the following command to start the chatbot:
   ```bash
   python main.py
   ```

---

## 🧠 How Does the Artificial Intelligence Work?

The AI agent models the problem as a **Contextual Bandit** (a special case of Q-Learning where the future state does not depend on the current action, hence, the discount factor $\gamma = 0$):

### 1. States and Intents
The bot classifies the text entered by the user into one of the following states (intents defined in `data.py`):
- `S0`: Greeting (Saludo)
- `S1`: Price (Precio)
- `S2`: Farewell (Despedida)
- `S3`: Hours (Horario)
- `S4`: Location (Ubicación)
- `S5`: Support (Soporte)
- `S6`: Unknown (Desconocido)

### 2. Decision Making ($\epsilon$-greedy Policy)
To decide how to respond, the agent:
- With probability **$\epsilon$ (Epsilon = 0.3)**: Chooses an action (response) completely at random to **explore** new options.
- With probability **$1 - \epsilon$**: Chooses the response that has the highest Q-value for the current state to **exploit** acquired knowledge.

### 3. Mathematical Update of the Q-value
When the user presses **Like (+1)** or **Dislike (-1)**, the Q-value of the selected State/Action combination is updated using the following temporal difference learning formula:

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \cdot [R_t - Q(S_t, A_t)]$$

Where:
- $Q(S_t, A_t)$ is the current value in the table for that state and intent.
- $\alpha$ (Learning rate = 0.5) determines how much the new feedback influences the previous knowledge.
- $R_t$ is the reward received ($+1.0$ or $-1.0$).
