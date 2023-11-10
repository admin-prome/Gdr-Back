from difflib import SequenceMatcher
from unidecode import unidecode

def calculate_similarity(a: str, b: str):
    """
    Pre: Recibe dos string
    Pos: Devuelve el porcentaje de similitud
    """
    return SequenceMatcher(None, a, b).ratio()

def remove_keywords(sentence: str, keywords: list):
    """
    Pre: Recibe un string y una lista de palabras que se deseen eliminar del string
    Pos: Devuelve el string sin las palabras coincidentes en la lista keywords
    """
    sentence = unidecode(sentence.lower())
    return ' '.join(word for word in sentence.split() if all(keyword not in word for keyword in keywords))

def find_max_similarity(text: str, options: list, keywords_to_remove=None):
    """
    Encontrar la opción con el máximo porcentaje de similitud con el texto proporcionado.
    Opcionalmente, eliminar las palabras clave especificadas antes de realizar la comparación
    """
    if keywords_to_remove:
        text = remove_keywords(text, keywords_to_remove)

    best_match = None
    best_similarity = 0

    for option in options:
        option_processed = remove_keywords(option, keywords_to_remove) if keywords_to_remove else option

        similarity = calculate_similarity(text, option_processed)

        if similarity > best_similarity:
            best_match = option
            best_similarity = similarity

    return best_match

if __name__ == '__main__':
    
    departments = {
        "administracion y finanzas": "10028",
        "red de sucursales": "10034",
        "cumplimiento y procesos": "10031",
        "inteligencia de negocios y gestion estrategica": "10036",
        "comercial": "10030",
        "personas": "10033",
        "tecnologia": "10029",
        "direccion ejecutiva": "10029",
        "riesgo": "10032",
        "comunicacion institucional": "10035",
        "investigacion y capacitacion": "10036"
    }

    text = "Gerencias De Tecnología"
    options = departments.keys()
    print(options)
    keywords_to_ignore = ["gerencia", "gcia", "gerencias", "gerenc", "gerenc"]

    result = find_max_similarity(text, options, keywords_to_ignore)
    print("Best match:", result)
