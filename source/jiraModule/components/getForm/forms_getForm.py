
import json


def leer_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r',encoding='utf-8') as archivo:
            objeto_json = json.load(archivo)

            
            return objeto_json
               

            return objeto_json
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se encontró.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el JSON en '{nombre_archivo}': {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el json : {e}")

forms = leer_json('./docs/forms.json')

traditionalTecno = forms['traditionalTecno']

traditional = forms['traditional']

personas =  forms['personas']


formsTecno = {  
    "traditional": traditionalTecno,
    "personas": personas
    }

formsAdmin = {
    "traditional": traditionalTecno
}

formsProcesos = {
    "traditional": traditional
}

formsUsuario = {
    "traditional": traditional,
    "personas" : personas
}
