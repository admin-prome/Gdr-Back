import re
from difflib import SequenceMatcher
from unidecode import unidecode

def buscarCoincidencia(texto, palabras_clave):
    for palabra_clave in palabras_clave:
        # Compila el patrón con la bandera re.IGNORECASE para que sea insensible a mayúsculas y minúsculas
        regex = re.compile(rf'{palabra_clave}', re.IGNORECASE)
        if regex.search(texto):
            return True
    return False


def search_match(text: str, keywords: str) -> bool:
    '''
    Busca coincidencias de palabras clave en texto.

    Argumentos:
    texto: El texto a buscar.
    palabras_clave: Una lista de palabras clave a buscar.
    Devuelve:
    True si se encuentra alguna de las palabras clave en el texto, False en caso contrario.
    '''

    # Converts all keywords to lowercase to make them case-insensitive.
    keywords = [keyword.lower() for keyword in keywords]

    # Uses the `re.findall()` method to find all matches of the keywords in the text.
    matches = re.findall(rf"({'|'.join(keywords)})", text.lower())

    # Returns True if any matches are found, False otherwise.
    return len(matches) > 0


def normalizarTexto(texto):
    # Normaliza el texto eliminando acentos y caracteres especiales
    return unidecode(texto)

###############################################################################################################

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
    
    try:
        sentence = unidecode(sentence.lower())
        return ' '.join(word for word in sentence.split() if all(keyword not in word for keyword in keywords))
    except Exception as e:
        print(f'Ocurrio un erorr al intentar remover palabras del string: {e}')
        return sentence
   

def find_max_similarity(text: str, options: list, keywords_to_remove=None):
    """
    Encontrar la opción con el máximo porcentaje de similitud con el texto proporcionado.
    Opcionalmente, eliminar las palabras clave especificadas antes de realizar la comparación
    """
    try: 
        best_match = None
        best_similarity = 0
        
        if keywords_to_remove:
            text = remove_keywords(text, keywords_to_remove)        

        for option in options:
            option_processed = remove_keywords(option, keywords_to_remove) if keywords_to_remove else option

            similarity = calculate_similarity(text, option_processed)

            if similarity > best_similarity:
                best_match = option
                best_similarity = similarity
    except Exception as e: print(f'Ocurrio un error al buscar la similitud de palabras: {e}')

    return best_match


def split_identifier_from_title(input_string: str)->tuple:
    # Define the regex pattern to find the specified nomenclature
    regex_pattern = r'\[([^\]]+)\] (.+)'

    # Search for the pattern in the input_string
    match = re.search(regex_pattern, input_string)

    # Check if the pattern is found
    if match:
        # Get the first and second captured groups
        first_group = match.group(1)
        second_group = match.group(2)

        # Return the results as a tuple
        return first_group, second_group
    else:
        # If the pattern is not found, return None
        return None, None