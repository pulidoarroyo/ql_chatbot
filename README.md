# ql_chatbot - Chatbot Interactivo con Aprendizaje por Refuerzo Q-Learning

Este proyecto es un chatbot interactivo de escritorio desarrollado en Python utilizando la biblioteca gráfica **Tkinter**. El bot utiliza el algoritmo de aprendizaje por refuerzo **Q-Learning** (simplificado como un *Contextual Bandit* con factor de descuento $\gamma = 0$) para aprender de forma dinámica a responder de manera óptima según la intención del usuario y la retroalimentación en tiempo real (Likes/Dislikes).

## 🚀 Características

- **Clasificación de Intenciones por Palabras Clave**: Detecta intenciones como saludos, preguntas sobre precios, horarios, ubicación, soporte técnico y despedidas.
- **Toma de Decisiones Epsilon-Greedy**: Alterna de forma balanceada entre la exploración (acciones aleatorias para descubrir nuevas respuestas) y la explotación (seleccionar la mejor respuesta aprendida).
- **Retroalimentación Interactiva**: El usuario puede calificar las respuestas del bot (+1 / -1) para actualizar la tabla de valores Q.
- **Visualización en Tiempo Real**:
  - Muestra la tabla de valores Q actualizada.
  - Visualización paso a paso de la fórmula matemática aplicada en cada actualización.
  - Historial de chat codificado por colores.
- **Persistencia**: La tabla Q se guarda de manera automática en un archivo `q_table.json`.

---

## 📁 Estructura del Proyecto

El proyecto se organiza de la siguiente manera:

```text
ql_chatbot/
│
├── main.py          # Punto de entrada de la aplicación. Inicializa el agente y lanza la interfaz Tkinter.
├── agent.py         # Clase QLearningAgent. Implementa la lógica del agente, selección de acciones y actualización de valores Q.
├── data.py          # Definición de los Estados (Intenciones), Acciones (Respuestas) y Palabras Clave para concordancia.
├── gui.py           # Clase ChatbotGUI. Interfaz gráfica interactiva y visualizaciones del agente en Tkinter.
├── q_table.json     # Archivo JSON persistente donde se guardan los valores de la tabla Q entrenados.
└── README.md        # Documentación de estructura y requisitos del proyecto.
```

---

## 🛠️ Requisitos del Proyecto

### Requisitos del Sistema
- **Python 3.x** instalado en el sistema.

### Dependencias
El proyecto utiliza bibliotecas nativas de Python, por lo que **no requiere instalar dependencias de terceros** (`pip install`).
- `tkinter` (incluido por defecto en la mayoría de las distribuciones de Python).
- `random` (estándar de Python).
- `json` (estándar de Python).
- `os` (estándar de Python).

*Nota para sistemas Linux:* Si ejecutas la aplicación en Linux y tienes problemas al abrir la interfaz gráfica, asegúrate de instalar Tkinter ejecutando:
```bash
sudo apt-get install python3-tk
```

---

## ⚙️ Cómo Ejecutar el Proyecto

1. Clona o descarga el repositorio en tu máquina local.
2. Abre una terminal en el directorio raíz del proyecto: `ql_chatbot`.
3. Ejecuta el siguiente comando para iniciar el chatbot:
   ```bash
   python main.py
   ```

---

## 🧠 ¿Cómo Funciona la Inteligencia Artificial?

El agente de IA modela el problema como un **Contextual Bandit** (un caso especial de Q-Learning donde el estado futuro no depende de la acción actual, por ende, el factor de descuento $\gamma = 0$):

### 1. Estados e Intenciones
El bot clasifica el texto ingresado por el usuario en uno de los siguientes estados (intenciones definidas en `data.py`):
- `S0`: Saludo
- `S1`: Precio
- `S2`: Despedida
- `S3`: Horario
- `S4`: Ubicación
- `S5`: Soporte
- `S6`: Desconocido

### 2. Toma de Decisiones (Política $\epsilon$-greedy)
Para decidir qué responder, el agente:
- Con probabilidad **$\epsilon$ (Epsilon = 0.3)**: Elige una acción (respuesta) de forma completamente aleatoria para **explorar** nuevas opciones.
- Con probabilidad **$1 - \epsilon$**: Elige la respuesta que tiene el mayor valor Q para el estado actual para **explotar** el conocimiento adquirido.

### 3. Actualización Matemática del Valor Q
Cuando el usuario presiona **Like (+1)** o **Dislike (-1)**, el valor Q de la combinación Estado/Acción seleccionada se actualiza usando la siguiente fórmula de aprendizaje por diferencia temporal:

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \cdot [R_t - Q(S_t, A_t)]$$

Donde:
- $Q(S_t, A_t)$ es el valor actual en la tabla para ese estado e intención.
- $\alpha$ (Tasa de aprendizaje = 0.5) determina qué tanto influye la nueva retroalimentación sobre el conocimiento previo.
- $R_t$ es la recompensa recibida ($+1.0$ o $-1.0$).
