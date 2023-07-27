import json
import os

def generate_and_save_json(data, filename):
    # Generar el JSON
    #json_data = json.dumps(data, indent=4)
    
    # Obtener la ruta del directorio padre
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    
    # Combinar la ruta del directorio objetivo con el nombre del archivo
    file_path = os.path.join(parent_dir, 'BackGDR/docs', filename)
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    # Guardar el JSON en un archivo
    with open(file_path, 'w') as file:
        file.write(str(data))
    
    print(f"Archivo JSON guardado como {file_path}")

# Ejemplo de uso

if __name__ == '__main__':
    data = {
        'nombre': 'John Doe',
        'edad': 30,
        'ciudad': 'Ejemploville'
    }

    filename = 'data.json'
    generate_and_save_json(data, filename)
