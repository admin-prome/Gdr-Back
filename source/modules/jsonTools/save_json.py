import json


def guardar_json(diccionario, nombre_archivo='archivo.json'):
    """
    Guarda un diccionario como un archivo JSON.

    :param diccionario: El diccionario que se desea guardar.
    :param nombre_archivo: El nombre del archivo JSON (por defecto, 'archivo.json').
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(diccionario, archivo, ensure_ascii=False, indent=2)
