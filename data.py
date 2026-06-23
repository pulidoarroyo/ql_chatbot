# data.py

STATES = {
    "S0": "Saludo",
    "S1": "Precio",
    "S2": "Despedida",
    "S3": "Horario",
    "S4": "Ubicacion",
    "S5": "Soporte",
    "S6": "Desconocido"
}

ACTIONS = {
    "A0": "¡Hola! ¿En qué te puedo ayudar hoy?",
    "A1": "El precio de nuestro servicio es de 20 dólares al mes.",
    "A2": "¡Hasta luego! Fue un placer atenderte.",
    "A3": "Atendemos de Lunes a Viernes de 8am a 6pm.",
    "A4": "Estamos ubicados en la Av. Principal, edificio Tech, piso 3.",
    "A5": "Para soporte técnico, puedes escribirnos a soporte@empresa.com.",
    "A6": "Lo siento, no entendí tu pregunta. ¿Puedes reformularla?"
}

# Palabras clave por intención
KEYWORDS = {
    "S0": ["hola", "buenas", "buenos", "saludos", "qué tal", "que tal", "hey", "buen dia", "buen día", "buenas tardes", "buenas noches"],
    "S1": ["precio", "costo", "cuánto", "cuanto", "vale", "valor", "tarifa", "cobran", "cuesta", "pagar", "dólares", "dolares"],
    "S2": ["adios", "adiós", "chao", "chau", "bye", "hasta luego", "hasta pronto", "nos vemos", "me voy"],
    "S3": ["horario", "hora", "abren", "cierran", "atención", "atencion", "cuando atienden", "disponible", "disponibilidad"],
    "S4": ["dónde", "donde", "ubicación", "ubicacion", "dirección", "direccion", "localización", "localizacion", "lugar", "llegar"],
    "S5": ["soporte", "ayuda", "problema", "error", "fallo", "falla", "no funciona", "broken", "técnico", "tecnico", "asistencia"]
}