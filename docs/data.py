import re
from unidecode import unidecode 

def buscarCoincidencia(texto, palabras_clave):
    for palabra_clave in palabras_clave:
        # Compila el patrón con la bandera re.IGNORECASE para que sea insensible a mayúsculas y minúsculas
        regex = re.compile(rf'{palabra_clave}', re.IGNORECASE)
        if regex.search(texto):
            return True
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

    texto_normalizado = normalizarTexto(texto)

    for gerencia, codigo in gerencias.items():
        palabras_clave = gerencia.split()  # Dividir el nombre de la gerencia en palabras clave
        if buscarCoincidencia(texto_normalizado, palabras_clave):
            return {"gerencia": gerencia, "codigo": codigo}

    return {"gerencia": "No se encontró coincidencia", "codigo": None}

if __name__ == '__main__':
   # Ejemplo de uso
    texto = "Gerencias De Tecnología"
    resultado = clasificarGerencia(texto)
    print("Gerencia:", resultado["gerencia"])
    print("Código:", resultado["codigo"])
