# data.py

STATES = {
    "S0": "Saludo",
    "S1": "Precio",
    "S2": "Despedida",
    "S3": "Desconocido"
}

ACTIONS = {
    "A0": "¡Hola! ¿En qué te puedo ayudar?",
    "A1": "El precio es de 20 dólares.",
    "A2": "¡Adiós! Vuelve pronto.",
    "A3": "¿Puedes repetir? No te entendí."
}

# Diccionario para clasificar texto usando palabras clave simples
KEYWORDS = {
    "S0": ["hola", "buenas", "tal", "saludos", "que mas"],
    "S1": ["precio", "costo", "cuanto", "vale", "dolares", "valor"],
    "S2": ["adios", "chao", "nos vemos", "bye", "hasta luego"]
}