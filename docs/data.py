import re
from unidecode import unidecode
from difflib import get_close_matches

def buscarCoincidencia(text, keywords):
    print(text)
    # Converts all keywords to lowercase to make them case-insensitive.
    keywords = [keyword.lower() for keyword in keywords]
    for i in range(len(keywords)):
        list = keywords[i].split(' ')
        print(list)
        for j in list: 
            if text in j:
                print('match')
                print(j)
                print(text)
                return j
    # Uses the `re.findall()` method to find all matches of the keywords in the text.
    matches = re.findall(rf"({'|'.join(keywords)})", text.lower())
    print(matches)
    
    # Returns True if any matches are found, False otherwise.
    return False

def normalizarTexto(texto):
    # Normaliza el texto eliminando acentos y caracteres especiales
    return unidecode(texto)

def clasificarGerencia(texto):
    gerencias = {
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

    texto_normalizado = unidecode(texto.lower())

    textos_normalizados = texto_normalizado.split()
    
    for texto in textos_normalizados:
        list_gerencias = list(gerencias.keys())
        print(list_gerencias)
        for gerencia in list_gerencias:
            print(f'esto es la gerencias: {gerencia} texto: {texto}')
            if texto in gerencias:
                print({"gerencia": texto, "codigo": gerencias[texto]})
                return {"gerencia": texto, "codigo": gerencias[texto]}
    else:
        matches = get_close_matches(texto_normalizado, gerencias.keys(), n=1, cutoff=0.8)
        if matches:
            gerencia = matches[0]
            return {"gerencia": gerencia, "codigo": gerencias[gerencia]}
        else:
            respuesta = buscarCoincidencia(texto_normalizado, gerencias.keys())
            if  respuesta!= False:
                print('hola')
                for respuesta, codigo in gerencias.items():
                    if re.search(respuesta, texto_normalizado):
                        return {"gerencia": gerencia, "codigo": codigo}
            return {"gerencia": "No se encontró coincidencia", "codigo": None}

if __name__ == '__main__':
   # Ejemplo de uso
    texto = "gcia investigacion"
    resultado = clasificarGerencia(texto)
    print("Gerencia:", resultado["gerencia"])
    print("Código:", resultado["codigo"])