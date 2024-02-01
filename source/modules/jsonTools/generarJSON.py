import json
import os

def generate_and_save_json(data, filename):
    # Verificar y crear el directorio 'BackGDR/docs' si no existe
    target_dir = 'gdrback/docs'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Obtener la ruta del directorio padre
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    
    # Combinar la ruta del directorio objetivo con el nombre del archivo
    file_path = os.path.join(parent_dir, target_dir, filename)
    
    # Guardar el JSON en un archivo
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
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
