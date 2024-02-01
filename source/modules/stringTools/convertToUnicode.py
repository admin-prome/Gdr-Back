import unidecode


def normalizarTexto(texto):
    # Normaliza el texto eliminando acentos y caracteres especiales
    return unidecode(texto)
