# data.py

# Estados (Intenciones del usuario)
STATES = {
    "S0": "Saludo",
    "S1": "Precio",
    "S2": "Despedida",
    "S3": "Desconocido"
}

# Acciones (Respuestas del bot)
ACTIONS = {
    "A0": "¡Hola! ¿En qué te ayudo?",
    "A1": "Cuesta 20$.",
    "A2": "¡Adiós! Vuelve pronto.",
    "A3": "¿Puedes repetir?"
}

# Palabras clave para clasificar la intención del usuario (Ejemplo básico)
KEYWORDS = {
    "hola": "S0", "buenas": "S0", "saludos": "S0",
    "precio": "S1", "costo": "S1", "cuanto": "S1",
    "adios": "S2", "chao": "S2", "hasta luego": "S2"
}