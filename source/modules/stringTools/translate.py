def translate_priority(priority_name, idioma_destino='es'):
    """
    Traduce el nombre de la prioridad de Jira al idioma especificado utilizando un diccionario predefinido.

    :param priority_name: Nombre de la prioridad a traducir.
    :param idioma_destino: Idioma al que se desea traducir (por defecto, español).
    :return: El nombre de la prioridad traducido.
    """
    diccionario_traducciones = {
        'High': 'Alta',
        'Medium': 'Estándar',
        'Low': 'Baja',
        'Highest': 'Muy Alta',
        'Lowest': 'Muy Baja',
        'Normative': 'Normativa',
        # Agrega más traducciones según sea necesario
    }

    # Traduce utilizando el diccionario predefinido
    translated_name = diccionario_traducciones.get(priority_name, priority_name)

    return translated_name